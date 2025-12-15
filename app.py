import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import os
import glob

# --- 1. CONSTANTES E MAPPING ---

REGIAO_UF = {
    'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MS': 'Centro-Oeste', 'MT': 'Centro-Oeste'
}
UF_CODE_TO_REGIAO = {
    11: 'Norte', 12: 'Norte', 13: 'Norte', 14: 'Norte', 15: 'Norte', 16: 'Norte', 17: 'Norte',
    21: 'Nordeste', 22: 'Nordeste', 23: 'Nordeste', 24: 'Nordeste', 25: 'Nordeste', 26: 'Nordeste', 27: 'Nordeste', 28: 'Nordeste', 29: 'Nordeste',
    31: 'Sudeste', 32: 'Sudeste', 33: 'Sudeste', 35: 'Sudeste',
    41: 'Sul', 42: 'Sul', 43: 'Sul',
    50: 'Centro-Oeste', 51: 'MT', 52: 'GO', 53: 'DF'
}
UF_CODE_TO_SG = {
    11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO',
    21: 'MA', 22: 'PI', 23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL', 28: 'SE', 29: 'BA',
    31: 'MG', 32: 'ES', 33: 'RJ', 35: 'SP',
    41: 'PR', 42: 'SC', 43: 'RS',
    50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF'
}

# Definição de Áreas STEM (CINE/OCDE)
CINE_STEM_CODES = ['05', '06', '07']
CINE_STEM_AREAS = {
    '05': 'Ciências Naturais, Matemática e Estatística',
    '06': 'Tecnologias da Informação e Comunicação (TIC)',
    '07': 'Engenharia, Produção e Construção'
}

# --- 2. FUNÇÕES DE CARREGAMENTO E PRÉ-PROCESSAMENTO ---

def infer_regiao_uf(df):
    """Adiciona colunas de região e UF ao DataFrame, se ausentes."""
    if 'NO_REGIAO' in df.columns:
        return df
    if 'SG_UF' in df.columns:
        df['NO_REGIAO'] = df['SG_UF'].map(REGIAO_UF)
        return df
    if 'CO_UF' in df.columns:
        df['NO_REGIAO'] = df['CO_UF'].map(UF_CODE_TO_REGIAO)
        if 'SG_UF' not in df.columns:
            df['SG_UF'] = df['CO_UF'].map(UF_CODE_TO_SG)
        return df
    if 'CO_MUNICIPIO' in df.columns:
        def _uf_code(x):
            try:
                return int(str(int(x))[:2])
            except Exception:
                return np.nan
        uf_codes = df['CO_MUNICIPIO'].apply(_uf_code)
        df['SG_UF'] = uf_codes.map(UF_CODE_TO_SG)
        df['NO_REGIAO'] = uf_codes.map(UF_CODE_TO_REGIAO)
        return df
    return df

def load_ies_mapping(ano):
    """Carrega dados de IES para mapeamento de microrregião/município."""
    paths = [
        os.path.join(PATH_CSV_DIR, f"MICRODADOS_CADASTRO_IES_{ano}.CSV"),
        os.path.join(PATH_CSV_DIR, f"MICRODADOS_ED_SUP_IES_{ano}.CSV")
    ]
    for p in paths:
        try:
            df = pd.read_csv(p, sep=';', encoding='latin1', low_memory=False)
            df = infer_regiao_uf(df)
            cols = [c for c in [
                'CO_IES', 'NO_MICRORREGIAO_IES', 'CO_MICRORREGIAO_IES',
                'NO_MUNICIPIO_IES', 'CO_MUNICIPIO_IES', 'SG_UF_IES', 'NO_REGIAO_IES', 'CO_UF_IES'
            ] if c in df.columns]
            return df[cols]
        except Exception:
            continue
    return pd.DataFrame(columns=['CO_IES'])

