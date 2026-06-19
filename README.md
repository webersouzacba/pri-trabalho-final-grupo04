# PRI 2025/2026 — Trabalho Final — Grupo 04

**Pesquisa e Recuperação de Informação**  
Mestrado em Engenharia Informática e Tecnologia Web (MEIW)  
Universidade Aberta / UTAD — Ano letivo 2025/2026

---

## Descrição

Este repositório contém os artefactos técnicos do Trabalho Final da unidade curricular de Pesquisa e Recuperação de Informação (PRI). O trabalho consiste na indexação da **Coleção CHAVE** — corpus jornalístico em língua portuguesa dos anos de 1994 e 1995 — no motor de busca **Meilisearch v1.13.0**, e na avaliação do sistema com as **200 questões do QA@CLEF 2008 (PT-PT)**.

O trabalho dá continuidade direta ao **Trabalho B** do mesmo grupo, no qual o Meilisearch foi instalado, configurado e avaliado com o corpus de filmes disponibilizado pela plataforma.

### Grupo 04

| Estudante | Número |
|-----------|--------|
| Weber Marcelo Guirra de Souza | al77734 |
| Mário Nogueira | al2501476 |
| Saiton Silva | al2501481 |

---

## Resultados Principais

| Métrica | Valor |
|---------|-------|
| Documentos indexados | 210.734 |
| Cobertura global (QA@CLEF 2008) | 99,0% (198/200) |
| Tempo médio de resposta | 71,3 ms |
| Duração total da indexação | ≈ 19 minutos |
| Motor de indexação | Meilisearch v1.13.0 |
| Ambiente de produção | VPS OCI NVMe 2 — AlmaLinux 9.7 — 3,6 GB RAM |
| Endpoint público | http://meilisearch.webersouza.com.br |

---

## Estrutura do Repositório

```
pri-trabalho-final-grupo04/
│
├── README.md                          # Este ficheiro
│
├── corpus/
│   └── README_corpus.md               # Instruções para obter a Coleção CHAVE via Linguateca
│                                      # (os ficheiros SGML não são redistribuíveis)
│
├── scripts/
│   ├── 01_preprocessar_chave.py       # Pré-processamento: SGML → JSON em lotes
│   ├── 02_indexar_chave.py            # Indexação dos lotes JSON no Meilisearch
│   ├── 03_consultas_qa.py             # Consultas QA@CLEF 2008 e exportação de resultados
│   └── resolucao_anaforas.py          # Dicionário de resolução manual de dependências anafóricas
│
├── qa/
│   └── QA-CLEF08-PT-PT_test.xml       # Conjunto de 200 questões QA@CLEF 2008 (PT-PT)
│
├── resultados/
│   ├── resultados_original.csv        # Top-10 documentos para cada pergunta (modo original)
│   ├── resultados_resolvida.csv       # Top-10 documentos para cada pergunta (modo resolvido)
│   ├── metricas.json                  # Métricas de cobertura e tempo dos dois modos
│   ├── relatorio_preprocessamento.json # Estatísticas do pré-processamento do corpus
│   └── relatorio_indexacao.json       # Estatísticas da indexação (tempos por lote, erros)
│
├── avaliacao/
│   └── avaliacao_qualitativa_qa.xlsx  # Planilha de avaliação qualitativa (200 perguntas)
│
└── relatorio/
    └── Trabalho_Final_PRI_Grupo04.pdf # Relatório final em PDF (após submissão)
```

---

## Pré-requisitos

### Pré-processamento local (sua máquina)

