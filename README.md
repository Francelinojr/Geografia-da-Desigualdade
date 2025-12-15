# Geografia da Desigualdade: Um Estudo de Clusters sobre a Participação Feminina em STEM no Nordeste vs. Sudeste

Este repositório apresenta uma análise de dados focada na disparidade de gênero em cursos de STEM (Science, Technology, Engineering, and Mathematics) no ensino superior brasileiro. O estudo investiga a desigualdade espacial, contrastando a representatividade feminina em grandes polos ("Município") versus seu entorno regional ("Microrregião"), além de traçar a evolução histórica e as diferenças entre o ensino Público e Privado com dados atualizados até 2024.

A sub-representação feminina nas áreas de Ciência, Tecnologia, Engenharia e Matemática (STEM) é um fenômeno global, mas que assume nuances específicas quando analisado sob a ótica das desigualdades regionais brasileiras. Este estudo propõe uma análise comparativa entre as regiões Nordeste e Sudeste do Brasil, investigando como a localização geográfica e fatores socioeconômicos correlacionam-se com a inserção de mulheres no ensino superior nessas áreas.

Utilizando dados abertos (como os do Censo da Educação Superior do INEP), a pesquisa aplica algoritmos de aprendizado de máquina não supervisionado — especificamente técnicas de Clusterização (como K-Means ou Hierarchical Clustering) — para identificar padrões latentes de matrícula e conclusão de cursos. O objetivo é segmentar instituições ou microrregiões em grupos homogêneos baseados no Índice de Paridade de Gênero (IPG), permitindo identificar se o desenvolvimento econômico do Sudeste se traduz efetivamente em maior equidade de gênero ou se o Nordeste apresenta "ilhas" de paridade que desafiam as tendências macroeconômicas. Os resultados visam fornecer subsídios baseados em dados para políticas públicas educacionais mais assertivas e regionalizadas.

## 🎯 Objetivos da Análise

- **Temporal**: Mapear a evolução da participação feminina ao longo de 14 anos (2010-2024).
- **Espacial**: Identificar se a inclusão é difusa (capilarizada na região) ou concentrada ("ilhas de excelência").
- **Setorial**: Comparar o desempenho de instituições Públicas e Privadas nas microrregiões, com foco em 2024.

## 📈 1. A Visão Macro: Evolução Temporal (2010-2024)

A linha do tempo abaixo revela a trajetória da participação feminina nas duas regiões comparadas, baseada na agregação dos microdados do INEP.

<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2010" src="https://github.com/user-attachments/assets/163fbdfd-0296-4b67-b1a5-4e91cf2d8265" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2011" src="https://github.com/user-attachments/assets/3d4df8f1-0197-4563-b9a0-2ee99ade3bfb" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2012" src="https://github.com/user-attachments/assets/056e59ef-7b48-437c-bb98-d0a0330bb659" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2013" src="https://github.com/user-attachments/assets/68bd6c27-7642-44c8-bcc8-15ae22f5590d" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2014" src="https://github.com/user-attachments/assets/f32171f9-94d3-4208-98d4-973117d53e19" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2015" src="https://github.com/user-attachments/assets/5508d082-e874-464d-8129-34f2e98d4c60" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2016" src="https://github.com/user-attachments/assets/bae1b1ff-ed96-4dac-9413-9fde1151702a" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2017" src="https://github.com/user-attachments/assets/a2b7cd5e-01bd-4c88-b44a-29777ffbc2e7" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2018" src="https://github.com/user-attachments/assets/f60ac36a-1d6a-4616-b208-ca7dc17a9f7b" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2019" src="https://github.com/user-attachments/assets/0fa7d3ad-913c-414f-be23-736be093e69d" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2020" src="https://github.com/user-attachments/assets/38fe4538-bf60-4822-9eb3-40e5cbe65e39" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2021" src="https://github.com/user-attachments/assets/19080ae2-33f7-402f-ae0f-794aa6ca40b1" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2022" src="https://github.com/user-attachments/assets/e6ba8002-44b4-4eda-9380-cc1131d52cde" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2023" src="https://github.com/user-attachments/assets/79022c55-c882-47f3-afba-e72a5884ee2a" />
<img width="1500" height="900" alt="comparacao_municipio_vs_microrregiao_2024" src="https://github.com/user-attachments/assets/eac81d6d-f7b2-4f28-8e6f-47a8a4bd23c1" />

## Microregião Sudeste Publica e Privada 2024

