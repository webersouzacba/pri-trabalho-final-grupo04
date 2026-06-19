#!/usr/bin/env python3
# =============================================================================
# 03_consultas_qa.py
# Execução das 200 questões do QA@CLEF 2008 contra o índice CHAVE
# Trabalho Final PRI 2025/2026 — Grupo 04
#
# Função: lê o QA-CLEF08-PT-PT_test.xml, envia cada pergunta ao Meilisearch
# em dois modos (original e com anáforas resolvidas), coleta os top-10
# documentos retornados e exporta CSV com todos os dados para avaliação.
#
# Uso (na VPS):
#   python3 03_consultas_qa.py \
#       --xml    /opt/pri-trabalho-final/QA-CLEF08-PT-PT_test.xml \
#       --host   http://localhost:7700 \
#       --chave  15e5fc92604b9aad3e67154d71c24569 \
#       --indice chave \
#       --topk   10 \
#       --saida  /opt/pri-trabalho-final/resultados
#
# Saída:
#   resultados_original.csv   — consultas com perguntas originais
#   resultados_resolvida.csv  — consultas com anáforas resolvidas
#   metricas.json             — Success@1/3/5/10 e MRR para ambos os modos
#
# Dependências: apenas biblioteca padrão do Python 3.6+
# =============================================================================

import argparse
import csv
import json
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# Importar as resoluções anafóricas (deve estar na mesma pasta)
import sys
sys.path.insert(0, str(Path(__file__).parent))
try:
    from resolucao_anaforas import RESOLUCOES
except ImportError:
    RESOLUCOES = {}
    print("AVISO: resolucao_anaforas.py não encontrado. "
          "Modo resolvido usará perguntas originais.")


# ---------------------------------------------------------------------------
# Cliente HTTP mínimo para o Meilisearch
# ---------------------------------------------------------------------------

class MeilisearchClient:
    def __init__(self, host: str, master_key: str):
        self.host = host.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {master_key}",
            "Content-Type":  "application/json",
        }

    def search(self, indice: str, query: str, top_k: int) -> dict:
        url     = f"{self.host}/indexes/{indice}/search"
        payload = json.dumps({
            "q":      query,
            "limit":  top_k,
            "attributesToRetrieve": [
                "id", "fonte", "data", "ano", "categoria", "ficheiro_origem"
            ],
            "attributesToHighlight": [],
            "attributesToCrop":     ["texto"],
            "cropLength":           50,
        }).encode("utf-8")

        req = urllib.request.Request(
            url, data=payload, headers=self.headers, method="POST"
        )
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data     = json.loads(resp.read().decode("utf-8"))
                duracao  = round((time.time() - t0) * 1000, 1)
                return data, duracao
        except urllib.error.HTTPError as e:
            erro = json.loads(e.read().decode("utf-8"))
            raise RuntimeError(f"HTTP {e.code}: {erro}")


# ---------------------------------------------------------------------------
# Leitura do XML
# ---------------------------------------------------------------------------

def carregar_perguntas(caminho_xml: str) -> list[dict]:
    tree = ET.parse(caminho_xml)
    root = tree.getroot()
    perguntas = []
    for q in root.findall("q"):
        perguntas.append({
            "q_id":       q.get("q_id"),
            "q_group_id": q.get("q_group_id"),
            "original":   q.text.strip(),
        })
    return perguntas


# ---------------------------------------------------------------------------
# Execução das consultas
# ---------------------------------------------------------------------------

