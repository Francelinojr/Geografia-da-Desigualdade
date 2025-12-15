
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

import glob
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
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
    50: 'Centro-Oeste', 51: 'Centro-Oeste', 52: 'Centro-Oeste', 53: 'Centro-Oeste'
}
UF_CODE_TO_SG = {
    11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO',
    21: 'MA', 22: 'PI', 23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE', 27: 'AL', 28: 'SE', 29: 'BA',
    31: 'MG', 32: 'ES', 33: 'RJ', 35: 'SP',
    41: 'PR', 42: 'SC', 43: 'RS',
    50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF'
}
def infer_regiao_uf(df):
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
    paths = [f"MICRODADOS_CADASTRO_IES_{ano}.CSV", f"MICRODADOS_ED_SUP_IES_{ano}.CSV"]
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

def load_cursos(ano):
    try:
        path_csv = f"MICRODADOS_CADASTRO_CURSOS_{ano}.CSV"
        df = pd.read_csv(path_csv, sep=';', encoding='latin1', low_memory=False)
        df = infer_regiao_uf(df)
        df = df[df['NO_REGIAO'].isin(['Nordeste', 'Sudeste'])].copy()
        col_area = 'NO_CINE_AREA_GERAL' if 'NO_CINE_AREA_GERAL' in df.columns else 'NO_OCDE_AREA_GERAL'
        cols = [
            'NO_REGIAO', 'SG_UF', 'NO_MUNICIPIO', 'CO_MUNICIPIO', 'TP_CATEGORIA_ADMINISTRATIVA',
            col_area, 'CO_CINE_AREA_GERAL', 'QT_MAT', 'QT_MAT_FEM', 'CO_IES'
        ]
        for c in ['QT_ING', 'QT_CONC']:
            if c in df.columns:
                cols.append(c)
        df_clean = df[cols].rename(columns={col_area: 'AREA_GERAL'})
        ies_map = load_ies_mapping(ano)
        if not ies_map.empty:
            df_clean = df_clean.merge(ies_map, on='CO_IES', how='left')
            if 'NO_MUNICIPIO_IES' in df_clean.columns:
                df_clean['NO_MUNICIPIO'] = df_clean['NO_MUNICIPIO'].fillna(df_clean['NO_MUNICIPIO_IES'])
            if 'CO_MUNICIPIO_IES' in df_clean.columns:
                df_clean['CO_MUNICIPIO'] = df_clean['CO_MUNICIPIO'].fillna(df_clean['CO_MUNICIPIO_IES'])
        df_clean['ANO'] = ano
        return df_clean
    except Exception:
        return pd.DataFrame()

# Configuração visual
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (12, 6)

def identificar_stem(texto):
    if pd.isna(texto): return False
    texto = str(texto).upper()
    palavras_chave = [
        'CIÊNCIAS NATURAIS', 'MATEMÁTICA', 'ESTATÍSTICA', 
        'COMPUTAÇÃO', 'TIC', 'ENGENHARIA', 'PRODUÇÃO', 'CONSTRUÇÃO'
    ]
    return any(p in texto for p in palavras_chave)

anos = sorted([int(p.split('_')[-1].split('.')[0]) for p in glob.glob("MICRODADOS_CADASTRO_CURSOS_*.CSV")])
lista_dfs = []
for ano in anos:
    print(f"Processando {ano}...")
    dfa = load_cursos(ano)
    if not dfa.empty:
        lista_dfs.append(dfa)
df_geral = pd.concat(lista_dfs, ignore_index=True)

# --- 3. ENGENHARIA DE DADOS (FILTROS E CÁLCULOS) ---

if 'CO_CINE_AREA_GERAL' in df_geral.columns:
    codes = df_geral['CO_CINE_AREA_GERAL'].astype(str).str.zfill(2)
    by_cine = codes.isin(['05', '06', '07'])
    df_geral['IS_STEM'] = np.where(df_geral['CO_CINE_AREA_GERAL'].notna(), by_cine, df_geral['AREA_GERAL'].apply(identificar_stem))
else:
    df_geral['IS_STEM'] = df_geral['AREA_GERAL'].apply(identificar_stem)
df_stem = df_geral[df_geral['IS_STEM']].copy()