def identificar_stem(texto):
    """Identifica cursos STEM por palavras-chave (fallback para anos sem CINE)."""
    if pd.isna(texto): return False
    texto = str(texto).upper()
    palavras_chave = [
        'CIÊNCIAS NATURAIS', 'MATEMÁTICA', 'ESTATÍSTICA', 
        'COMPUTAÇÃO', 'TIC', 'ENGENHARIA', 'PRODUÇÃO', 'CONSTRUÇÃO'
    ]
    return any(p in texto for p in palavras_chave)

def load_cursos(ano):
    """Carrega e pré-processa os dados de cursos para um dado ano."""
    try:
        path_csv = os.path.join(PATH_CSV_DIR, f"MICRODADOS_CADASTRO_CURSOS_{ano}.CSV")
        df = pd.read_csv(path_csv, sep=';', encoding='latin1', low_memory=False)
        df = infer_regiao_uf(df)
        
        # Filtra apenas Nordeste e Sudeste
        df = df[df['NO_REGIAO'].isin(['Nordeste', 'Sudeste'])].copy()
        
        # Identifica a coluna de área geral
        col_area = 'NO_CINE_AREA_GERAL' if 'NO_CINE_AREA_GERAL' in df.columns else 'NO_OCDE_AREA_GERAL'
        
        # Colunas a serem mantidas
        cols = [
            'NO_REGIAO', 'SG_UF', 'NO_MUNICIPIO', 'CO_MUNICIPIO', 'TP_CATEGORIA_ADMINISTRATIVA',
            col_area, 'CO_CINE_AREA_GERAL', 'QT_MAT', 'QT_MAT_FEM', 'CO_IES'
        ]
        for c in ['QT_ING', 'QT_CONC']:
            if c in df.columns:
                cols.append(c)
        
        df_clean = df[cols].rename(columns={col_area: 'AREA_GERAL'})
        
        # Merge com dados de IES para informações de microrregião/município
        ies_map = load_ies_mapping(ano)
        if not ies_map.empty:
            df_clean = df_clean.merge(ies_map, on='CO_IES', how='left')
            # Preenche dados de município/microrregião do curso com os da IES, se faltarem
            if 'NO_MUNICIPIO_IES' in df_clean.columns:
                df_clean['NO_MUNICIPIO'] = df_clean['NO_MUNICIPIO'].fillna(df_clean['NO_MUNICIPIO_IES'])
            if 'CO_MUNICIPIO_IES' in df_clean.columns:
                df_clean['CO_MUNICIPIO'] = df_clean['CO_MUNICIPIO'].fillna(df_clean['CO_MUNICIPIO_IES'])
        
        df_clean['ANO'] = ano
        return df_clean
    except Exception as e:
        # print(f"Erro ao carregar dados do ano {ano}: {e}")
        return pd.DataFrame()

# --- 3. ENGENHARIA DE DADOS (FILTROS E CÁLCULOS) ---

# Configuração visual
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (12, 6)

# Define o diretório de dados
PATH_CSV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Comma Separated Values Source File')
if not os.path.exists(PATH_CSV_DIR):
    PATH_CSV_DIR = os.path.join(os.getcwd(), 'Dados', 'Comma Separated Values Source File')

# Carrega todos os anos disponíveis
anos = sorted([int(os.path.basename(p).split('_')[-1].split('.')[0]) for p in glob.glob(os.path.join(PATH_CSV_DIR, "MICRODADOS_CADASTRO_CURSOS_*.CSV"))])
lista_dfs = []
for ano in anos:
    print(f"Processando {ano}...")
    dfa = load_cursos(ano)
    if not dfa.empty:
        lista_dfs.append(dfa)
df_geral = pd.concat(lista_dfs, ignore_index=True) if len(lista_dfs) > 0 else pd.DataFrame(columns=['ANO'])

if df_geral.empty:
    print("Nenhum dado carregado. Verifique os arquivos CSV.")
    exit()

# Identificação STEM
if 'CO_CINE_AREA_GERAL' in df_geral.columns:
    codes = df_geral['CO_CINE_AREA_GERAL'].astype(str).str.zfill(2)
    by_cine = codes.isin(CINE_STEM_CODES)
    # Usa CINE como primário, fallback para palavras-chave
    df_geral['IS_STEM'] = np.where(df_geral['CO_CINE_AREA_GERAL'].notna(), by_cine, df_geral['AREA_GERAL'].apply(identificar_stem))
