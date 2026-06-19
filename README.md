# Indexação da Coleção CHAVE e Avaliação com QA@CLEF 2008

**Unidade Curricular:** Pesquisa e Recuperação de Informação (PRI)  
**Programa:** Mestrado em Engenharia Informática e Tecnologia Web (MEIW)  
**Instituição:** Universidade Aberta / UTAD  
**Ano letivo:** 2025/2026

---

## Sobre o trabalho

Este repositório documenta o Trabalho Final da unidade curricular de Pesquisa e Recuperação de Informação, realizado pelo Grupo 04. O trabalho consiste na construção de um sistema de recuperação de informação sobre a **Coleção CHAVE** — corpus jornalístico em língua portuguesa dos anos de 1994 e 1995 — e na sua avaliação com as **200 questões do QA@CLEF 2008** em português europeu.

O sistema foi construído sobre o motor de indexação **Meilisearch v1.13.0**, cuja instalação, configuração e validação inicial foram realizadas no Trabalho B da mesma unidade curricular. O Trabalho Final estende esse trabalho anterior com um corpus de escala real e um protocolo de avaliação baseado num benchmark estabelecido na literatura de recuperação de informação em língua portuguesa.

### Grupo 04

| Estudante | Número de aluno |
|-----------|----------------|
| Weber Marcelo Guirra de Souza | al77734 |
| Mário Nogueira | al2501476 |
| Saiton Silva | al2501481 |

**Orientadores:** Prof. Vitor Rocio (Universidade Aberta) · Prof. António Jorge Gouveia (UTAD)

---

## Resultados principais

O sistema indexou 210.734 artigos jornalísticos extraídos da Coleção CHAVE e respondeu às 200 questões do QA@CLEF 2008 com uma cobertura global de 99,0%, num tempo médio de resposta de 71 ms por consulta.

| Indicador | Valor |
|-----------|-------|
| Corpus indexado | Coleção CHAVE (Público + Folha de São Paulo, 1994–1995) |
| Documentos indexados | 210.734 artigos jornalísticos |
| Questões avaliadas | 200 (QA@CLEF 2008, PT-PT) |
| Cobertura global | 99,0% (198 de 200 questões com resultado) |
| Tempo médio de resposta | 71,3 ms por consulta |
| Duração da indexação | 19 minutos (1.138 segundos) |
| Motor de indexação | Meilisearch v1.13.0 |
| Endpoint público | http://meilisearch.webersouza.com.br |

---

## Corpus e dados de avaliação