# Definição Pública vs Privada (1,2,3 = Pública)
cat = pd.to_numeric(df_stem['TP_CATEGORIA_ADMINISTRATIVA'], errors='coerce')
df_stem['TIPO_IES'] = np.where(cat.fillna(9).astype(int) <= 3, 'Pública', 'Privada')

# Agregação por Ano e Região
resumo_anual = df_stem.groupby(['ANO', 'NO_REGIAO']).agg({
    'QT_MAT': 'sum',
    'QT_MAT_FEM': 'sum'
}).reset_index()

resumo_anual['PCT_MULHERES'] = resumo_anual['QT_MAT_FEM'] / resumo_anual['QT_MAT'] * 100

# --- 4. GERAÇÃO DOS GRÁFICOS ---

# GRÁFICO 1: A Evolução da Desigualdade (Linha do Tempo)
plt.figure(figsize=(10, 6))
for reg in resumo_anual['NO_REGIAO'].unique():
    d = resumo_anual[resumo_anual['NO_REGIAO'] == reg]
    plt.plot(d['ANO'], d['PCT_MULHERES'], marker='o', linewidth=2.5, label=reg)
resumo_media_w = resumo_anual.groupby('ANO').agg({'QT_MAT':'sum','QT_MAT_FEM':'sum'}).reset_index()
resumo_media_w['PCT'] = resumo_media_w['QT_MAT_FEM'] / resumo_media_w['QT_MAT'] * 100
plt.title('Evolução da Participação Feminina em STEM: Nordeste vs Sudeste (2010-2024)', fontsize=14)
plt.ylabel('% de Mulheres em Cursos STEM')
plt.xlabel('Ano')
plt.ylim(0, 55)
plt.legend(title='Região')
plt.grid(True, alpha=0.3)
plt.gca().yaxis.set_major_formatter(PercentFormatter(100))
plt.tight_layout()
plt.savefig(f"evolucao_pct_mulheres_stem_NE_SE.png", dpi=150)
plt.show()

# GRÁFICO 2: "Clusters" Visuais - Pública vs Privada (Foco em 2024)
# Para ver onde a desigualdade se esconde (no setor privado ou público?)
resumo_tipo = df_stem.groupby(['ANO', 'NO_REGIAO', 'TIPO_IES']).agg({
    'QT_MAT': 'sum',
    'QT_MAT_FEM': 'sum'
}).reset_index()
resumo_tipo['PCT_MULHERES'] = resumo_tipo['QT_MAT_FEM'] / resumo_tipo['QT_MAT'] * 100

plt.figure(figsize=(10, 6))
dt = resumo_tipo[resumo_tipo['ANO'] == 2024]
pivot_tipo = dt.pivot_table(index='NO_REGIAO', columns='TIPO_IES', values='PCT_MULHERES')
idx = np.arange(len(pivot_tipo.index))
width = 0.35
plt.bar(idx - width/2, pivot_tipo.get('Pública', pd.Series(index=pivot_tipo.index, dtype=float)), width, label='Pública')
plt.bar(idx + width/2, pivot_tipo.get('Privada', pd.Series(index=pivot_tipo.index, dtype=float)), width, label='Privada')
plt.xticks(idx, pivot_tipo.index)
plt.title('Geografia da Desigualdade: Impacto do Tipo de IES (Dados de 2024)', fontsize=14)
plt.ylabel('% de Mulheres em STEM')
plt.xlabel('Região')
plt.ylim(0, 60)
plt.legend(title='Categoria Administrativa')
plt.gca().yaxis.set_major_formatter(PercentFormatter(100))
plt.tight_layout()
plt.savefig(f"pct_mulheres_stem_tipo_IES_2024.png", dpi=150)
plt.show()

print("Tabela de Dados (Evolução):")
print(resumo_anual)