def executar_consultas(
    client:   MeilisearchClient,
    perguntas: list[dict],
    indice:   str,
    top_k:    int,
    modo:     str,          # "original" ou "resolvida"
) -> list[dict]:
    """
    Executa todas as perguntas e retorna lista de resultados.
    Cada linha representa uma pergunta com os top-k documentos retornados.
    """
    resultados = []
    total = len(perguntas)

    print(f"\n[MODO: {modo.upper()}] Executando {total} consultas...")

    for i, p in enumerate(perguntas, 1):
        q_id = p["q_id"]

        # Determinar texto da query conforme o modo
        if modo == "resolvida" and q_id in RESOLUCOES:
            query_texto = RESOLUCOES[q_id]["resolvida"]
            tipo_anafora = RESOLUCOES[q_id]["tipo"]
        else:
            query_texto  = p["original"]
            tipo_anafora = "N/A"

        # Executar busca
        try:
            data, duracao_ms = client.search(indice, query_texto, top_k)
            hits             = data.get("hits", [])
            total_hits       = data.get("estimatedTotalHits", 0)
            n_retornados     = len(hits)

            # Extrair IDs e metadados dos documentos retornados
            docs_ids    = [h.get("id", "")    for h in hits]
            docs_fontes = [h.get("fonte", "") for h in hits]
            docs_datas  = [h.get("data", "")  for h in hits]
            docs_cats   = [h.get("categoria", "") for h in hits]

            linha = {
                "q_id":           q_id,
                "q_group_id":     p["q_group_id"],
                "pergunta_orig":  p["original"],
                "query_enviada":  query_texto,
                "tipo_anafora":   tipo_anafora,
                "modo":           modo,
                "n_retornados":   n_retornados,
                "total_hits_est": total_hits,
                "tempo_ms":       duracao_ms,
                "doc_1_id":       docs_ids[0]    if len(docs_ids)    > 0 else "",
                "doc_1_fonte":    docs_fontes[0] if len(docs_fontes) > 0 else "",
                "doc_1_data":     docs_datas[0]  if len(docs_datas)  > 0 else "",
                "doc_1_cat":      docs_cats[0]   if len(docs_cats)   > 0 else "",
                "doc_2_id":       docs_ids[1]    if len(docs_ids)    > 1 else "",
                "doc_3_id":       docs_ids[2]    if len(docs_ids)    > 2 else "",
                "doc_4_id":       docs_ids[3]    if len(docs_ids)    > 3 else "",
                "doc_5_id":       docs_ids[4]    if len(docs_ids)    > 4 else "",
                "doc_6_id":       docs_ids[5]    if len(docs_ids)    > 5 else "",
                "doc_7_id":       docs_ids[6]    if len(docs_ids)    > 6 else "",
                "doc_8_id":       docs_ids[7]    if len(docs_ids)    > 7 else "",
                "doc_9_id":       docs_ids[8]    if len(docs_ids)    > 8 else "",
                "doc_10_id":      docs_ids[9]    if len(docs_ids)    > 9 else "",
                "todos_doc_ids":  "|".join(docs_ids),
                "erro":           "",
            }

        except Exception as e:
            linha = {
                "q_id":           q_id,
                "q_group_id":     p["q_group_id"],
                "pergunta_orig":  p["original"],
                "query_enviada":  query_texto,
                "tipo_anafora":   tipo_anafora,
                "modo":           modo,
                "n_retornados":   0,
                "total_hits_est": 0,
                "tempo_ms":       0,
                **{f"doc_{k}_id": "" for k in range(1, 11)},
                "doc_1_fonte": "", "doc_1_data": "", "doc_1_cat": "",
                "doc_2_id": "", "doc_3_id": "", "doc_4_id": "",
                "doc_5_id": "", "doc_6_id": "", "doc_7_id": "",
                "doc_8_id": "", "doc_9_id": "", "doc_10_id": "",
                "todos_doc_ids":  "",
                "erro":           str(e),
            }

        resultados.append(linha)

        # Progresso a cada 20 perguntas
        if i % 20 == 0 or i == total:
            print(f"  {i}/{total} concluídas...", end="\r")

        # Pausa mínima para não sobrecarregar a API
        time.sleep(0.05)

    print(f"\n  Concluído: {total} consultas executadas.")
    return resultados