else:
    df_geral['IS_STEM'] = df_geral['AREA_GERAL'].apply(identificar_stem)
    
df_stem = df_geral[df_geral['IS_STEM']].copy()

# Definição Pública vs Privada (1,2,3 = Pública)
cat = pd.to_numeric(df_stem['TP_CATEGORIA_ADMINISTRATIVA'], errors='coerce')
df_stem['TIPO_IES'] = np.where(cat.fillna(9).astype(int) <= 3, 'Pública', 'Privada')

# Cálculo da Disparidade de Gênero
df_stem['QT_MAT_MASC'] = df_stem['QT_MAT'] - df_stem['QT_MAT_FEM']

# Agregação por Ano e Região
resumo_anual = df_stem.groupby(['ANO', 'NO_REGIAO']).agg(
    QT_MAT=('QT_MAT', 'sum'),
    QT_MAT_FEM=('QT_MAT_FEM', 'sum'),
    QT_MAT_MASC=('QT_MAT_MASC', 'sum')
).reset_index()

# Cálculo das métricas de gênero
resumo_anual['PCT_MULHERES'] = resumo_anual['QT_MAT_FEM'] / resumo_anual['QT_MAT'] * 100
resumo_anual['PCT_HOMENS'] = resumo_anual['QT_MAT_MASC'] / resumo_anual['QT_MAT'] * 100
# Índice de Paridade de Gênero (IPG): Mulheres / Homens. IPG = 1.0 é paridade.
resumo_anual['IPG_STEM'] = np.where(resumo_anual['QT_MAT_MASC'] > 0, resumo_anual['QT_MAT_FEM'] / resumo_anual['QT_MAT_MASC'], np.nan)

# --- 4. GERAÇÃO DOS GRÁFICOS E TABELAS ---

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Imagens_Geradas')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# GRÁFICO 1: Evolução da Disparidade (IPG)
plt.figure(figsize=(12, 7))
for reg in resumo_anual['NO_REGIAO'].unique():
    d = resumo_anual[resumo_anual['NO_REGIAO'] == reg]
    plt.plot(d['ANO'], d['IPG_STEM'], marker='o', linewidth=2.5, label=reg)

plt.axhline(1.0, color='red', linestyle='--', linewidth=1, label='Paridade (IPG=1.0)')
plt.title('Evolução do Índice de Paridade de Gênero (IPG) em STEM: Nordeste vs Sudeste', fontsize=14)
plt.ylabel('Índice de Paridade de Gênero (Mulheres/Homens)')
plt.xlabel('Ano')
plt.ylim(0, 1.5)
plt.legend(title='Região')
plt.grid(True, alpha=0.3)
plt.tight_layout()
ipg_filename = "evolucao_ipg_stem_NE_SE.png"
plt.savefig(os.path.join(OUTPUT_DIR, ipg_filename), dpi=150)
plt.close()

# GRÁFICO 2: Comparação Pública vs Privada (Foco no último ano) - PCT_MULHERES
ano_ref = anos[-1]
resumo_tipo = df_stem.groupby(['ANO', 'NO_REGIAO', 'TIPO_IES']).agg(
    QT_MAT=('QT_MAT', 'sum'),
    QT_MAT_FEM=('QT_MAT_FEM', 'sum')
).reset_index()
resumo_tipo['PCT_MULHERES'] = resumo_tipo['QT_MAT_FEM'] / resumo_tipo['QT_MAT'] * 100