keys = ['ANO', 'NO_REGIAO', 'SG_UF', 'NO_MUNICIPIO', 'CO_MUNICIPIO']
df_stem_tipo = df_stem.groupby(keys + ['TIPO_IES']).agg(
    QT_MAT=('QT_MAT', 'sum'),
    QT_MAT_FEM=('QT_MAT_FEM', 'sum')
).reset_index()
wide = df_stem_tipo.pivot_table(index=keys, columns='TIPO_IES', values='QT_MAT', aggfunc='sum')
wide = wide.rename(columns={'Pública': 'QT_MAT_PUBLICA', 'Privada': 'QT_MAT_PRIVADA'})
base = df_stem.groupby(keys).agg(
    QT_MAT=('QT_MAT', 'sum'),
    QT_MAT_FEM=('QT_MAT_FEM', 'sum')
)
df_ind = base.join(wide).fillna(0)
df_ind['PCT_FEM_STEM'] = np.where(df_ind['QT_MAT'] > 0, df_ind['QT_MAT_FEM'] / df_ind['QT_MAT'], np.nan)
df_ind['VOLUME_STEM'] = df_ind['QT_MAT']
df_ind['PCT_PUBLICA'] = np.where(df_ind['QT_MAT'] > 0, df_ind['QT_MAT_PUBLICA'] / df_ind['QT_MAT'], np.nan)
df_ind['PCT_PRIVADA'] = np.where(df_ind['QT_MAT'] > 0, df_ind['QT_MAT_PRIVADA'] / df_ind['QT_MAT'], np.nan)
if {'QT_ING', 'QT_CONC'}.issubset(df_stem.columns):
    base2 = df_stem.groupby(keys).agg(
        QT_ING=('QT_ING', 'sum'),
        QT_CONC=('QT_CONC', 'sum')
    )
    df_ind = df_ind.join(base2)
    df_ind['TAXA_SUCESSO'] = np.where(df_ind['QT_ING'] > 0, df_ind['QT_CONC'] / df_ind['QT_ING'], np.nan)

ano_ref = int(df_ind.reset_index()['ANO'].max())
df_k = df_ind.reset_index()
df_k = df_k[df_k['ANO'] == ano_ref].copy()
features = ['PCT_FEM_STEM', 'VOLUME_STEM', 'PCT_PUBLICA']
X = df_k[features].fillna(0).values
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
km = KMeans(n_clusters=3, n_init=10, random_state=42)
df_k['CLUSTER'] = km.fit_predict(Xs)
means = df_k.groupby('CLUSTER')[['PCT_FEM_STEM', 'VOLUME_STEM', 'PCT_PRIVADA', 'PCT_PUBLICA']].mean()
cid_c = means['PCT_FEM_STEM'].idxmin()
vol_thresh = df_k['VOLUME_STEM'].quantile(0.75)
priv_med = means['PCT_PRIVADA'].fillna(0).mean()
score_a = (means['VOLUME_STEM'] * means['PCT_PRIVADA'].fillna(0))
eligible = score_a[means['VOLUME_STEM'] >= vol_thresh]
cid_a = eligible.idxmax() if not eligible.empty else score_a.idxmax()
labels = {}
for cid in means.index:
    if cid == cid_a:
        labels[cid] = 'A'
    elif cid == cid_c:
        labels[cid] = 'C'
    else:
        labels[cid] = 'B'
df_k['LABEL'] = df_k['CLUSTER'].map(labels)
dist = df_k.groupby(['NO_REGIAO', 'CLUSTER']).size().reset_index(name='QTD')
plt.figure(figsize=(10, 6))
pivot_cl = df_k.groupby(['NO_REGIAO', 'LABEL']).size().reset_index(name='QTD').pivot_table(index='NO_REGIAO', columns='LABEL', values='QTD', fill_value=0)
idx = np.arange(len(pivot_cl.index))
width = 0.2
for i, cl in enumerate(pivot_cl.columns):
    plt.bar(idx + (i - len(pivot_cl.columns)/2)*width, pivot_cl[cl], width, label=str(cl))
plt.xticks(idx, pivot_cl.index)
plt.title(f'Distribuição de Clusters por Região (Ano {ano_ref})')
plt.ylabel('Municípios')
plt.xlabel('Região')
plt.legend(title='Cluster')
plt.show()
top_desertos = df_k.sort_values('PCT_FEM_STEM').head(10)[['NO_REGIAO', 'SG_UF', 'NO_MUNICIPIO', 'PCT_FEM_STEM', 'VOLUME_STEM', 'PCT_PUBLICA', 'LABEL']]
print("Municípios com menor participação feminina em STEM (ano de referência):")
print(top_desertos)
df_ind.reset_index().to_csv("indicadores_stem_municipio.csv", index=False)
df_k.to_csv(f"clusters_stem_municipio_{ano_ref}.csv", index=False)

