# =============================================================================
# RESOLUÇÃO MANUAL DE PERGUNTAS ANAFÓRICAS — QA@CLEF 2008 PT-PT
# Trabalho Final PRI 2025/2026 — Grupo 04
#
# Critérios aplicados:
# 1. Substituição direta: pronome ou elipse substituído pelo referente explícito
#    da pergunta anterior do mesmo grupo.
# 2. Expansão estrutural: perguntas do tipo "E X?" expandidas para a estrutura
#    completa da pergunta anterior, substituindo apenas o elemento variável.
# 3. Casos sem resolução possível: marcados como INALTERADA com justificativa.
#    São perguntas que, mesmo com o contexto do grupo, não têm referente
#    textual que possa ser inserido na query sem introduzir viés indevido.
#
# Classificação dos grupos:
# - RESOLVIDA: pergunta dependente foi expandida com referente explícito
# - PARCIAL: resolução aproximada; ambiguidade residual documentada
# - INALTERADA: pergunta isolável ou sem dependência lexical relevante
# =============================================================================

RESOLUCOES = {

    # -------------------------------------------------------------------------
    # Grupo 2601 — Tintin
    # -------------------------------------------------------------------------
    "0002": {
        "original":  "Quem foi o criador de Tintin?",
        "resolvida": "Quem foi o criador de Tintin?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora do grupo. Independente."
    },
    "0003": {
        "original":  "Quando é que ele foi criado?",
        "resolvida": "Quando é que Tintin foi criado?",
        "tipo": "RESOLVIDA",
        "nota": "'ele' refere-se a Tintin, criado por Hergé."
    },
    "0004": {
        "original":  "Como se chama o cão dele?",
        "resolvida": "Como se chama o cão do Tintin?",
        "tipo": "RESOLVIDA",
        "nota": "'dele' refere-se a Tintin."
    },
    "0005": {
        "original":  "De que raça é o cão?",
        "resolvida": "De que raça é o cão do Tintin?",
        "tipo": "RESOLVIDA",
        "nota": "Referência ao cão de Tintin (Milu/Milou)."
    },

    # -------------------------------------------------------------------------
    # Grupo 2607 — Montanha mais alta
    # -------------------------------------------------------------------------
    "0011": {
        "original":  "Qual é a montanha mais alta do México?",
        "resolvida": "Qual é a montanha mais alta do México?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0012": {
        "original":  "E do Japão?",
        "resolvida": "Qual é a montanha mais alta do Japão?",
        "tipo": "RESOLVIDA",
        "nota": "Expansão da estrutura 'Qual é a montanha mais alta de X?'."
    },

    # -------------------------------------------------------------------------
    # Grupo 2615 — Thomas Mann
    # -------------------------------------------------------------------------
    "0020": {
        "original":  "Quando nasceu Thomas Mann?",
        "resolvida": "Quando nasceu Thomas Mann?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0021": {
        "original":  "E quando morreu?",
        "resolvida": "Quando morreu Thomas Mann?",
        "tipo": "RESOLVIDA",
        "nota": "Expansão com referente explícito Thomas Mann."
    },

    # -------------------------------------------------------------------------
    # Grupo 2618 — Álvaro de Campos
    # -------------------------------------------------------------------------
    "0024": {
        "original":  "Quem foi Álvaro de Campos?",
        "resolvida": "Quem foi Álvaro de Campos?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0025": {
        "original":  "Diga uma das suas obras.",
        "resolvida": "Diga uma das obras de Álvaro de Campos.",
        "tipo": "RESOLVIDA",
        "nota": "'suas' refere-se a Álvaro de Campos."
    },

    # -------------------------------------------------------------------------
    # Grupo 2624 — Júlio César / alea iacta est
    # -------------------------------------------------------------------------
    "0031": {
        "original":  "Quem disse \"alea iacta est\"?",
        "resolvida": "Quem disse \"alea iacta est\"?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0032": {
        "original":  "Ao atravessar que rio?",
        "resolvida": "Que rio atravessou Júlio César ao dizer alea iacta est?",
        "tipo": "RESOLVIDA",
        "nota": "Referente implícito é Júlio César cruzando o Rubicão."
    },

    # -------------------------------------------------------------------------
    # Grupo 2628 — Elementos químicos
    # -------------------------------------------------------------------------
    "0036": {
        "original":  "Diga um gás nobre.",
        "resolvida": "Diga um gás nobre.",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora. Independente."
    },
    "0037": {
        "original":  "E um não-metal",
        "resolvida": "Diga um elemento não-metal.",
        "tipo": "RESOLVIDA",
        "nota": "Expansão da estrutura 'Diga um X'."
    },

    # -------------------------------------------------------------------------
    # Grupo 2639 — Pato Donald
    # -------------------------------------------------------------------------
    "0048": {
        "original":  "Quem são os sobrinhos do Pato Donald?",
        "resolvida": "Quem são os sobrinhos do Pato Donald?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0049": {
        "original":  "E a namorada dele?",
        "resolvida": "Quem é a namorada do Pato Donald?",
        "tipo": "RESOLVIDA",
        "nota": "'dele' refere-se ao Pato Donald."
    },
    "0050": {
        "original":  "Qual a profissão dele?",
        "resolvida": "Qual a profissão do Pato Donald?",
        "tipo": "RESOLVIDA",
        "nota": "'dele' refere-se ao Pato Donald."
    },

    # -------------------------------------------------------------------------
    # Grupo 2643 — Queijo feta
    # -------------------------------------------------------------------------
    "0054": {
        "original":  "O que é o feta?",
        "resolvida": "O que é o feta?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0055": {
        "original":  "De que país é originário?",
        "resolvida": "De que país é originário o queijo feta?",
        "tipo": "RESOLVIDA",
        "nota": "Referente é o queijo feta."
    },

    # -------------------------------------------------------------------------
    # Grupo 2648 — Ossétia
    # -------------------------------------------------------------------------
    "0060": {
        "original":  "Em que país fica a Ossétia do Norte?",
        "resolvida": "Em que país fica a Ossétia do Norte?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0061": {
        "original":  "E a Ossétia do Sul?",
        "resolvida": "Em que país fica a Ossétia do Sul?",
        "tipo": "RESOLVIDA",
        "nota": "Expansão da estrutura 'Em que país fica X?'."
    },

    # -------------------------------------------------------------------------
    # Grupo 2651 — Santos padroeiros
    # -------------------------------------------------------------------------
    "0064": {
        "original":  "Quem é o santo patrono dos cervejeiros?",
        "resolvida": "Quem é o santo patrono dos cervejeiros?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0065": {
        "original":  "E do pão?",
        "resolvida": "Quem é o santo patrono do pão?",
        "tipo": "RESOLVIDA",
        "nota": "Expansão da estrutura 'Quem é o santo patrono de X?'."
    },

    # -------------------------------------------------------------------------
    # Grupo 2653 — Milhafre-preto
    # -------------------------------------------------------------------------
    "0067": {
        "original":  "Qual a envergadura de um milhafre-preto?",
        "resolvida": "Qual a envergadura de um milhafre-preto?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0068": {
        "original":  "Quanto é que ele pesa?",
        "resolvida": "Quanto pesa um milhafre-preto?",
        "tipo": "RESOLVIDA",
        "nota": "'ele' refere-se ao milhafre-preto."
    },
    "0069": {
        "original":  "Que tipo de ave é?",
        "resolvida": "Que tipo de ave é o milhafre-preto?",
        "tipo": "RESOLVIDA",
        "nota": "Referente é o milhafre-preto."
    },

    # -------------------------------------------------------------------------
    # Grupo 2658 — Berlim
    # -------------------------------------------------------------------------
    "0074": {
        "original":  "Quantos habitantes tinha Berlim em 1850?",
        "resolvida": "Quantos habitantes tinha Berlim em 1850?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0075": {
        "original":  "Quantos tem hoje em dia?",
        "resolvida": "Quantos habitantes tem Berlim hoje em dia?",
        "tipo": "RESOLVIDA",
        "nota": "Referente é Berlim; 'hoje em dia' mantido como contexto temporal."
    },

    # -------------------------------------------------------------------------
    # Grupo 2659 — ICCROM
    # -------------------------------------------------------------------------
    "0076": {
        "original":  "O que é o ICCROM?",
        "resolvida": "O que é o ICCROM?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0077": {
        "original":  "Quantos estados membros tinha em 1995?",
        "resolvida": "Quantos estados membros tinha o ICCROM em 1995?",
        "tipo": "RESOLVIDA",
        "nota": "Referente é o ICCROM."
    },
    "0078": {
        "original":  "Onde tem a sua sede?",
        "resolvida": "Onde fica a sede do ICCROM?",
        "tipo": "RESOLVIDA",
        "nota": "Referente é o ICCROM."
    },

    # -------------------------------------------------------------------------
    # Grupo 2662 — Último rei de Portugal
    # -------------------------------------------------------------------------
    "0081": {
        "original":  "Quem foi o último rei de Portugal?",
        "resolvida": "Quem foi o último rei de Portugal?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0082": {
        "original":  "Em que período foi ele rei?",
        "resolvida": "Em que período foi Manuel II rei de Portugal?",
        "tipo": "RESOLVIDA",
        "nota": "Referente é Manuel II, último rei de Portugal."
    },
    "0083": {
        "original":  "Em que barco ele embarcou para o exílio?",
        "resolvida": "Em que barco Manuel II embarcou para o exílio?",
        "tipo": "RESOLVIDA",
        "nota": "Referente é Manuel II."
    },

    # -------------------------------------------------------------------------
    # Grupo 2664 — Lula
    # -------------------------------------------------------------------------
    "0085": {
        "original":  "Quantos votos teve o Lula nas eleições presidenciais de 2002?",
        "resolvida": "Quantos votos teve o Lula nas eleições presidenciais de 2002?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0086": {
        "original":  "Quando é que ele tomou posse?",
        "resolvida": "Quando é que Lula tomou posse como presidente do Brasil?",
        "tipo": "RESOLVIDA",
        "nota": "'ele' refere-se a Lula."
    },

    # -------------------------------------------------------------------------
    # Grupo 2667 — Livro da Selva
    # -------------------------------------------------------------------------
    "0089": {
        "original":  "Quem escreveu o Livro da Selva?",
        "resolvida": "Quem escreveu o Livro da Selva?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0090": {
        "original":  "Quem é a personagem principal do livro?",
        "resolvida": "Quem é a personagem principal do Livro da Selva?",
        "tipo": "RESOLVIDA",
        "nota": "'o livro' refere-se ao Livro da Selva."
    },

    # -------------------------------------------------------------------------
    # Grupo 2671 — Estados dos EUA
    # -------------------------------------------------------------------------
    "0094": {
        "original":  "Qual é o 31º estado dos Estados Unidos?",
        "resolvida": "Qual é o 31º estado dos Estados Unidos?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0095": {
        "original":  "E o 37º?",
        "resolvida": "Qual é o 37º estado dos Estados Unidos?",
        "tipo": "RESOLVIDA",
        "nota": "Expansão da estrutura 'Qual é o Nº estado dos Estados Unidos?'."
    },

    # -------------------------------------------------------------------------
    # Grupo 2673 — Jogos Olímpicos 1976
    # -------------------------------------------------------------------------
    "0097": {
        "original":  "Quantos atletas participaram nos Jogos Olímpicos de 1976?",
        "resolvida": "Quantos atletas participaram nos Jogos Olímpicos de 1976?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0098": {
        "original":  "Em que país se realizaram?",
        "resolvida": "Em que país se realizaram os Jogos Olímpicos de 1976?",
        "tipo": "RESOLVIDA",
        "nota": "Referente são os Jogos Olímpicos de 1976."
    },
    "0099": {
        "original":  "E em que cidade?",
        "resolvida": "Em que cidade se realizaram os Jogos Olímpicos de 1976?",
        "tipo": "RESOLVIDA",
        "nota": "Expansão com referente explícito."
    },

    # -------------------------------------------------------------------------
    # Grupo 2681 — Cazaquistão
    # -------------------------------------------------------------------------
    "0107": {
        "original":  "Qual é a capital do Cazaquistão?",
        "resolvida": "Qual é a capital do Cazaquistão?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0108": {
        "original":  "E a sua maior cidade?",
        "resolvida": "Qual é a maior cidade do Cazaquistão?",
        "tipo": "RESOLVIDA",
        "nota": "'sua' refere-se ao Cazaquistão."
    },

    # -------------------------------------------------------------------------
    # Grupo 2682 — Presidente da Guatemala
    # -------------------------------------------------------------------------
    "0109": {
        "original":  "Quem é o actual presidente da Guatemala?",
        "resolvida": "Quem é o actual presidente da Guatemala?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0110": {
        "original":  "Qual era o cargo dele em 1991?",
        "resolvida": "Qual era o cargo do presidente da Guatemala em 1991?",
        "tipo": "PARCIAL",
        "nota": "Resolução aproximada; o referente exato depende de quem era presidente em 2008."
    },

    # -------------------------------------------------------------------------
    # Grupo 2692 — Joana de Arc
    # -------------------------------------------------------------------------
    "0120": {
        "original":  "Em que guerra combateu Joana de Arc?",
        "resolvida": "Em que guerra combateu Joana de Arc?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0121": {
        "original":  "Onde é que ela foi queimada?",
        "resolvida": "Onde é que Joana de Arc foi queimada?",
        "tipo": "RESOLVIDA",
        "nota": "'ela' refere-se a Joana de Arc."
    },
    "0122": {
        "original":  "Quando?",
        "resolvida": "Quando foi queimada Joana de Arc?",
        "tipo": "RESOLVIDA",
        "nota": "Pergunta de uma palavra; contexto é a execução de Joana de Arc."
    },
    "0123": {
        "original":  "Que idade tinha ela?",
        "resolvida": "Que idade tinha Joana de Arc quando foi queimada?",
        "tipo": "RESOLVIDA",
        "nota": "'ela' refere-se a Joana de Arc."
    },

    # -------------------------------------------------------------------------
    # Grupo 2693 — Fidel Castro
    # -------------------------------------------------------------------------
    "0124": {
        "original":  "Desde quando está Fidel Castro no poder?",
        "resolvida": "Desde quando está Fidel Castro no poder?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0125": {
        "original":  "Quando é que ele nasceu?",
        "resolvida": "Quando é que Fidel Castro nasceu?",
        "tipo": "RESOLVIDA",
        "nota": "'ele' refere-se a Fidel Castro."
    },
    "0126": {
        "original":  "Quem é o irmão dele?",
        "resolvida": "Quem é o irmão de Fidel Castro?",
        "tipo": "RESOLVIDA",
        "nota": "'dele' refere-se a Fidel Castro."
    },

    # -------------------------------------------------------------------------
    # Grupo 2703 — Prémio Cervantes
    # -------------------------------------------------------------------------
    "0136": {
        "original":  "Qual a dotação do Prémio Cervantes?",
        "resolvida": "Qual a dotação do Prémio Cervantes?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0137": {
        "original":  "Quem é que ganhou o prémio em 1994?",
        "resolvida": "Quem ganhou o Prémio Cervantes em 1994?",
        "tipo": "RESOLVIDA",
        "nota": "'o prémio' refere-se ao Prémio Cervantes."
    },

    # -------------------------------------------------------------------------
    # Grupo 2709 — Mulheres no espaço
    # -------------------------------------------------------------------------
    "0143": {
        "original":  "Quem foi a primeira mulher no espaço?",
        "resolvida": "Quem foi a primeira mulher no espaço?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0144": {
        "original":  "E a segunda?",
        "resolvida": "Quem foi a segunda mulher no espaço?",
        "tipo": "RESOLVIDA",
        "nota": "Expansão da estrutura 'Quem foi a Nª mulher no espaço?'."
    },

    # -------------------------------------------------------------------------
    # Grupo 2712 — Vasco da Gama (clube)
    # -------------------------------------------------------------------------
    "0147": {
        "original":  "Quando foi fundado o Vasco da Gama?",
        "resolvida": "Quando foi fundado o Vasco da Gama?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0148": {
        "original":  "Por quem foi fundado?",
        "resolvida": "Por quem foi fundado o Vasco da Gama?",
        "tipo": "RESOLVIDA",
        "nota": "Referente é o clube Vasco da Gama."
    },

    # -------------------------------------------------------------------------
    # Grupo 2713 — Vasco da Gama (navegador)
    # -------------------------------------------------------------------------
    "0149": {
        "original":  "Quando nasceu Vasco da Gama?",
        "resolvida": "Quando nasceu Vasco da Gama?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0150": {
        "original":  "Onde é que ele morreu?",
        "resolvida": "Onde é que Vasco da Gama morreu?",
        "tipo": "RESOLVIDA",
        "nota": "'ele' refere-se a Vasco da Gama."
    },

    # -------------------------------------------------------------------------
    # Grupo 2719 — Carl Barks
    # -------------------------------------------------------------------------
    "0156": {
        "original":  "Quem foi Carl Barks?",
        "resolvida": "Quem foi Carl Barks?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0157": {
        "original":  "Onde é que ele nasceu?",
        "resolvida": "Onde é que Carl Barks nasceu?",
        "tipo": "RESOLVIDA",
        "nota": "'ele' refere-se a Carl Barks."
    },
    "0158": {
        "original":  "Quem eram os pais dele?",
        "resolvida": "Quem eram os pais de Carl Barks?",
        "tipo": "RESOLVIDA",
        "nota": "'dele' refere-se a Carl Barks."
    },

    # -------------------------------------------------------------------------
    # Grupo 2722 — Jean Vigo
    # -------------------------------------------------------------------------
    "0161": {
        "original":  "Quantos filmes realizou Jean Vigo?",
        "resolvida": "Quantos filmes realizou Jean Vigo?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0162": {
        "original":  "Diga um desses filmes.",
        "resolvida": "Diga um filme realizado por Jean Vigo.",
        "tipo": "RESOLVIDA",
        "nota": "'desses filmes' refere-se aos filmes de Jean Vigo."
    },

    # -------------------------------------------------------------------------
    # Grupo 2725 — Pearl Harbor
    # -------------------------------------------------------------------------
    "0165": {
        "original":  "Que navio americano foi afundado em Pearl Harbor in 1941?",
        "resolvida": "Que navio americano foi afundado em Pearl Harbor em 1941?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora. Corrigido 'in' para 'em'."
    },
    "0166": {
        "original":  "E que navio japonês?",
        "resolvida": "Que navio japonês foi afundado em Pearl Harbor em 1941?",
        "tipo": "RESOLVIDA",
        "nota": "Expansão da estrutura da pergunta anterior."
    },

    # -------------------------------------------------------------------------
    # Grupo 2727 — Clubes de futebol
    # -------------------------------------------------------------------------
    "0168": {
        "original":  "Diga um clube de futebol de Campinas.",
        "resolvida": "Diga um clube de futebol de Campinas.",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0169": {
        "original":  "E um de Belo Horizonte.",
        "resolvida": "Diga um clube de futebol de Belo Horizonte.",
        "tipo": "RESOLVIDA",
        "nota": "Expansão da estrutura 'Diga um clube de futebol de X'."
    },

    # -------------------------------------------------------------------------
    # Grupo 2729 — Elizabeth Taylor
    # -------------------------------------------------------------------------
    "0171": {
        "original":  "Quem foi o oitavo marido de Elizabeth Taylor?",
        "resolvida": "Quem foi o oitavo marido de Elizabeth Taylor?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0172": {
        "original":  "Quando é que eles se casaram?",
        "resolvida": "Quando é que Elizabeth Taylor e o seu oitavo marido se casaram?",
        "tipo": "RESOLVIDA",
        "nota": "'eles' refere-se a Elizabeth Taylor e o oitavo marido."
    },
    "0173": {
        "original":  "Qual é a nacionalidade dela?",
        "resolvida": "Qual é a nacionalidade de Elizabeth Taylor?",
        "tipo": "RESOLVIDA",
        "nota": "'dela' refere-se a Elizabeth Taylor."
    },

    # -------------------------------------------------------------------------
    # Grupo 2730 — Géneros gramaticais
    # -------------------------------------------------------------------------
    "0174": {
        "original":  "Quantos gêneros tem o alemão?",
        "resolvida": "Quantos gêneros tem o alemão?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0175": {
        "original":  "E quantos tem o romanche?",
        "resolvida": "Quantos gêneros gramaticais tem o romanche?",
        "tipo": "RESOLVIDA",
        "nota": "Expansão com o conceito de gêneros gramaticais."
    },

    # -------------------------------------------------------------------------
    # Grupo 2731 — Ramsés II
    # -------------------------------------------------------------------------
    "0176": {
        "original":  "Quanto tempo reinou Ramsés II?",
        "resolvida": "Quanto tempo reinou Ramsés II?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0177": {
        "original":  "Quando começou o seu reinado?",
        "resolvida": "Quando começou o reinado de Ramsés II?",
        "tipo": "RESOLVIDA",
        "nota": "'seu' refere-se a Ramsés II."
    },
    "0178": {
        "original":  "Ele ordenou a construção de que templos?",
        "resolvida": "Que templos ordenou Ramsés II construir?",
        "tipo": "RESOLVIDA",
        "nota": "'Ele' refere-se a Ramsés II."
    },

    # -------------------------------------------------------------------------
    # Grupo 2733 — Ópera Aida
    # -------------------------------------------------------------------------
    "0180": {
        "original":  "Quantos actos tem a ópera Verdi da Aida?",
        "resolvida": "Quantos actos tem a ópera Aida de Verdi?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora. Leve reordenação para clareza."
    },
    "0181": {
        "original":  "Quem escreveu o libretto dessa ópera?",
        "resolvida": "Quem escreveu o libretto da ópera Aida?",
        "tipo": "RESOLVIDA",
        "nota": "'dessa ópera' refere-se à Aida."
    },
    "0182": {
        "original":  "Quando é que estreou a ópera?",
        "resolvida": "Quando é que estreou a ópera Aida?",
        "tipo": "RESOLVIDA",
        "nota": "Referente é a Aida."
    },

    # -------------------------------------------------------------------------
    # Grupo 2739 — Parque Estadual Guariba
    # -------------------------------------------------------------------------
    "0188": {
        "original":  "Qual a área do Parque Estadual Guariba?",
        "resolvida": "Qual a área do Parque Estadual Guariba?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0189": {
        "original":  "Quando foi criado o parque?",
        "resolvida": "Quando foi criado o Parque Estadual Guariba?",
        "tipo": "RESOLVIDA",
        "nota": "'o parque' refere-se ao Parque Estadual Guariba."
    },

    # -------------------------------------------------------------------------
    # Grupo 2740 — Torre do Tombo
    # -------------------------------------------------------------------------
    "0190": {
        "original":  "O que é a Torre do Tombo?",
        "resolvida": "O que é a Torre do Tombo?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0191": {
        "original":  "Onde fica?",
        "resolvida": "Onde fica a Torre do Tombo?",
        "tipo": "RESOLVIDA",
        "nota": "Referente é a Torre do Tombo."
    },

    # -------------------------------------------------------------------------
    # Grupo 2743 — Ngungunhane
    # -------------------------------------------------------------------------
    "0194": {
        "original":  "Quantas esposas tinha Ngungunhane?",
        "resolvida": "Quantas esposas tinha Ngungunhane?",
        "tipo": "INALTERADA",
        "nota": "Pergunta âncora."
    },
    "0195": {
        "original":  "Como é que se chamava o filho dele?",
        "resolvida": "Como é que se chamava o filho de Ngungunhane?",
        "tipo": "RESOLVIDA",
        "nota": "'dele' refere-se a Ngungunhane."
    },
}

# Estatísticas
if __name__ == "__main__":
    total = len(RESOLUCOES)
    resolvidas  = sum(1 for v in RESOLUCOES.values() if v["tipo"] == "RESOLVIDA")
    parciais    = sum(1 for v in RESOLUCOES.values() if v["tipo"] == "PARCIAL")
    inalteradas = sum(1 for v in RESOLUCOES.values() if v["tipo"] == "INALTERADA")

    print("=" * 60)
    print("RESUMO DA RESOLUÇÃO ANAFÓRICA")
    print(f"  Perguntas em grupos com dependência : {total}")
    print(f"  Resolvidas com referente explícito  : {resolvidas}")
    print(f"  Resolução parcial (ambiguidade)     : {parciais}")
    print(f"  Inalteradas (âncoras do grupo)      : {inalteradas}")
    print(f"  Perguntas isoladas (sem dependência): {200 - total}")
    print("=" * 60)