plt.figure(figsize=(10, 6))
dt = resumo_tipo[resumo_tipo['ANO'] == ano_ref] # Último ano
pivot_tipo = dt.pivot_table(index='NO_REGIAO', columns='TIPO_IES', values='PCT_MULHERES')
idx = np.arange(len(pivot_tipo.index))
width = 0.35
plt.bar(idx - width/2, pivot_tipo.get('Pública', pd.Series(index=pivot_tipo.index, dtype=float)), width, label='Pública', color='#1f77b4')
plt.bar(idx + width/2, pivot_tipo.get('Privada', pd.Series(index=pivot_tipo.index, dtype=float)), width, label='Privada', color='#ff7f0e')
plt.xticks(idx, pivot_tipo.index)
plt.title(f'Geografia da Desigualdade: % Mulheres em STEM por Tipo de IES ({ano_ref})', fontsize=14)
plt.ylabel('% de Mulheres em STEM')
plt.xlabel('Região')
plt.ylim(0, 60)
plt.legend(title='Categoria Administrativa')
plt.gca().yaxis.set_major_formatter(PercentFormatter(100))
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
ies_filename = f"pct_mulheres_stem_tipo_IES_{ano_ref}.png"
plt.savefig(os.path.join(OUTPUT_DIR, ies_filename), dpi=150)
plt.close()

print(f"Código executado. Gráficos salvos em: {OUTPUT_DIR}")

print("\n--- Tabela de Evolução da Disparidade (IPG) ---")
print(resumo_anual[['ANO', 'NO_REGIAO', 'QT_MAT', 'QT_MAT_FEM', 'QT_MAT_MASC', 'PCT_MULHERES', 'IPG_STEM']].to_markdown(index=False))

print("\n--- Classificação de Cursos STEM ---")
print(pd.DataFrame(CINE_STEM_AREAS.items(), columns=['Código CINE', 'Área de Estudo']).to_markdown(index=False))

# --- 5. Geração de Tabela de Disparidade por Área STEM (Último Ano) ---
df_stem_area = df_stem[df_stem['ANO'] == ano_ref].copy()
df_stem_area['AREA_CINE'] = df_stem_area['CO_CINE_AREA_GERAL'].astype(str).str.zfill(2).map(CINE_STEM_AREAS)

resumo_area = df_stem_area.groupby(['NO_REGIAO', 'AREA_CINE']).agg(
    QT_MAT=('QT_MAT', 'sum'),
    QT_MAT_FEM=('QT_MAT_FEM', 'sum'),
    QT_MAT_MASC=('QT_MAT_MASC', 'sum')
).reset_index()

resumo_area['PCT_MULHERES'] = resumo_area['QT_MAT_FEM'] / resumo_area['QT_MAT'] * 100
resumo_area['IPG_STEM'] = np.where(resumo_area['QT_MAT_MASC'] > 0, resumo_area['QT_MAT_FEM'] / resumo_area['QT_MAT_MASC'], np.nan)

print(f"\n--- Tabela de Disparidade por Área STEM e Região ({ano_ref}) ---")
print(resumo_area[['NO_REGIAO', 'AREA_CINE', 'QT_MAT', 'PCT_MULHERES', 'IPG_STEM']].sort_values(by=['NO_REGIAO', 'IPG_STEM'], ascending=[True, False]).to_markdown(index=False))

# Tabela 4: Comparação Pública vs Privada (Último Ano)
resumo_tipo = df_stem.groupby(['ANO', 'NO_REGIAO', 'TIPO_IES']).agg(
    QT_MAT=('QT_MAT', 'sum'),
    QT_MAT_FEM=('QT_MAT_FEM', 'sum'),
    QT_MAT_MASC=('QT_MAT_MASC', 'sum')
).reset_index()
resumo_tipo['PCT_MULHERES'] = resumo_tipo['QT_MAT_FEM'] / resumo_tipo['QT_MAT'] * 100
resumo_tipo['IPG_STEM'] = np.where(resumo_tipo['QT_MAT_MASC'] > 0, resumo_tipo['QT_MAT_FEM'] / resumo_tipo['QT_MAT_MASC'], np.nan)

print(f"\n--- Tabela de Disparidade por Tipo de IES e Região ({ano_ref}) ---")
print(resumo_tipo[resumo_tipo['ANO'] == ano_ref][['NO_REGIAO', 'TIPO_IES', 'QT_MAT', 'PCT_MULHERES', 'IPG_STEM']].sort_values(by=['NO_REGIAO', 'TIPO_IES']).to_markdown(index=False))
