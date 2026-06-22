#!/usr/bin/env python3
# =============================================================================
# 04_configurar_stopwords_e_reexecutar.py
# Configuração de stop words no índice CHAVE e re-execução das consultas
# Trabalho Final PRI 2025/2026 — Grupo 04
#
# Este script:
#   1. Aplica lista de stop words ao índice 'chave'
#   2. Aguarda a conclusão da tarefa assíncrona
#   3. Re-executa as 200 questões QA@CLEF 2008 nos dois modos
#   4. Exporta CSVs e métricas comparativas (sem SW vs com SW)
#
# Uso (na VPS):
#   python3 04_configurar_stopwords_e_reexecutar.py \
#       --xml    /opt/pri-trabalho-final/QA-CLEF08-PT-PT_test.xml \
#       --chave  15e5fc92604b9aad3e67154d71c24569 \
#       --saida  /opt/pri-trabalho-final/resultados_sw
#
# Dependências: apenas biblioteca padrão Python 3.6+
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

import sys
sys.path.insert(0, str(Path(__file__).parent))
try:
    from resolucao_anaforas import RESOLUCOES
except ImportError:
    RESOLUCOES = {}
    print("AVISO: resolucao_anaforas.py não encontrado.")


# ---------------------------------------------------------------------------
# Stop words para português — focadas nas queries do QA@CLEF 2008
# ---------------------------------------------------------------------------
STOP_WORDS_PT = [
    # Artigos
    "o", "a", "os", "as", "um", "uma", "uns", "umas",
    # Preposições e contrações
    "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas",
    "ao", "à", "aos", "às", "pelo", "pela", "pelos", "pelas",
    "por", "para", "com", "sem", "sob", "sobre", "entre", "até",
    # Pronomes
    "se", "me", "te", "lhe", "nos", "vos", "lhes",
    "ele", "ela", "eles", "elas", "eu", "tu", "nós", "vós",
    "seu", "sua", "seus", "suas", "dele", "dela", "deles", "delas",
    "este", "esta", "estes", "estas", "esse", "essa", "esses", "essas",
    # Verbos auxiliares e cópula
    "é", "são", "foi", "foram", "ser", "estar", "ter", "tem",
    "era", "eram", "sendo", "sido", "tendo", "teve",
    # Palavras interrogativas (presentes nas queries mas sem valor de conteúdo)
    "que", "quem", "qual", "quais", "onde", "quando", "como",
    "quanto", "quantos", "quantas", "diga",
    # Conjunções e advérbios frequentes
    "e", "ou", "mas", "porém", "que", "porque", "pois",
    "não", "mais", "muito", "também", "já", "ainda", "mesmo",
    "bem", "há", "lá", "cá", "aqui", "ali",
    # Outros tokens de alta frequência sem valor discriminativo
    "num", "numa", "nuns", "numas", "dum", "duma",
    "às", "ao", "neste", "nesta", "nesse", "nessa",
    "deste", "desta", "desse", "dessa",
]


# ---------------------------------------------------------------------------
# Cliente HTTP mínimo
# ---------------------------------------------------------------------------

