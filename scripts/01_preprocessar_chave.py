#!/usr/bin/env python3
# =============================================================================
# 01_preprocessar_chave.py
# Pré-processamento local da coleção CHAVE para o Trabalho Final PRI 2025/2026
# Grupo 04 — Weber Souza, Mário Nogueira, Saiton Silva
#
# Função: lê os ZIPs CHAVEPublico.zip e CHAVEFolha.zip diretamente (sem
# descompactar manualmente), extrai cada <DOC> dos arquivos SGML, converte
# de ISO-8859-1 para UTF-8, e serializa em arquivos JSON em lotes de 5.000
# documentos, prontos para indexação no Meilisearch.
#
# Uso:
#   python3 01_preprocessar_chave.py \
#       --publico CHAVEPublico.zip \
#       --folha   CHAVEFolha.zip \
#       --saida   ./json_lotes \
#       --lote    5000
#
# Dependências: apenas biblioteca padrão do Python 3.6+
# =============================================================================

import argparse
import json
import os
import re
import zipfile
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuração dos padrões de extração SGML
# ---------------------------------------------------------------------------

# Padrão para delimitar cada documento dentro de um arquivo SGML diário
RE_DOC = re.compile(r"<DOC>(.*?)</DOC>", re.DOTALL)

# Campos estruturados presentes de forma consistente na coleção CHAVE
RE_DOCNO    = re.compile(r"<DOCNO>\s*(.*?)\s*</DOCNO>", re.DOTALL)
RE_DATE     = re.compile(r"<DATE>\s*(.*?)\s*</DATE>",   re.DOTALL)
RE_CATEGORY = re.compile(r"<CATEGORY>\s*(.*?)\s*</CATEGORY>", re.DOTALL)
RE_TEXT     = re.compile(r"<TEXT>(.*?)</TEXT>", re.DOTALL)


def normalizar_data(raw: str) -> str:
    """Converte datas YYYYMMDD para YYYY-MM-DD. Retorna raw se não reconhecer."""
    raw = raw.strip()
    if re.match(r"^\d{8}$", raw):
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
    return raw


def extrair_titulo_opcional(texto: str) -> str | None:
    """
    Tenta extrair o título da primeira linha não-vazia do campo TEXT.
    Retorna None se a linha for muito longa (>= 120 chars) ou ausente.
    A ausência de marcação SGML consistente de título na coleção CHAVE
    foi identificada na inspeção do corpus; este campo é, portanto,
    tratado como metadado opcional e não estruturado.
    """
    for linha in texto.splitlines():
        linha = linha.strip()
        if linha and len(linha) < 120:
            return linha
    return None


def processar_sgml(conteudo_bytes: bytes, fonte: str, nome_ficheiro: str) -> list[dict]:
    """
    Recebe o conteúdo bruto de um arquivo SGML em ISO-8859-1,
    converte para UTF-8 e extrai todos os documentos <DOC>.
    Retorna lista de dicionários prontos para serialização JSON.
    """
    try:
        texto_utf8 = conteudo_bytes.decode("iso-8859-1")
    except UnicodeDecodeError:
        # Fallback com substituição de caracteres irrecuperáveis
        texto_utf8 = conteudo_bytes.decode("iso-8859-1", errors="replace")

    documentos = []
    for match in RE_DOC.finditer(texto_utf8):
        bloco = match.group(1)

        docno    = RE_DOCNO.search(bloco)
        date_raw = RE_DATE.search(bloco)
        category = RE_CATEGORY.search(bloco)
        text_raw = RE_TEXT.search(bloco)

        # Documentos sem DOCNO ou sem TEXT são descartados
        if not docno or not text_raw:
            continue

        docno_val = docno.group(1).strip()
        texto_val = text_raw.group(1).strip()
        data_raw  = date_raw.group(1).strip() if date_raw else ""
        data_norm = normalizar_data(data_raw) if data_raw else ""
        ano_val   = int(data_norm[:4]) if data_norm and data_norm[:4].isdigit() else None
        cat_val   = category.group(1).strip() if category else ""

        titulo_opt = extrair_titulo_opcional(texto_val)

        doc = {
            "id":              docno_val,
            "fonte":           fonte,
            "data":            data_norm,
            "ano":             ano_val,
            "categoria":       cat_val,
            "texto":           texto_val,
            "ficheiro_origem": nome_ficheiro,
        }
        # Campo opcional: só incluído quando extraível com confiança razoável
        if titulo_opt:
            doc["titulo_extraido"] = titulo_opt

        documentos.append(doc)

    return documentos


def salvar_lote(lote: list[dict], pasta_saida: Path, numero_lote: int) -> str:
    """Salva um lote de documentos em arquivo JSON numerado."""
    nome = pasta_saida / f"chave_lote_{numero_lote:04d}.json"
    with open(nome, "w", encoding="utf-8") as f:
        json.dump(lote, f, ensure_ascii=False, indent=None, separators=(",", ":"))
    return str(nome)