keys_micro = ['ANO', 'NO_REGIAO', 'SG_UF', 'NO_MICRORREGIAO_IES', 'CO_MICRORREGIAO_IES']
base_m = df_stem.groupby(keys_micro).agg(
    QT_MAT=('QT_MAT', 'sum'),
    QT_MAT_FEM=('QT_MAT_FEM', 'sum')
)
tipo_m = df_stem.groupby(keys_micro + ['TIPO_IES']).agg(QT_MAT=('QT_MAT', 'sum')).reset_index()
wide_m = tipo_m.pivot_table(index=keys_micro, columns='TIPO_IES', values='QT_MAT', aggfunc='sum')
wide_m = wide_m.rename(columns={'Pública': 'QT_MAT_PUBLICA', 'Privada': 'QT_MAT_PRIVADA'})
df_ind_m = base_m.join(wide_m).fillna(0)
df_ind_m['PCT_FEM_STEM'] = np.where(df_ind_m['QT_MAT'] > 0, df_ind_m['QT_MAT_FEM'] / df_ind_m['QT_MAT'], np.nan)
df_ind_m['VOLUME_STEM'] = df_ind_m['QT_MAT']
df_ind_m['PCT_PUBLICA'] = np.where(df_ind_m['QT_MAT'] > 0, df_ind_m['QT_MAT_PUBLICA'] / df_ind_m['QT_MAT'], np.nan)
df_ind_m['PCT_PRIVADA'] = np.where(df_ind_m['QT_MAT'] > 0, df_ind_m['QT_MAT_PRIVADA'] / df_ind_m['QT_MAT'], np.nan)
df_ind_m.reset_index().to_csv("indicadores_stem_microrregiao.csv", index=False)

cmp_mun = df_ind.reset_index().groupby('NO_REGIAO')['PCT_FEM_STEM'].mean().rename('MUNICIPIO')
cmp_mic = df_ind_m.reset_index().groupby('NO_REGIAO')['PCT_FEM_STEM'].mean().rename('MICRORREGIAO')
cmp = pd.concat([cmp_mun, cmp_mic], axis=1)
plt.figure(figsize=(10, 6))
idx = np.arange(len(cmp.index))
width = 0.35
plt.bar(idx - width/2, cmp['MUNICIPIO'], width, label='Município')
plt.bar(idx + width/2, cmp['MICRORREGIAO'], width, label='Microrregião')
plt.xticks(idx, cmp.index)
plt.title('Comparação de % Mulheres em STEM: Município vs Microrregião')
plt.ylabel('% de Mulheres')
plt.xlabel('Região')
plt.legend()
plt.gca().yaxis.set_major_formatter(PercentFormatter(100))
plt.tight_layout()
plt.savefig(f"comparacao_municipio_vs_microrregiao_{ano_ref}.png", dpi=150)
plt.show()
if 'NO_MICRORREGIAO_IES' in df_ind_m.index.names or 'NO_MICRORREGIAO_IES' in df_ind_m.reset_index().columns:
    tmp = df_ind_m.reset_index()
    tmp = tmp[tmp['ANO'] == ano_ref]
    for reg in ['Nordeste', 'Sudeste']:
        sub = tmp[tmp['NO_REGIAO'] == reg]
        grp = sub.groupby('NO_MICRORREGIAO_IES')['PCT_FEM_STEM'].mean().sort_values(ascending=False).head(15)
        plt.figure(figsize=(10, 6))
        plt.barh(grp.index[::-1], grp.values[::-1])
        plt.title(f"% Mulheres em STEM por Microrregião ({reg}, {ano_ref})")
        plt.xlabel('% de Mulheres')
        plt.ylabel('Microrregião')
        plt.tight_layout()
        plt.show()