class MeilisearchClient:
    def __init__(self, host: str, master_key: str):
        self.host = host.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {master_key}",
            "Content-Type":  "application/json",
        }

    def _request(self, method, path, body=None):
        url = f"{self.host}{path}"
        req = urllib.request.Request(
            url, data=body, headers=self.headers, method=method
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise RuntimeError(json.loads(e.read().decode("utf-8")))

    def get(self, path):
        return self._request("GET", path)

    def put(self, path, payload):
        return self._request("PUT", path,
                             json.dumps(payload, ensure_ascii=False).encode())

    def patch(self, path, payload):
        return self._request("PATCH", path,
                             json.dumps(payload, ensure_ascii=False).encode())

    def post(self, path, payload):
        return self._request("POST", path,
                             json.dumps(payload, ensure_ascii=False).encode())

    def aguardar(self, task_uid, intervalo=1.5, timeout=120):
        t0 = time.time()
        while True:
            t = self.get(f"/tasks/{task_uid}")
            if t.get("status") in ("succeeded", "failed", "canceled"):
                return t
            if time.time() - t0 > timeout:
                raise TimeoutError(f"Tarefa {task_uid} não concluiu em {timeout}s")
            time.sleep(intervalo)

    def search(self, indice, query, top_k):
        payload = {
            "q":     query,
            "limit": top_k,
            "attributesToRetrieve": [
                "id", "fonte", "data", "ano", "categoria", "ficheiro_origem"
            ],
        }
        t0 = time.time()
        data = self.post(f"/indexes/{indice}/search", payload)
        duracao = round((time.time() - t0) * 1000, 1)
        return data, duracao


# ---------------------------------------------------------------------------
# Leitura do XML
# ---------------------------------------------------------------------------

def carregar_perguntas(caminho):
    root = ET.parse(caminho).getroot()
    return [{"q_id": q.get("q_id"),
             "q_group_id": q.get("q_group_id"),
             "original": q.text.strip()}
            for q in root.findall("q")]


# ---------------------------------------------------------------------------
# Execução das consultas
# ---------------------------------------------------------------------------

CAMPOS_CSV = [
    "q_id", "q_group_id", "pergunta_orig", "query_enviada",
    "tipo_anafora", "modo", "n_retornados", "total_hits_est", "tempo_ms",
    "doc_1_id", "doc_1_fonte", "doc_1_data",
    "doc_2_id", "doc_3_id", "doc_4_id", "doc_5_id",
    "doc_6_id", "doc_7_id", "doc_8_id", "doc_9_id", "doc_10_id",
    "todos_doc_ids", "erro",
]


def executar(client, perguntas, indice, top_k, modo):
    resultados = []
    total = len(perguntas)
    print(f"\n  [{modo.upper()}] {total} consultas...")

    for i, p in enumerate(perguntas, 1):
        qid = p["q_id"]
        if modo == "resolvida" and qid in RESOLUCOES:
            query = RESOLUCOES[qid]["resolvida"]
            anafora = RESOLUCOES[qid]["tipo"]
        else:
            query = p["original"]
            anafora = "N/A"

        try:
            data, ms = client.search(indice, query, top_k)
            hits = data.get("hits", [])
            ids = [h.get("id", "") for h in hits]
            linha = {
                "q_id": qid, "q_group_id": p["q_group_id"],
                "pergunta_orig": p["original"], "query_enviada": query,
                "tipo_anafora": anafora, "modo": modo,
                "n_retornados": len(hits),
                "total_hits_est": data.get("estimatedTotalHits", 0),
                "tempo_ms": ms,
                "doc_1_id":  ids[0] if len(ids) > 0 else "",
                "doc_1_fonte": hits[0].get("fonte","") if hits else "",
                "doc_1_data":  hits[0].get("data","")  if hits else "",
                **{f"doc_{k}_id": ids[k-1] if len(ids) >= k else ""
                   for k in range(2, 11)},
                "todos_doc_ids": "|".join(ids), "erro": "",
            }
        except Exception as e:
            linha = {f: "" for f in CAMPOS_CSV}
            linha.update({"q_id": qid, "q_group_id": p["q_group_id"],
                          "pergunta_orig": p["original"],
                          "query_enviada": query, "modo": modo,
                          "n_retornados": 0, "erro": str(e)})

        resultados.append(linha)
        if i % 25 == 0 or i == total:
            print(f"    {i}/{total}", end="\r")
        time.sleep(0.05)

    print()
    return resultados


def salvar_csv(resultados, caminho):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
        w.writeheader()
        w.writerows(resultados)
    print(f"  CSV: {caminho}")


def metricas(resultados, modo):
    total = len(resultados)
    com   = sum(1 for r in resultados if r["n_retornados"] > 0)
    tempos = [float(r["tempo_ms"]) for r in resultados if r["tempo_ms"]]

    # Hits médios estimados (mede ruído: quanto menor, melhor após SW)
    hits_est = [int(r["total_hits_est"]) for r in resultados
                if str(r["total_hits_est"]).isdigit()]
    hits_medio = round(sum(hits_est) / len(hits_est)) if hits_est else 0

    fontes = [r["doc_1_fonte"] for r in resultados if r.get("doc_1_fonte")]
    dist = {}
    for f in fontes:
        dist[f] = dist.get(f, 0) + 1

    return {
        "modo": modo,
        "total": total,
        "com_resultado": com,
        "cobertura_pct": round(com / total * 100, 1),
        "hits_estimados_medio": hits_medio,
        "tempo_medio_ms": round(sum(tempos)/len(tempos), 1) if tempos else 0,
        "tempo_max_ms":   max(tempos) if tempos else 0,
        "distribuicao_fonte_doc1": dist,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--xml",    required=True)
    parser.add_argument("--host",   default="http://localhost:7700")
    parser.add_argument("--chave",  required=True)
    parser.add_argument("--indice", default="chave")
    parser.add_argument("--topk",   type=int, default=10)
    parser.add_argument("--saida",  default="/opt/pri-trabalho-final/resultados_sw")
    parser.add_argument("--sem-stopwords", action="store_true",
                        help="Remover stop words do índice (restaurar estado original)")
    args = parser.parse_args()

    pasta = Path(args.saida)
    pasta.mkdir(parents=True, exist_ok=True)

    client = MeilisearchClient(args.host, args.chave)

    # Verificar conexão
    saude = client.get("/health")
    print(f"[CONEXÃO] Meilisearch: {saude.get('status')}")

    # Mostrar configuração actual de stop words
    try:
        sw_actual = client.get(f"/indexes/{args.indice}/settings/stop-words")
        print(f"[ESTADO ACTUAL] Stop words: {len(sw_actual)} palavras configuradas")
    except Exception:
        print("[ESTADO ACTUAL] Stop words: nenhuma")

    if args.sem_stopwords:
        # Remover stop words (restaurar estado original)
        print("\n[CONFIG] Removendo stop words...")
        resp = client.put(f"/indexes/{args.indice}/settings/stop-words", [])
        tarefa = client.aguardar(resp.get("taskUid"))
        print(f"  Status: {tarefa['status']}")
    else:
        # Aplicar stop words
        print(f"\n[CONFIG] Aplicando {len(STOP_WORDS_PT)} stop words ao índice '{args.indice}'...")
        print(f"  Palavras: {', '.join(STOP_WORDS_PT[:15])}... (e mais {len(STOP_WORDS_PT)-15})")

        resp = client.put(
            f"/indexes/{args.indice}/settings/stop-words",
            STOP_WORDS_PT
        )
        task_uid = resp.get("taskUid")
        print(f"  Tarefa {task_uid} enviada. Aguardando conclusão...")
        tarefa = client.aguardar(task_uid, intervalo=2, timeout=120)

        if tarefa["status"] != "succeeded":
            print(f"  ERRO: {tarefa}")
            return
        print(f"  Stop words aplicadas com sucesso.")

    # Carregar perguntas
    perguntas = carregar_perguntas(args.xml)
    print(f"\n[XML] {len(perguntas)} perguntas carregadas")
    print(f"[CONFIG] Índice: '{args.indice}' | Top-K: {args.topk}")
    print(f"[INÍCIO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Executar consultas — modo original com SW
    res_orig = executar(client, perguntas, args.indice, args.topk, "original_sw")
    salvar_csv(res_orig, pasta / "resultados_original_sw.csv")

    # Executar consultas — modo resolvido com SW
    res_res = executar(client, perguntas, args.indice, args.topk, "resolvida_sw")
    salvar_csv(res_res, pasta / "resultados_resolvida_sw.csv")

    # Métricas
    m_o = metricas(res_orig, "original_sw")
    m_r = metricas(res_res, "resolvida_sw")

    metricas_json = {
        "timestamp": datetime.now().isoformat(),
        "stop_words_aplicadas": not args.sem_stopwords,
        "n_stop_words": len(STOP_WORDS_PT) if not args.sem_stopwords else 0,
        "original_sw": m_o,
        "resolvida_sw": m_r,
    }
    with open(pasta / "metricas_sw.json", "w", encoding="utf-8") as f:
        json.dump(metricas_json, f, ensure_ascii=False, indent=2)

    # Resumo comparativo
    print("\n" + "=" * 65)
    print("RESULTADOS COM STOP WORDS")
    print(f"  {'Métrica':<35} {'Original':>12} {'Resolvida':>12}")
    print(f"  {'-'*35} {'-'*12} {'-'*12}")
    print(f"  {'Com resultado':<35} {m_o['com_resultado']:>12} {m_r['com_resultado']:>12}")
    print(f"  {'Cobertura (%)':<35} {m_o['cobertura_pct']:>12} {m_r['cobertura_pct']:>12}")
    print(f"  {'Hits estimados médios':<35} {m_o['hits_estimados_medio']:>12} {m_r['hits_estimados_medio']:>12}")
    print(f"  {'Tempo médio (ms)':<35} {m_o['tempo_medio_ms']:>12} {m_r['tempo_medio_ms']:>12}")
    print("=" * 65)
    print(f"\nArquivos em: {pasta.resolve()}")
    print("\nIMPORTANTE: Compare 'hits_estimados_medio' com os valores")
    print("sem stop words (~1000). Uma redução expressiva indica que")
    print("as stop words melhoraram o foco do ranking.")
    print("\nPara restaurar o estado sem stop words:")
    print(f"  python3 {Path(__file__).name} --xml {args.xml} "
          f"--chave {args.chave} --sem-stopwords")


if __name__ == "__main__":
    main()