def processar_zip(
    caminho_zip: str,
    fonte: str,
    pasta_saida: Path,
    tamanho_lote: int,
    lote_atual: list,
    contador_lotes: list,   # usa lista para simular referência mutável
    total_docs: list,
    total_descartados: list,
) -> None:
    """Percorre um ZIP, processa cada SGML e acumula documentos em lotes."""
    extensoes_validas = {".sgml", ".SGML"}

    with zipfile.ZipFile(caminho_zip, "r") as zf:
        nomes = [n for n in zf.namelist()
                 if Path(n).suffix in extensoes_validas and not n.endswith("/")]
        nomes.sort()
        total_arquivos = len(nomes)

        print(f"\n[{fonte}] {total_arquivos} arquivos SGML encontrados em {caminho_zip}")

        for i, nome in enumerate(nomes, 1):
            if i % 50 == 0 or i == total_arquivos:
                print(f"  [{fonte}] Processando {i}/{total_arquivos} — "
                      f"docs acumulados: {total_docs[0]}", end="\r")

            try:
                conteudo = zf.read(nome)
            except Exception as e:
                print(f"\n  AVISO: erro ao ler {nome}: {e}")
                total_descartados[0] += 1
                continue

            docs = processar_sgml(conteudo, fonte, Path(nome).name)

            # Documentos sem DOCNO ou TEXT já foram filtrados em processar_sgml
            total_descartados[0] += 0  # contador explícito se necessário

            for doc in docs:
                lote_atual.append(doc)
                total_docs[0] += 1

                if len(lote_atual) >= tamanho_lote:
                    arq = salvar_lote(lote_atual, pasta_saida, contador_lotes[0])
                    print(f"\n  -> Lote {contador_lotes[0]:04d} salvo: "
                          f"{len(lote_atual)} docs em {arq}")
                    lote_atual.clear()
                    contador_lotes[0] += 1

    print()  # nova linha após o \r


def main():
    parser = argparse.ArgumentParser(
        description="Pré-processamento CHAVE SGML → JSON para Meilisearch"
    )
    parser.add_argument("--publico", required=True,
                        help="Caminho para CHAVEPublico.zip")
    parser.add_argument("--folha",   required=True,
                        help="Caminho para CHAVEFolha.zip")
    parser.add_argument("--saida",   default="./json_lotes",
                        help="Pasta de saída para os arquivos JSON (padrão: ./json_lotes)")
    parser.add_argument("--lote",    type=int, default=5000,
                        help="Número de documentos por lote JSON (padrão: 5000)")
    args = parser.parse_args()

    pasta_saida = Path(args.saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)

    # Contadores partilhados entre as chamadas dos dois ZIPs
    lote_atual        = []
    contador_lotes    = [1]
    total_docs        = [0]
    total_descartados = [0]

    # Processar Público
    processar_zip(
        caminho_zip=args.publico,
        fonte="Publico",
        pasta_saida=pasta_saida,
        tamanho_lote=args.lote,
        lote_atual=lote_atual,
        contador_lotes=contador_lotes,
        total_docs=total_docs,
        total_descartados=total_descartados,
    )

    # Processar Folha de São Paulo
    processar_zip(
        caminho_zip=args.folha,
        fonte="Folha",
        pasta_saida=pasta_saida,
        tamanho_lote=args.lote,
        lote_atual=lote_atual,
        contador_lotes=contador_lotes,
        total_docs=total_docs,
        total_descartados=total_descartados,
    )

    # Salvar lote final (documentos que não completaram um lote inteiro)
    if lote_atual:
        arq = salvar_lote(lote_atual, pasta_saida, contador_lotes[0])
        print(f"\n-> Lote final {contador_lotes[0]:04d} salvo: "
              f"{len(lote_atual)} docs em {arq}")
        contador_lotes[0] += 1

    total_lotes = contador_lotes[0] - 1

    print("\n" + "=" * 60)
    print("PRÉ-PROCESSAMENTO CONCLUÍDO")
    print(f"  Documentos extraídos : {total_docs[0]}")
    print(f"  Arquivos JSON gerados: {total_lotes}")
    print(f"  Pasta de saída       : {pasta_saida.resolve()}")
    print("=" * 60)

    # Salvar relatório de execução para registro no relatório acadêmico
    relatorio = {
        "total_documentos_extraidos": total_docs[0],
        "total_lotes_json":           total_lotes,
        "tamanho_lote_configurado":   args.lote,
        "fontes_processadas":         ["Publico", "Folha"],
        "pasta_saida":                str(pasta_saida.resolve()),
        "codificacao_entrada":        "ISO-8859-1",
        "codificacao_saida":          "UTF-8",
        "campos_obrigatorios":        ["id", "fonte", "data", "ano",
                                       "categoria", "texto", "ficheiro_origem"],
        "campos_opcionais":           ["titulo_extraido"],
    }
    rel_path = pasta_saida / "relatorio_preprocessamento.json"
    with open(rel_path, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    print(f"\nRelatório de execução salvo em: {rel_path}")


if __name__ == "__main__":
    main()