<img width="1500" height="900" alt="microrregiao_Sudeste_Privada_2024" src="https://github.com/user-attachments/assets/386f9fd9-7af7-445f-85bf-464b90ffe1db" />
<img width="1500" height="900" alt="microrregiao_Sudeste_Pública_2024" src="https://github.com/user-attachments/assets/cfd80dc5-e7b5-41ba-9b2b-77dfc1221742" />


## Microregião Nordeste Publica e Privada 2024

<img width="1500" height="900" alt="microrregiao_Nordeste_Privada_2024" src="https://github.com/user-attachments/assets/39a48c49-15c0-436f-b6a9-94546531f19d" />
<img width="1500" height="900" alt="microrregiao_Nordeste_Pública_2024" src="https://github.com/user-attachments/assets/30208d94-0da7-4a96-beab-4bd77ec17447" />

<img width="1500" height="900" alt="pct_mulheres_stem_tipo_IES_2024" src="https://github.com/user-attachments/assets/0479e4f0-7c0c-4791-a2ca-e838f71fd022" />
<img width="1500" height="900" alt="evolucao_pct_mulheres_stem_NE_SE" src="https://github.com/user-attachments/assets/809a5c84-b067-4163-b9ac-fe4d4ae4892d" />
<img width="1000" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/d1a96b59-26f3-48d8-bf2d-d66dd95a9ee2" />

Tabela de Dados (Evolução):
     ANO NO_REGIAO    QT_MAT  QT_MAT_FEM  PCT_MULHERES
0   2010  Nordeste  147232.0     43256.0     29.379483
1   2010   Sudeste  582439.0    155855.0     26.759025
2   2011  Nordeste  171998.0     51466.0     29.922441
3   2011   Sudeste  666840.0    183548.0     27.525043
4   2012  Nordeste  200121.0     61860.0     30.911299
5   2012   Sudeste  731630.0    208762.0     28.533822
6   2013  Nordeste  230045.0     72318.0     31.436458
7   2013   Sudeste  802633.0    235560.0     29.348407
8   2014  Nordeste  260457.0     83071.0     31.894324
9   2014   Sudeste  883253.0    263837.0     29.871056
10  2015  Nordeste  283502.0     90707.0     31.995189
11  2015   Sudeste  904216.0    275287.0     30.444827
12  2016  Nordeste  289322.0     92314.0     31.907010
13  2016   Sudeste  879720.0    269940.0     30.684763
14  2017  Nordeste  289320.0     92022.0     31.806304
15  2017   Sudeste  863151.0    262601.0     30.423530
16  2018  Nordeste  288106.0     89359.0     31.016015
17  2018   Sudeste  835003.0    249726.0     29.907198
18  2019  Nordeste  276050.0     84369.0     30.562941
19  2019   Sudeste  787123.0    231685.0     29.434409
20  2020  Nordeste  259369.0     77352.0     29.823148
21  2020   Sudeste  776019.0    223937.0     28.857154
22  2021  Nordeste  264517.0     77835.0     29.425330
23  2021   Sudeste  772810.0    218130.0     28.225566
24  2022  Nordeste  287260.0     82333.0     28.661491
25  2022   Sudeste  820504.0    226978.0     27.663241
26  2023  Nordeste  299659.0     83830.0     27.975132
27  2023   Sudeste  889237.0    241873.0     27.200060
28  2024  Nordeste  318961.0     87457.0     27.419340
29  2024   Sudeste  926305.0    249824.0     26.969951

Municípios com menor participação feminina em STEM (ano de referência):
      NO_REGIAO SG_UF          NO_MUNICIPIO  PCT_FEM_STEM  VOLUME_STEM  PCT_PUBLICA LABEL
13776  Nordeste    AL                Anadia           0.0          1.0          0.0     C
13848  Nordeste    BA               Brejões           0.0          1.0          0.0     C
14418  Nordeste    PE             Dormentes           0.0         10.0          0.0     C
14897   Sudeste    MG                 Ijaci           0.0          1.0          0.0     C
15689   Sudeste    SP  Vista Alegre do Alto           0.0          1.0          0.0     C
13780  Nordeste    AL               Batalha           0.0          3.0          0.0     C
13783  Nordeste    AL          Campo Alegre           0.0         12.0          0.0     C
13784  Nordeste    AL    Colônia Leopoldina           0.0          2.0          0.0     C
13788  Nordeste    AL          Feira Grande           0.0          1.0          0.0     C
13830  Nordeste    BA      Amélia Rodrigues           0.0          3.0          0.0     C