# ---------------------------------------------------------------------------
# Exportação CSV
# ---------------------------------------------------------------------------

CAMPOS_CSV = [
    "q_id", "q_group_id", "pergunta_orig", "query_enviada",
    "tipo_anafora", "modo", "n_retornados", "total_hits_est", "tempo_ms",
    "doc_1_id", "doc_1_fonte", "doc_1_data", "doc_1_cat",
    "doc_2_id", "doc_3_id", "doc_4_id", "doc_5_id",
    "doc_6_id", "doc_7_id", "doc_8_id", "doc_9_id", "doc_10_id",
    "todos_doc_ids", "erro",
]


def salvar_csv(resultados: list[dict], caminho: Path) -> None:
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
        writer.writeheader()
        writer.writerows(resultados)
    print(f"  CSV salvo: {caminho}")


# ---------------------------------------------------------------------------
# Cálculo de métricas
# ---------------------------------------------------------------------------

def calcular_metricas_placeholder(resultados: list[dict], modo: str) -> dict:
    """
    Calcula métricas de cobertura e tempo.
    Nota: Success@k e MRR requerem gabarito de respostas corretas.
    Como o QA@CLEF 2008 não fornece gabarito automático neste contexto,
    registamos métricas observáveis: cobertura (n_retornados > 0) e tempo médio.
    A avaliação qualitativa manual completará a análise no relatório.
    """
    total = len(resultados)
    com_resultados    = sum(1 for r in resultados if r["n_retornados"] > 0)
    sem_resultados    = total - com_resultados
    tempos            = [r["tempo_ms"] for r in resultados if r["tempo_ms"] > 0]
    tempo_medio       = round(sum(tempos) / len(tempos), 1) if tempos else 0
    tempo_max         = max(tempos) if tempos else 0
    tempo_min         = min(tempos) if tempos else 0

    # Cobertura por limiar de documentos retornados
    cob_top1  = sum(1 for r in resultados if r["n_retornados"] >= 1)
    cob_top3  = sum(1 for r in resultados if r["n_retornados"] >= 3)
    cob_top5  = sum(1 for r in resultados if r["n_retornados"] >= 5)
    cob_top10 = sum(1 for r in resultados if r["n_retornados"] >= 10)

    # Distribuição por fonte nos primeiros resultados
    fontes = [r["doc_1_fonte"] for r in resultados if r.get("doc_1_fonte")]
    dist_fontes = {}
    for f in fontes:
        dist_fontes[f] = dist_fontes.get(f, 0) + 1

    return {
        "modo":                    modo,
        "total_perguntas":         total,
        "com_resultados":          com_resultados,
        "sem_resultados":          sem_resultados,
        "cobertura_pct":           round(com_resultados / total * 100, 1),
        "cobertura_top1_pct":      round(cob_top1  / total * 100, 1),
        "cobertura_top3_pct":      round(cob_top3  / total * 100, 1),
        "cobertura_top5_pct":      round(cob_top5  / total * 100, 1),
        "cobertura_top10_pct":     round(cob_top10 / total * 100, 1),
        "tempo_medio_ms":          tempo_medio,
        "tempo_max_ms":            tempo_max,
        "tempo_min_ms":            tempo_min,
        "distribuicao_fonte_doc1": dist_fontes,
        "nota_avaliacao": (
            "Success@k e MRR requerem gabarito manual de respostas corretas. "
            "A cobertura aqui reportada indica apenas se o sistema retornou "
            "algum documento, não se o documento contém a resposta correta. "
            "A avaliação qualitativa manual consta do relatório."
        ),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Consultas QA@CLEF 2008 contra o índice CHAVE no Meilisearch"
    )
    parser.add_argument("--xml",    required=True,
                        help="Caminho para QA-CLEF08-PT-PT_test.xml")
    parser.add_argument("--host",   default="http://localhost:7700",
                        help="Endereço do Meilisearch")
    parser.add_argument("--chave",  required=True,
                        help="Master key do Meilisearch")
    parser.add_argument("--indice", default="chave",
                        help="Nome do índice (padrão: chave)")
    parser.add_argument("--topk",   type=int, default=10,
                        help="Número de documentos a recuperar por consulta (padrão: 10)")
    parser.add_argument("--saida",  default="/opt/pri-trabalho-final/resultados",
                        help="Pasta de saída para CSVs e métricas")
    args = parser.parse_args()

    pasta_saida = Path(args.saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)

    # Verificar conectividade
    client = MeilisearchClient(args.host, args.chave)
    try:
        req = urllib.request.Request(
            f"{args.host}/health",
            headers={"Authorization": f"Bearer {args.chave}"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            saude = json.loads(r.read())
        print(f"[CONEXÃO] Meilisearch: {saude.get('status')}")
    except Exception as e:
        print(f"[ERRO] Não foi possível conectar: {e}")
        return

    # Carregar perguntas
    perguntas = carregar_perguntas(args.xml)
    print(f"[XML] {len(perguntas)} perguntas carregadas de {args.xml}")
    print(f"[CONFIG] Índice: '{args.indice}' | Top-K: {args.topk} | "
          f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Executar modo original
    res_original = executar_consultas(
        client, perguntas, args.indice, args.topk, "original"
    )
    salvar_csv(res_original, pasta_saida / "resultados_original.csv")

    # Executar modo resolvido
    res_resolvida = executar_consultas(
        client, perguntas, args.indice, args.topk, "resolvida"
    )
    salvar_csv(res_resolvida, pasta_saida / "resultados_resolvida.csv")

    # Calcular e salvar métricas
    metricas = {
        "timestamp":  datetime.now().isoformat(),
        "indice":     args.indice,
        "top_k":      args.topk,
        "original":   calcular_metricas_placeholder(res_original,  "original"),
        "resolvida":  calcular_metricas_placeholder(res_resolvida, "resolvida"),
    }

    metricas_path = pasta_saida / "metricas.json"
    with open(metricas_path, "w", encoding="utf-8") as f:
        json.dump(metricas, f, ensure_ascii=False, indent=2)

    # Exibir resumo comparativo
    m_o = metricas["original"]
    m_r = metricas["resolvida"]

    print("\n" + "=" * 65)
    print("RESUMO COMPARATIVO — ORIGINAL vs. ANÁFORAS RESOLVIDAS")
    print(f"  {'Métrica':<35} {'Original':>10} {'Resolvida':>12}")
    print(f"  {'-'*35} {'-'*10} {'-'*12}")
    print(f"  {'Perguntas com resultado':<35} "
          f"{m_o['com_resultados']:>10} {m_r['com_resultados']:>12}")
    print(f"  {'Cobertura geral (%)':<35} "
          f"{m_o['cobertura_pct']:>10} {m_r['cobertura_pct']:>12}")
    print(f"  {'Cobertura top-1 (%)':<35} "
          f"{m_o['cobertura_top1_pct']:>10} {m_r['cobertura_top1_pct']:>12}")
    print(f"  {'Cobertura top-5 (%)':<35} "
          f"{m_o['cobertura_top5_pct']:>10} {m_r['cobertura_top5_pct']:>12}")
    print(f"  {'Cobertura top-10 (%)':<35} "
          f"{m_o['cobertura_top10_pct']:>10} {m_r['cobertura_top10_pct']:>12}")
    print(f"  {'Tempo médio por consulta (ms)':<35} "
          f"{m_o['tempo_medio_ms']:>10} {m_r['tempo_medio_ms']:>12}")
    print("=" * 65)
    print(f"\nArquivos gerados em: {pasta_saida.resolve()}")
    print(f"  resultados_original.csv")
    print(f"  resultados_resolvida.csv")
    print(f"  metricas.json")


if __name__ == "__main__":
    main()