- Python 3.6 ou superior
- Apenas biblioteca padrão (sem dependências externas)
- Os ficheiros `CHAVEPublico.zip` e `CHAVEFolha.zip` obtidos via [Linguateca](http://www.linguateca.pt/CHAVE/)

### Indexação e consultas (servidor)

- Meilisearch v1.13.0 instalado e em execução
- Python 3.6 ou superior (apenas biblioteca padrão)
- Acesso SSH ao servidor

---

## Como Utilizar

### 1. Pré-processamento (executa localmente)

Coloque os dois ficheiros ZIP da Coleção CHAVE na mesma pasta que o script e execute:

```bash
python3 scripts/01_preprocessar_chave.py \
    --publico CHAVEPublico.zip \
    --folha   CHAVEFolha.zip \
    --saida   ./json_lotes \
    --lote    5000
```

O script gera ficheiros `chave_lote_NNNN.json` na pasta de saída e um relatório `relatorio_preprocessamento.json` com os totais.

No Windows (PowerShell), use a versão em linha única:

```powershell
python scripts/01_preprocessar_chave.py --publico CHAVEPublico.zip --folha CHAVEFolha.zip --saida ./json_lotes --lote 5000
```

**Saída esperada:** 43 ficheiros JSON, 210.453 documentos extraídos, ≈ 590 MB.

### 2. Transferência para o servidor

```bash
scp -P PORTA -r ./json_lotes/ utilizador@servidor:/opt/pri-trabalho-final/
scp -P PORTA scripts/02_indexar_chave.py utilizador@servidor:/opt/pri-trabalho-final/
scp -P PORTA scripts/03_consultas_qa.py utilizador@servidor:/opt/pri-trabalho-final/
scp -P PORTA scripts/resolucao_anaforas.py utilizador@servidor:/opt/pri-trabalho-final/
scp -P PORTA qa/QA-CLEF08-PT-PT_test.xml utilizador@servidor:/opt/pri-trabalho-final/
```

### 3. Indexação (executa no servidor)

```bash
cd /opt/pri-trabalho-final
python3 02_indexar_chave.py --chave SUA_MASTER_KEY
```

Opções disponíveis:

```
--pasta    Pasta com os ficheiros JSON   (padrão: ./json_lotes)
--host     Endereço do Meilisearch       (padrão: http://localhost:7700)
--chave    Master key do Meilisearch     (obrigatório)
--indice   Nome do índice                (padrão: chave)
```

**Saída esperada:** 210.734 documentos indexados em ≈ 19 minutos, sem erros.

### 4. Consultas QA@CLEF 2008 (executa no servidor)

```bash
python3 03_consultas_qa.py \
    --xml   /opt/pri-trabalho-final/QA-CLEF08-PT-PT_test.xml \
    --chave SUA_MASTER_KEY
```

Opções disponíveis:

```
--xml      Caminho para o ficheiro XML das questões  (obrigatório)
--host     Endereço do Meilisearch                   (padrão: http://localhost:7700)
--chave    Master key do Meilisearch                 (obrigatório)
--indice   Nome do índice                            (padrão: chave)
--topk     Documentos por consulta                   (padrão: 10)
--saida    Pasta de saída para os resultados         (padrão: ./resultados)
```

O script executa as 200 perguntas nos dois modos (original e com anáforas resolvidas) e exibe um quadro comparativo no terminal.

---

## Configuração do Índice Meilisearch

O índice `chave` é criado automaticamente pelo script `02_indexar_chave.py` com a seguinte configuração:

```json
{
  "searchableAttributes": ["texto", "titulo_extraido"],
  "filterableAttributes": ["fonte", "ano", "categoria"],
  "sortableAttributes":   ["data", "ano"],
  "rankingRules": ["words", "typo", "proximity", "attribute", "sort", "exactness"]
}
```

### Estrutura dos Documentos JSON

Cada documento indexado segue o esquema:

```json
{
  "id":              "PUBLICO-19940101-001",
  "fonte":           "Publico",
  "data":            "1994-01-01",
  "ano":             1994,
  "categoria":       "Economia",
  "texto":           "Texto integral do artigo jornalístico...",
  "ficheiro_origem": "ED940101.sgml",
  "titulo_extraido": "Título opcional extraído da primeira linha"
}
```

O campo `titulo_extraido` é opcional, por ausência de marcação SGML consistente de títulos na Coleção CHAVE.

---

## Decisões Metodológicas Relevantes

### Resolução de Dependências Anafóricas

Das 200 perguntas do QA@CLEF 2008, 50 apresentam dependência anafórica — pronomes ou elipses que remetem para referentes de perguntas anteriores do mesmo grupo temático. O ficheiro `resolucao_anaforas.py` documenta a resolução manual aplicada, com classificação de cada caso em:

- **RESOLVIDA** — substituição direta do referente (50 perguntas)
- **PARCIAL** — resolução aproximada com ambiguidade residual documentada (1 pergunta)
- **INALTERADA** — pergunta âncora do grupo, independente (37 perguntas)

### Perguntas sem Resultado

As perguntas q_0031 (*"Quem disse 'alea iacta est'?"*) e q_0187 (*"Quem foi o 'pai do teatro português'?"*) não retornaram resultados em nenhum dos dois modos. A causa identificada foi a presença de aspas duplas no texto da query, que o Meilisearch interpretou como operador de busca por frase exata. A sanitização prévia das queries eliminaria este comportamento.

### Codificação do Corpus

Os ficheiros SGML da Coleção CHAVE estão codificados em ISO-8859-1. A conversão para UTF-8 é realizada automaticamente pelo script de pré-processamento durante a extração.

---

## Infraestrutura

| Componente | Especificação |
|------------|---------------|
| Servidor | VPS OCI NVMe 2 |
| Sistema Operativo | AlmaLinux 9.7 |
| RAM | 3,6 GB |
| Disco | 50 GB NVMe |
| Motor de busca | Meilisearch v1.13.0 |
| Endpoint público | http://meilisearch.webersouza.com.br |
| Porta | 7700 (via proxy Nginx) |

---

## Referências

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to information retrieval*. Cambridge University Press.
- Baeza-Yates, R., & Ribeiro-Neto, B. (2011). *Modern information retrieval* (2nd ed.). Addison-Wesley.
- Santos, D., & Rocha, P. (2005). The key to the first question answering system in Portuguese: QA@CLEF 2004. In *Proceedings of CLEF 2004* (pp. 453–464). Springer.
- Forner, P., et al. (2009). Overview of the CLEF 2008 multilingual question answering track. In *Multilingual Information Access Evaluation I* (pp. 262–295). Springer.
- Meilisearch. (2024). *Meilisearch documentation (v1.13)*. https://www.meilisearch.com/docs

---

## Licença

Os scripts deste repositório são disponibilizados para fins académicos no contexto da UC de PRI do MEIW — Universidade Aberta / UTAD.

A Coleção CHAVE é propriedade da Linguateca e está sujeita às suas condições de uso. Os resultados obtidos fora das avaliações oficiais CLEF não devem ser apresentados como avaliação oficial CLEF.