seg = df_stem[df_stem['ANO'] == ano_ref].groupby(keys_micro + ['TIPO_IES']).agg(QT_MAT=('QT_MAT','sum'), QT_MAT_FEM=('QT_MAT_FEM','sum')).reset_index()
seg['PCT_FEM_STEM'] = np.where(seg['QT_MAT']>0, seg['QT_MAT_FEM']/seg['QT_MAT'], np.nan)
for reg in ['Nordeste', 'Sudeste']:
    for tipo in ['Pública', 'Privada']:
        sub = seg[(seg['NO_REGIAO'] == reg) & (seg['TIPO_IES'] == tipo)]
        grp = sub.groupby('NO_MICRORREGIAO_IES')['PCT_FEM_STEM'].mean().sort_values(ascending=False).head(15)
        if not grp.empty:
            plt.figure(figsize=(10, 6))
            plt.barh(grp.index[::-1], grp.values[::-1])
            plt.title(f"% Mulheres em STEM por Microrregião ({reg}, {tipo}, {ano_ref})")
            plt.xlabel('% de Mulheres')
            plt.ylabel('Microrregião')
            plt.tight_layout()
            plt.savefig(f"microrregiao_{reg}_{tipo}_{ano_ref}.png", dpi=150)
            plt.show()
for ano in sorted(df_ind.reset_index()['ANO'].unique()):
    df_ind.reset_index().query('ANO == @ano').to_csv(f"indicadores_stem_municipio_{ano}.csv", index=False)
    if 'NO_MICRORREGIAO_IES' in df_ind_m.reset_index().columns:
        df_ind_m.reset_index().query('ANO == @ano').to_csv(f"indicadores_stem_microrregiao_{ano}.csv", index=False)
    cmp_mun_y = df_ind.reset_index().query('ANO == @ano').groupby('NO_REGIAO')['PCT_FEM_STEM'].mean().rename('MUNICIPIO')
    cmp_mic_y = df_ind_m.reset_index().query('ANO == @ano').groupby('NO_REGIAO')['PCT_FEM_STEM'].mean().rename('MICRORREGIAO')
    cmp_y = pd.concat([cmp_mun_y, cmp_mic_y], axis=1)
    if not cmp_y.empty:
        plt.figure(figsize=(10, 6))
        idxy = np.arange(len(cmp_y.index))
        widthy = 0.35
        plt.bar(idxy - widthy/2, cmp_y['MUNICIPIO'], widthy, label='Município')
        plt.bar(idxy + widthy/2, cmp_y['MICRORREGIAO'], widthy, label='Microrregião')
        plt.xticks(idxy, cmp_y.index)
        plt.title(f'Comparação de % Mulheres em STEM: Município vs Microrregião ({ano})')
        plt.ylabel('% de Mulheres')
        plt.xlabel('Região')
        plt.legend()
        plt.gca().yaxis.set_major_formatter(PercentFormatter(100))
        plt.tight_layout()
        plt.savefig(f"comparacao_municipio_vs_microrregiao_{ano}.png", dpi=150)
        plt.show()
    dfa = df_ind.reset_index()
    dfa = dfa[dfa['ANO'] == ano]
    Xa = dfa[['PCT_FEM_STEM', 'VOLUME_STEM', 'PCT_PUBLICA']].fillna(0).values
    if Xa.shape[0] >= 3:
        sca = StandardScaler()
        Xsa = sca.fit_transform(Xa)
        kma = KMeans(n_clusters=3, n_init=10, random_state=42)
        labs = kma.fit_predict(Xsa)
        dfka = dfa.copy()
        dfka['CLUSTER'] = labs
        mna = dfka.groupby('CLUSTER')[['PCT_FEM_STEM', 'VOLUME_STEM', 'PCT_PRIVADA', 'PCT_PUBLICA']].mean()
        ida_c = mna['PCT_FEM_STEM'].idxmin()
        thr = dfka['VOLUME_STEM'].quantile(0.75)
        sca2 = (mna['VOLUME_STEM'] * mna['PCT_PRIVADA'].fillna(0))
        elig = sca2[mna['VOLUME_STEM'] >= thr]
        ida_a = elig.idxmax() if not elig.empty else sca2.idxmax()
        labmap = {}
        for cid in mna.index:
            if cid == ida_a:
                labmap[cid] = 'A'
            elif cid == ida_c:
                labmap[cid] = 'C'
            else:
                labmap[cid] = 'B'
        dfka['LABEL'] = dfka['CLUSTER'].map(labmap)
        dfka.to_csv(f"clusters_stem_municipio_{ano}.csv", index=False) 