A **Coleção CHAVE** foi compilada pela [Linguateca](http://www.linguateca.pt/CHAVE/) no âmbito das avaliações CLEF (*Cross-Language Evaluation Forum*) e constitui o principal recurso de avaliação de sistemas de recuperação de informação em língua portuguesa. Inclui edições integrais de dois jornais lusófonos: o **Público** (Portugal) e a **Folha de São Paulo** (Brasil), cobrindo os anos de 1994 e 1995.

Por restrições de direitos de uso, os ficheiros do corpus não são redistribuíveis e não estão incluídos neste repositório. A pasta `corpus/` contém instruções para solicitar acesso à Linguateca.

As **questões de avaliação** provêm do conjunto de teste do QA@CLEF 2008 para português europeu (`qa/QA-CLEF08-PT-PT_test.xml`), composto por 200 perguntas factuais em linguagem natural, organizadas em grupos temáticos. Os resultados obtidos neste trabalho não constituem avaliação oficial CLEF.

---

## Pipeline técnico

O trabalho implementa um pipeline de três fases, cada uma documentada num script Python independente que usa apenas a biblioteca padrão da linguagem.

### Fase 1 — Pré-processamento (`scripts/01_preprocessar_chave.py`)

Extrai os artigos dos ficheiros SGML da Coleção CHAVE, converte a codificação de ISO-8859-1 para UTF-8 e serializa o resultado em ficheiros JSON em lotes de 5.000 documentos. O processo gerou 43 ficheiros JSON a partir de 1.456 ficheiros SGML, sem dependências externas.

Cada documento é representado pelo seguinte esquema:

```json
{
  "id":              "PUBLICO-19940101-001",
  "fonte":           "Publico",
  "data":            "1994-01-01",
  "ano":             1994,
  "categoria":       "Economia",
  "texto":           "Texto integral do artigo...",
  "ficheiro_origem": "ED940101.sgml",
  "titulo_extraido": "Título opcional (primeira linha do texto, quando identificável)"
}
```

O campo `titulo_extraido` é tratado como atributo opcional, por ausência de marcação SGML consistente de títulos na coleção.

### Fase 2 — Indexação (`scripts/02_indexar_chave.py`)

Configura o índice `chave` no Meilisearch e envia os lotes JSON sequencialmente via API REST, aguardando a confirmação de cada tarefa assíncrona antes de avançar. A configuração do índice reflete as decisões metodológicas do grupo:

| Parâmetro | Configuração |
|-----------|-------------|
| `searchableAttributes` | `texto`, `titulo_extraido` |
| `filterableAttributes` | `fonte`, `ano`, `categoria` |
| `sortableAttributes` | `data`, `ano` |
| `rankingRules` | Configuração padrão Meilisearch v1.13.0 |

### Fase 3 — Consultas e avaliação (`scripts/03_consultas_qa.py`)

Executa as 200 questões do QA@CLEF 2008 em dois modos distintos. No **modo original**, as perguntas são submetidas ao sistema exatamente como constam no ficheiro XML. No **modo resolvido**, as perguntas com dependência anafórica são expandidas com o referente explícito, conforme o dicionário de resoluções em `scripts/resolucao_anaforas.py`. Os resultados de ambos os modos são exportados em CSV para análise comparativa.

---

## Tratamento de dependências anafóricas

Das 200 questões do conjunto de teste, 88 integram grupos temáticos com dependência contextual entre perguntas consecutivas. O ficheiro `scripts/resolucao_anaforas.py` documenta a resolução manual aplicada a cada caso, com classificação explícita:

- **RESOLVIDA** (50 perguntas): substituição direta do pronome ou elipse pelo referente nominal da pergunta âncora do grupo — por exemplo, *"Quando é que ele foi criado?"* torna-se *"Quando é que Tintin foi criado?"*
- **PARCIAL** (1 pergunta): resolução aproximada com ambiguidade residual documentada
- **INALTERADA** (37 perguntas): pergunta âncora do grupo, independente por natureza

A comparação entre os dois modos de consulta constitui um dos eixos de análise do relatório.

---

## Estrutura do repositório

```
pri-trabalho-final-grupo04/
│
├── README.md
│
├── scripts/
│   ├── 01_preprocessar_chave.py       # Pré-processamento: SGML → JSON
│   ├── 02_indexar_chave.py            # Indexação no Meilisearch
│   ├── 03_consultas_qa.py             # Consultas e exportação de resultados
│   └── resolucao_anaforas.py          # Resoluções anafóricas documentadas
│
├── qa/
│   └── QA-CLEF08-PT-PT_test.xml       # 200 questões QA@CLEF 2008 (PT-PT)
│
├── corpus/
│   └── README_corpus.md               # Instruções para obter a Coleção CHAVE
│
├── resultados/
│   ├── resultados_original.csv        # Top-10 por pergunta — modo original
│   ├── resultados_resolvida.csv       # Top-10 por pergunta — modo resolvido
│   ├── metricas.json                  # Métricas de cobertura e tempo
│   ├── relatorio_preprocessamento.json
│   └── relatorio_indexacao.json
│
└── avaliacao/
    └── avaliacao_qualitativa_qa.xlsx  # Planilha de avaliação qualitativa manual
```

---

## Referências

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to information retrieval*. Cambridge University Press.
- Baeza-Yates, R., & Ribeiro-Neto, B. (2011). *Modern information retrieval* (2nd ed.). Addison-Wesley.
- Santos, D., & Rocha, P. (2005). The key to the first question answering system in Portuguese: QA@CLEF 2004. In *Proceedings of CLEF 2004* (pp. 453–464). Springer.
- Forner, P., et al. (2009). Overview of the CLEF 2008 multilingual question answering track. In *Multilingual Information Access Evaluation I* (pp. 262–295). Springer.
- Meilisearch. (2024). *Meilisearch documentation (v1.13)*. https://www.meilisearch.com/docs

---

*Os resultados obtidos neste trabalho não constituem avaliação oficial CLEF. A Coleção CHAVE é propriedade da Linguateca e está sujeita às suas condições de uso.*
