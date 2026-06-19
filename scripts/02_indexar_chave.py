#!/usr/bin/env python3
# =============================================================================
# 02_indexar_chave.py
# Indexação da coleção CHAVE no Meilisearch — Trabalho Final PRI 2025/2026
# Grupo 04 — Weber Souza, Mário Nogueira, Saiton Silva
#
# Função: configura o índice 'chave' no Meilisearch e envia os 43 lotes JSON
# em sequência, aguardando confirmação de cada tarefa antes de prosseguir.
# Regista tempos, totais e erros para documentação no relatório académico.
#
# Uso (na VPS):
#   python3 02_indexar_chave.py \
#       --pasta  /opt/pri-trabalho-final/json_lotes \
#       --host   http://localhost:7700 \
#       --chave  15e5fc92604b9aad3e67154d71c24569
#
# Dependências: apenas biblioteca padrão do Python 3.6+
# =============================================================================

import argparse
import json
import os
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# Cliente HTTP mínimo para a API REST do Meilisearch
# ---------------------------------------------------------------------------

class MeilisearchClient:
    def __init__(self, host: str, master_key: str):
        self.host = host.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {master_key}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, body: bytes = None) -> dict:
        url = f"{self.host}{path}"
        req = urllib.request.Request(url, data=body, headers=self.headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            erro = json.loads(e.read().decode("utf-8"))
            raise RuntimeError(f"HTTP {e.code} em {path}: {erro}")

    def get(self, path: str) -> dict:
        return self._request("GET", path)

    def post(self, path: str, payload: dict) -> dict:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        return self._request("POST", path, body)

    def patch(self, path: str, payload: dict) -> dict:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        return self._request("PATCH", path, body)

    def put(self, path: str, payload: dict) -> dict:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        return self._request("PUT", path, body)

    def aguardar_tarefa(self, task_uid: int, intervalo: float = 2.0,
                        timeout: float = 600.0) -> dict:
        """Aguarda uma tarefa assíncrona do Meilisearch concluir."""
        inicio = time.time()
        while True:
            tarefa = self.get(f"/tasks/{task_uid}")
            status = tarefa.get("status")
            if status in ("succeeded", "failed", "canceled"):
                return tarefa
            if time.time() - inicio > timeout:
                raise TimeoutError(
                    f"Tarefa {task_uid} não concluiu em {timeout}s"
                )
            time.sleep(intervalo)


# ---------------------------------------------------------------------------
# Configuração do índice
# ---------------------------------------------------------------------------

CONFIGURACAO_INDICE = {
    "searchableAttributes": ["texto", "titulo_extraido"],
    "filterableAttributes": ["fonte", "ano", "categoria"],
    "sortableAttributes":   ["data", "ano"],
    "displayedAttributes":  [
        "id", "fonte", "data", "ano", "categoria",
        "texto", "ficheiro_origem", "titulo_extraido"
    ],
    # Ranking rules: configuração padrão do Meilisearch v1.13.0
    # Mantida conforme decisão do Trabalho B (Grupo 04, 2026)
    "rankingRules": [
        "words", "typo", "proximity", "attribute", "sort", "exactness"
    ],
}


def configurar_indice(client: MeilisearchClient, nome_indice: str) -> None:
    """Cria o índice se não existir e aplica as configurações."""
    print(f"\n[CONFIGURAÇÃO] Verificando índice '{nome_indice}'...")

    # Verificar se o índice já existe
    try:
        info = client.get(f"/indexes/{nome_indice}")
        print(f"  Índice '{nome_indice}' já existe "
              f"({info.get('numberOfDocuments', 0)} documentos). "
              f"Continuando a indexação.")
    except RuntimeError:
        # Índice não existe — criar
        print(f"  Criando índice '{nome_indice}'...")
        resp = client.post("/indexes", {
            "uid":        nome_indice,
            "primaryKey": "id"
        })
        task_uid = resp.get("taskUid")
        if task_uid:
            client.aguardar_tarefa(task_uid)
        print(f"  Índice '{nome_indice}' criado.")

    # Aplicar configurações
    print("  Aplicando configurações de atributos e ranking...")
    resp = client.patch(f"/indexes/{nome_indice}/settings", CONFIGURACAO_INDICE)
    task_uid = resp.get("taskUid")
    if task_uid:
        tarefa = client.aguardar_tarefa(task_uid)
        if tarefa["status"] == "succeeded":
            print("  Configurações aplicadas com sucesso.")
        else:
            raise RuntimeError(f"Falha ao aplicar configurações: {tarefa}")


# ---------------------------------------------------------------------------
# Indexação em lotes
# ---------------------------------------------------------------------------

def indexar_lotes(
    client: MeilisearchClient,
    pasta: Path,
    nome_indice: str,
) -> dict:
    """Envia cada lote JSON ao Meilisearch e aguarda confirmação."""

    arquivos = sorted(pasta.glob("chave_lote_*.json"))
    total_arquivos = len(arquivos)

    if total_arquivos == 0:
        raise FileNotFoundError(f"Nenhum lote JSON encontrado em {pasta}")

    print(f"\n[INDEXAÇÃO] {total_arquivos} lotes encontrados em {pasta}")
    print(f"  Índice de destino: '{nome_indice}'")
    print(f"  Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    total_docs_enviados  = 0
    total_docs_indexados = 0
    erros                = []
    tempos_lote          = []
    inicio_geral         = time.time()

    for i, arquivo in enumerate(arquivos, 1):
        print(f"  Lote {i:02d}/{total_arquivos}: {arquivo.name} ", end="", flush=True)

        # Carregar documentos do lote
        with open(arquivo, "r", encoding="utf-8") as f:
            documentos = json.load(f)

        n_docs = len(documentos)
        total_docs_enviados += n_docs

        # Enviar ao Meilisearch
        t0 = time.time()
        try:
            resp = client.post(
                f"/indexes/{nome_indice}/documents",
                documentos
            )
            task_uid = resp.get("taskUid")
            if not task_uid:
                raise RuntimeError("Resposta sem taskUid")

            # Aguardar conclusão da tarefa
            tarefa = client.aguardar_tarefa(task_uid, intervalo=1.5, timeout=300)
            duracao = time.time() - t0
            tempos_lote.append(duracao)

            if tarefa["status"] == "succeeded":
                indexados = tarefa.get("details", {}).get("indexedDocuments", n_docs)
                total_docs_indexados += indexados
                print(f"OK — {indexados} docs em {duracao:.1f}s")
            else:
                erro_msg = tarefa.get("error", {}).get("message", "desconhecido")
                erros.append({"lote": arquivo.name, "erro": erro_msg})
                print(f"FALHOU — {erro_msg}")

        except Exception as e:
            duracao = time.time() - t0
            erros.append({"lote": arquivo.name, "erro": str(e)})
            print(f"ERRO — {e}")

    duracao_total = time.time() - inicio_geral

    # Verificação final via /stats
    try:
        stats = client.get("/stats")
        docs_no_servidor = (
            stats.get("indexes", {})
                 .get(nome_indice, {})
                 .get("numberOfDocuments", "N/A")
        )
    except Exception:
        docs_no_servidor = "N/A (erro ao consultar /stats)"

    resultado = {
        "timestamp_conclusao":       datetime.now().isoformat(),
        "indice":                    nome_indice,
        "total_lotes_processados":   total_arquivos,
        "total_docs_enviados":       total_docs_enviados,
        "total_docs_indexados":      total_docs_indexados,
        "docs_confirmados_no_indice": docs_no_servidor,
        "duracao_total_segundos":    round(duracao_total, 1),
        "duracao_media_por_lote_s":  round(
            sum(tempos_lote) / len(tempos_lote), 1
        ) if tempos_lote else 0,
        "erros":                     erros,
        "configuracao_aplicada":     CONFIGURACAO_INDICE,
    }

    return resultado


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Indexação da coleção CHAVE no Meilisearch"
    )
    parser.add_argument("--pasta",  default="/opt/pri-trabalho-final/json_lotes",
                        help="Pasta com os arquivos chave_lote_*.json")
    parser.add_argument("--host",   default="http://localhost:7700",
                        help="Endereço do Meilisearch (padrão: http://localhost:7700)")
    parser.add_argument("--chave",  required=True,
                        help="Master key do Meilisearch")
    parser.add_argument("--indice", default="chave",
                        help="Nome do índice a criar/usar (padrão: chave)")
    args = parser.parse_args()

    pasta = Path(args.pasta)
    if not pasta.exists():
        print(f"ERRO: pasta não encontrada: {pasta}")
        return

    client = MeilisearchClient(args.host, args.chave)

    # Verificar conectividade
    try:
        saude = client.get("/health")
        print(f"[CONEXÃO] Meilisearch: {saude.get('status', 'desconhecido')}")
    except Exception as e:
        print(f"[ERRO] Não foi possível conectar ao Meilisearch: {e}")
        return

    # Configurar índice
    configurar_indice(client, args.indice)

    # Indexar lotes
    resultado = indexar_lotes(client, pasta, args.indice)

    # Exibir resumo
    print("\n" + "=" * 60)
    print("INDEXAÇÃO CONCLUÍDA")
    print(f"  Documentos enviados  : {resultado['total_docs_enviados']}")
    print(f"  Documentos indexados : {resultado['total_docs_indexados']}")
    print(f"  Confirmado no índice : {resultado['docs_confirmados_no_indice']}")
    print(f"  Duração total        : {resultado['duracao_total_segundos']}s "
          f"({resultado['duracao_total_segundos']/60:.1f} min)")
    print(f"  Média por lote       : {resultado['duracao_media_por_lote_s']}s")
    if resultado["erros"]:
        print(f"  Erros                : {len(resultado['erros'])}")
        for e in resultado["erros"]:
            print(f"    - {e['lote']}: {e['erro']}")
    else:
        print("  Erros                : nenhum")
    print("=" * 60)

    # Salvar relatório
    rel_path = pasta / "relatorio_indexacao.json"
    with open(rel_path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"\nRelatório de indexação salvo em: {rel_path}")


if __name__ == "__main__":
    main()
