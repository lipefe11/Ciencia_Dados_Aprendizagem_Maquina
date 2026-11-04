"""Análise de dados reais do Ipea/Mapa das OSCs e IBGE/Censo 2022."""
from pathlib import Path
import json
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.metrics import (f1_score,precision_score,recall_score,accuracy_score,
    roc_auc_score,average_precision_score,confusion_matrix,silhouette_score,r2_score,mean_absolute_error)
from sklearn.model_selection import GroupShuffleSplit,train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.tree import DecisionTreeClassifier

ROOT=Path(__file__).resolve().parents[1]
FEATURES=['idade_anos','uf','natureza_juridica']
SEED=42


def salvar(df,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(path,index=False,float_format='%.6f',lineterminator='\n')


def preparar(root=ROOT):
    raw=root/'dados/brutos'
    fonte=json.loads((raw/'FONTES.json').read_text(encoding='utf-8'))
    osc=pd.read_csv(raw/'oscs_assistencia_social_20260806.csv',dtype=str)
    qualidade=[]
    for nome,mask in [('cnpj_invalido',~osc.cnpj.fillna('').str.fullmatch(r'\d{14}')),
                      ('cnpj_duplicado',osc.cnpj.duplicated())]:
        qualidade.append({'verificacao':nome,'ocorrencias':int(mask.sum())})
    osc=osc[osc.cnpj.fillna('').str.fullmatch(r'\d{14}')].drop_duplicates('cnpj').copy()
    osc=osc.rename(columns={'UF_Sigla':'uf','municipio_nome':'municipio_fonte','tx_razao_social_osc':'razao_social'})
    osc['fundacao']=pd.to_datetime(osc.dt_fundacao_osc,errors='coerce')
    ref=pd.Timestamp('2026-08-31')
    osc['idade_anos']=(ref-osc.fundacao).dt.days/365.25
    osc['ano_fundacao']=osc.fundacao.dt.year
    osc['cnpj_raiz']=osc.cnpj.str[:8]
    osc['nao_ativa']=osc.situacao_cadastral.ne('Ativa').astype(int)
    osc['ativa_no_mapa']=osc.situacao_cadastral.eq('Ativa') & osc.removida_do_mosc.eq('não')
    ufs=set('AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO'.split())
    qualidade += [{'verificacao':'data_fundacao_ausente_ou_invalida','ocorrencias':int(osc.fundacao.isna().sum())},
        {'verificacao':'fundacao_posterior_referencia','ocorrencias':int(osc.idade_anos.lt(0).sum())},
        {'verificacao':'uf_invalida','ocorrencias':int((~osc.uf.isin(ufs)).sum())},
        {'verificacao':'nome_municipio_com_caractere_substituido','ocorrencias':int(osc.municipio_fonte.fillna('').str.contains('\ufffd',regex=False).sum())}]
    # Situação cadastral não equivale a atendimento social, saúde financeira ou atividade operacional.
    popraw=json.loads((raw/'populacao_ibge_2022.json').read_text(encoding='utf-8-sig'))
    pop=pd.DataFrame([{'cd_municipio':r['D1C'],'municipio':r['D1N'],'populacao_2022':pd.to_numeric(r['V'],errors='coerce'),
                       'uf':r['D1N'][-2:]} for r in popraw[1:]])
    # A agregação usa códigos municipais e a UF oficial do IBGE, não a UF ausente do Ipea.
    ativas=osc[osc.ativa_no_mapa].copy()
    grupos=ativas.groupby('cd_municipio').agg(oscs_ativas=('cnpj','size'),idade_mediana=('idade_anos','median'),
                 fracao_fundadas_2010=('ano_fundacao',lambda x:float((x>=2010).mean()))).reset_index()
    municipios=pop.merge(grupos,on='cd_municipio',how='left',validate='one_to_one')
    municipios['oscs_ativas']=municipios.oscs_ativas.fillna(0).astype(int)
    municipios['oscs_por_100mil']=municipios.oscs_ativas/municipios.populacao_2022*100000
    faltantes=ativas[~ativas.cd_municipio.isin(pop.cd_municipio)]
    qualidade.append({'verificacao':'oscs_ativas_sem_correspondencia_municipal_censo2022','ocorrencias':len(faltantes)})
    proc=root/'dados/tratados'
    salvar(osc,proc/'oscs.csv');salvar(municipios,proc/'municipios.csv')
    salvar(pd.DataFrame(qualidade),proc/'qualidade.csv')
    salvar(faltantes[['cnpj','uf','cd_municipio']],proc/'sem_correspondencia.csv')
    return osc,municipios,pd.DataFrame(qualidade),fonte


def dividir(osc):
    dados=osc[osc.idade_anos.between(0,300) & osc.uf.notna() & osc.natureza_juridica.notna()].copy()
    a,b=next(GroupShuffleSplit(n_splits=1,test_size=.20,random_state=SEED).split(dados,groups=dados.cnpj_raiz))
    restante,teste=dados.iloc[a],dados.iloc[b]
    a,b=next(GroupShuffleSplit(n_splits=1,test_size=.20,random_state=SEED+1).split(restante,groups=restante.cnpj_raiz))
    return restante.iloc[a],restante.iloc[b],teste


def medir(y,pred,prob):
    return {'acuracia':float(accuracy_score(y,pred)),'precisao':float(precision_score(y,pred,zero_division=0)),
            'recall':float(recall_score(y,pred,zero_division=0)),'f1':float(f1_score(y,pred,zero_division=0)),
            'auc_roc':float(roc_auc_score(y,prob)),'ap':float(average_precision_score(y,prob))}


def modelar(osc,root=ROOT):
    treino,val,teste=dividir(osc)
    def pre():
        return ColumnTransformer([('idade',StandardScaler(),['idade_anos']),
            ('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False),['uf','natureza_juridica'])])
    modelos={'Maioria':DummyClassifier(strategy='most_frequent'),
        'Regressao logistica':make_pipeline(pre(),LogisticRegression(class_weight='balanced',max_iter=2000,random_state=SEED)),
        'Arvore':make_pipeline(pre(),DecisionTreeClassifier(max_depth=5,min_samples_leaf=80,class_weight='balanced',random_state=SEED)),
        'Random Forest':make_pipeline(pre(),RandomForestClassifier(n_estimators=150,max_depth=8,min_samples_leaf=40,
                              class_weight='balanced',random_state=SEED,n_jobs=1))}
    def avaliar(frame):
        return pd.DataFrame([{'modelo':nome,**medir(frame.nao_ativa,m.predict(frame[FEATURES]),m.predict_proba(frame[FEATURES])[:,1])}
                             for nome,m in modelos.items()])
    for m in modelos.values():m.fit(treino[FEATURES],treino.nao_ativa)
    metricas_val=avaliar(val)
    escolhido=metricas_val.loc[metricas_val.f1.idxmax(),'modelo']
    combinado=pd.concat([treino,val])
    for m in modelos.values():m.fit(combinado[FEATURES],combinado.nao_ativa)
    metricas_teste=avaliar(teste)
    pred=teste[['cnpj','cnpj_raiz','uf','situacao_cadastral','nao_ativa']].copy()
    pred['previsto']=modelos[escolhido].predict(teste[FEATURES])
    proc=root/'dados/tratados'
    salvar(metricas_val,proc/'metricas_validacao.csv');salvar(metricas_teste,proc/'metricas_teste.csv')
    salvar(pred,proc/'predicoes_teste.csv')
    particoes=pd.concat([f[['cnpj','cnpj_raiz']].assign(conjunto=n) for n,f in [('treino',treino),('validacao',val),('teste',teste)]])
    salvar(particoes,proc/'particoes.csv')
    return metricas_val,metricas_teste,escolhido,pred


def regressao(municipios,root=ROOT):
    dados=municipios[municipios.populacao_2022.gt(0)].copy()
    dados['x']=np.log10(dados.populacao_2022)
    dados['y']=np.log1p(dados.oscs_ativas)
    treino,teste=train_test_split(dados,test_size=.2,random_state=SEED)
    m=LinearRegression().fit(treino[['x']],treino.y)
    pred=m.predict(teste[['x']])
    res={'coeficiente':float(m.coef_[0]),'intercepto':float(m.intercept_),
         'r2_teste_log':float(r2_score(teste.y,pred)),
         'mae_teste_oscs':float(mean_absolute_error(teste.oscs_ativas,np.maximum(0,np.expm1(pred)))),
         'n_treino':len(treino),'n_teste':len(teste)}
    (root/'dados/tratados/regressao.json').write_text(json.dumps(res,indent=2,ensure_ascii=False),encoding='utf-8')
    return treino,teste,m,res


def agrupar(municipios,root=ROOT):
    p=municipios[municipios.oscs_ativas.ge(5)].dropna(subset=['idade_mediana','fracao_fundadas_2010','oscs_por_100mil']).copy()
    p['log_taxa']=np.log1p(p.oscs_por_100mil)
    x=StandardScaler().fit_transform(p[['log_taxa','idade_mediana','fracao_fundadas_2010']])
    fits={};scores=[]
    for k in [2,3,4,5]:
        km=KMeans(n_clusters=k,n_init=20,random_state=SEED).fit(x);fits[k]=km
        scores.append({'k':k,'silhueta':float(silhouette_score(x,km.labels_,sample_size=min(2000,len(p)),random_state=SEED))})
    aval=pd.DataFrame(scores);k=int(aval.loc[aval.silhueta.idxmax(),'k']);p['cluster']=fits[k].labels_
    salvar(p,root/'dados/tratados/perfis_municipios.csv');salvar(aval,root/'dados/tratados/avaliacao_kmeans.csv')
    return p,aval


def sql(osc,municipios,root=ROOT):
    out={}
    with sqlite3.connect(':memory:') as con:
        for n,d in [('oscs',osc.drop(columns=['fundacao'])),('municipios',municipios)]:d.to_sql(n,con,index=False,if_exists='replace')
        for bloco in (root/'sql/consultas.sql').read_text(encoding='utf-8').split('-- CONSULTA ')[1:]:
            nome,q=bloco.split('\n',1);nome=nome.strip();out[nome]=pd.read_sql_query(q,con)
            salvar(out[nome],root/f'resultados/sql/{nome}.csv')
    return out


def graficos(osc,municipios,met,pred,perfis,reg,root=ROOT):
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,
        'axes.titlesize':12,'axes.labelsize':10,'figure.facecolor':'#f4f7fa','axes.facecolor':'white','savefig.facecolor':'#f4f7fa'})
    out=root/'Dashboard';out.mkdir(exist_ok=True)
    def fim(fig,titulo,nome):
        fig.suptitle(titulo,x=.06,y=.98,ha='left',fontsize=19,fontweight='bold',color='#16324f')
        fig.text(.06,.016,'FONTES REAIS: Ipea / Mapa das OSCs (ago. 2026) e IBGE / Censo 2022 | Recorte de assistência social',fontsize=8,color='#475569')
        fig.tight_layout(rect=[.04,.05,.98,.93],h_pad=3,w_pad=3);fig.savefig(out/nome,dpi=160);plt.close(fig)
    fig,axes=plt.subplots(2,2,figsize=(13,8))
    uf=municipios.groupby('uf').oscs_ativas.sum().nlargest(12).sort_values()
    axes[0,0].barh(uf.index,uf,color='#157f82');axes[0,0].set(title='OSCs ativas: 12 UFs com maior contagem',xlabel='Estabelecimentos (CNPJs)')
    status=osc.situacao_cadastral.value_counts().sort_values()
    axes[0,1].barh(status.index,status,color='#725b9e');axes[0,1].set(title='Situação cadastral no recorte completo',xlabel='Estabelecimentos (CNPJs)')
    taxas=municipios.groupby('uf').agg(n=('oscs_ativas','sum'),p=('populacao_2022','sum'))
    taxas['taxa']=taxas.n/taxas.p*100000;top=taxas.taxa.nlargest(12).sort_values()
    axes[1,0].barh(top.index,top,color='#c86b38');axes[1,0].set(title='OSCs ativas por 100 mil habitantes: 12 maiores UFs',xlabel='Contagem 2026 / população 2022 × 100 mil')
    ages=osc.loc[osc.ativa_no_mapa & osc.idade_anos.between(0,120),'idade_anos']
    axes[1,1].hist(ages,bins=24,color='#157f82',edgecolor='white');axes[1,1].set(title='Idade das OSCs ativas (até 120 anos)',xlabel='Anos desde a fundação; referência 31/08/2026',ylabel='Estabelecimentos')
    fim(fig,'Perfil das OSCs de assistência social','01_visao_geral.png')
    fig,axes=plt.subplots(1,2,figsize=(13,5.8));treino,teste,m,r=reg
    axes[0].scatter(treino.x,treino.y,s=9,alpha=.3,label='Treino',color='#157f82')
    axes[0].scatter(teste.x,teste.y,s=10,alpha=.4,label='Teste',color='#c86b38')
    xx=np.linspace(min(treino.x.min(),teste.x.min()),max(treino.x.max(),teste.x.max()),100)
    axes[0].plot(xx,m.predict(pd.DataFrame({'x':xx})),color='#16324f');axes[0].legend(frameon=False)
    axes[0].set(title='População × OSCs ativas por município',xlabel='log10(população residente 2022)',ylabel='ln(1 + OSCs ativas no recorte 2026)')
    previsto=m.predict(teste[['x']]);axes[1].scatter(previsto,teste.y-previsto,s=12,alpha=.4,color='#c86b38');axes[1].axhline(0,color='#16324f',linestyle='--')
    axes[1].set(title=f'Resíduos no teste | R² em log = {r["r2_teste_log"]:.3f}',xlabel='ln(1 + OSCs) previsto',ylabel='Observado − previsto (escala log)')
    fim(fig,'Dispersão e regressão com dados oficiais','02_dispersao_regressao.png')
    fig,axes=plt.subplots(2,2,figsize=(13,8));pos=np.arange(len(met))
    axes[0,0].barh(pos-.17,met.recall,height=.32,label='Recall',color='#157f82');axes[0,0].barh(pos+.17,met.f1,height=.32,label='F1',color='#725b9e')
    axes[0,0].set_yticks(pos,met.modelo);axes[0,0].set(title='Classificar situação não ativa (teste)',xlim=(0,1));axes[0,0].legend(frameon=False)
    cm=confusion_matrix(pred.nao_ativa,pred.previsto,labels=[0,1]);axes[0,1].imshow(cm,cmap='Blues')
    for i in range(2):
        for j in range(2):axes[0,1].text(j,i,str(cm[i,j]),ha='center',va='center',fontsize=15,color='white' if cm[i,j]>cm.max()/2 else '#16324f')
    axes[0,1].set(title='Modelo selecionado na validação',xlabel='Previsto',ylabel='Real',xticks=[0,1],yticks=[0,1],xticklabels=['Ativa','Não ativa'],yticklabels=['Ativa','Não ativa'])
    for c,g in perfis.groupby('cluster'):axes[1,0].scatter(g.idade_mediana,g.oscs_por_100mil,s=13,alpha=.45,label=f'Grupo {c}')
    axes[1,0].set(title='Perfis municipais (mínimo 5 OSCs ativas)',xlabel='Idade mediana das OSCs (anos)',ylabel='OSCs por 100 mil habitantes',yscale='log');axes[1,0].legend(frameon=False,fontsize=8)
    df=osc[osc.uf.eq('DF')].situacao_cadastral.value_counts().sort_values()
    axes[1,1].barh(df.index,df,color='#c86b38');axes[1,1].set(title='Distrito Federal: situação cadastral',xlabel='CNPJs de assistência social no recorte')
    fim(fig,'Modelos exploratórios e recorte do DF','03_modelos.png')


def tabela(frame):
    def f(v):return f'{v:.3f}' if isinstance(v,(float,np.floating)) else str(v)
    return '\n'.join(['| '+' | '.join(frame.columns)+' |','| '+' | '.join(['---']*len(frame.columns))+' |']+
        ['| '+' | '.join(f(v) for v in r)+' |' for r in frame.itertuples(index=False,name=None)])


def relatar(osc,municipios,qualidade,fonte,val,met,escolhido,perfis,aval,reg,root=ROOT):
    tr,va,te=dividir(osc)
    resumo={'origem':'dados reais públicos','oscs_base_original':fonte['linhas_original'],'oscs_assistencia':len(osc),
        'ativas_no_mapa':int(osc.ativa_no_mapa.sum()),'municipios_censo':len(municipios),
        'municipios_com_osc_ativa':int(municipios.oscs_ativas.gt(0).sum()),'oscs_df':int(osc.uf.eq('DF').sum()),
        'classificador_escolhido':escolhido,'n_treino':len(tr),'n_validacao':len(va),'n_teste':len(te),
        'positivos_teste':int(te.nao_ativa.sum()),'k':int(aval.loc[aval.silhueta.idxmax(),'k']),
        'silhueta':float(aval.silhueta.max()),'municipios_clusterizados':len(perfis),'regressao':reg[3]}
    out=root/'resultados';out.mkdir(exist_ok=True)
    (out/'resumo.json').write_text(json.dumps(resumo,indent=2,ensure_ascii=False),encoding='utf-8')
    txt=f'''# Resultados com dados públicos reais

Pergunta: qual é o perfil e a distribuição das OSCs de assistência social e como os
dados cadastrais podem apoiar o planejamento de parcerias do Pescadores Web?

## Fontes e recortes

Ipea/Mapa das OSCs: arquivo oficial 20260806, coleta agosto/2026 conforme portal.
IBGE: Censo 2022, população residente municipal, SIDRA tabela 4714, variável 93.
Extração em 4/11/2026. A fonte integral tem {fonte['linhas_original']:,} CNPJs;
o filtro Area_Assistencia_social = 1 resulta em {len(osc):,} estabelecimentos.
Há {resumo['ativas_no_mapa']:,} CNPJs com situação Ativa e não removidos do Mapa.
São CNPJs de estabelecimentos, incluindo filiais, não necessariamente instituições
independentes. As áreas de atuação podem se sobrepor na base original.

O arquivo integral (343 MB) fica fora do repositório; o recorte exato de linhas e
colunas está em dados/brutos. URLs, filtros e hashes SHA-256 estão em FONTES.json.
Não há observações artificiais, erros inseridos ou preenchimento de valores faltantes
das OSCs. Zeros municipais são contagens obtidas após o cruzamento, não OSCs inventadas.

## Qualidade

{tabela(qualidade)}

O nome municipal do Ipea contém caracteres substituídos em parte das linhas.
Não reconstruímos grafias por palpite: agregações usam código municipal e os nomes
do IBGE. Datas inválidas/futuras ficam fora da modelagem. Linhas sem vínculo municipal
são registradas em sem_correspondencia.csv; não são redistribuídas.

## Distribuição e relação com a população

Dos {len(municipios)} municípios/territórios municipais retornados pelo Censo,
{resumo['municipios_com_osc_ativa']} têm ao menos uma OSC ativa no recorte. O DF tem
{resumo['oscs_df']} estabelecimentos no recorte completo, somando situações cadastrais.
As taxas relacionam numerador 2026 a denominador 2022: não são taxas oficiais de
2026. Contagem e densidade não medem capacidade de atendimento nem necessidade social.

Regressão: ln(1 + OSCs ativas) = {reg[3]['coeficiente']:.4f} × log10(população 2022)
+ {reg[3]['intercepto']:.4f}. Treino: {reg[3]['n_treino']} municípios; teste:
{reg[3]['n_teste']}. R² no teste em escala log: {reg[3]['r2_teste_log']:.3f}; MAE na
escala de contagem após transformação inversa: {reg[3]['mae_teste_oscs']:.2f} OSCs.
No cálculo do MAE, previsões invertidas negativas são limitadas a zero. O gráfico
mostra a reta linear bruta; ela pode extrapolar valores negativos para municípios
pequenos. Modelos próprios para contagens são uma alternativa para a próxima etapa.
É associação transversal, sem causalidade ou previsão de crescimento futuro.

## Classificação cadastral

Alvo positivo: situação diferente de Ativa (Inapta, Suspensa ou Nula ou Baixada).
Características: idade cadastral, UF e natureza jurídica. Situação, remoção,
fechamento, razão social, CNAE e marcador matriz/filial não entram nas características.
É uma demonstração de associação cadastral; a situação real já está disponível
na fonte e deve ser consultada diretamente, sem substituir o cadastro por previsão.

Divisão por raiz do CNPJ (8 dígitos): {len(tr)} treino, {len(va)} validação e {len(te)}
teste, com {int(te.nao_ativa.sum())} positivos. Matriz e filiais não atravessam partições.
Não é teste temporal e não valida previsão de encerramento ou dificuldade financeira.
Modelo escolhido por F1 na validação, antes de usar o teste: **{escolhido}**.

Validação:

{tabela(val)}

Teste após reajuste em treino + validação:

{tabela(met)}

Precisão mede a fração de positivos previstos que se confirmam; recall mede a fração
dos não ativos identificados. AP é average precision. O limiar é fixo em 0,5.
Os resultados têm utilidade didática e não justificam negar parcerias ou atribuir
falhas operacionais a uma organização.

## K-means e aplicação ao TCC

{len(perfis)} municípios com pelo menos cinco OSCs ativas são agrupados por densidade
(log), idade mediana e fração fundada desde 2010. k = {resumo['k']}, silhueta =
{resumo['silhueta']:.3f}. Grupos são exploratórios, sem rótulos de carência ou impacto.

O Pescadores Web pode usar os indicadores para conhecer o contexto territorial e
preparar uma lista de organizações a verificar. O painel pode ser incorporado como
contextualização; não contém doações, estoque, voluntários ou atendimentos da ONG.
Não há integração automática ao Laravel nem mensagens enviadas às organizações.

## Limitações e próxima etapa

Cadastro não comprova funcionamento, capacidade, saúde financeira ou qualidade do
serviço. Há diferença entre datas das fontes, possibilidade de desatualização e
variação de cobertura. Zero no recorte não prova ausência de assistência social.
As divisões aleatórias por grupo não eliminam dependência regional. Revalidar os
indicadores quando a base mudar, guardar os hashes e confirmar informações antes
de estabelecer uma parceria. Para analisar falta de estoque serão necessários
registros operacionais reais; essa previsão foi retirada desta versão.
'''
    (out/'RESULTADOS.md').write_text(txt,encoding='utf-8')
    return resumo


def executar(root=ROOT):
    osc,mun,q,fonte=preparar(root)
    val,met,escolhido,pred=modelar(osc,root)
    reg=regressao(mun,root);perfis,aval=agrupar(mun,root)
    sql(osc,mun,root);graficos(osc,mun,met,pred,perfis,reg,root)
    return relatar(osc,mun,q,fonte,val,met,escolhido,perfis,aval,reg,root)


if __name__=='__main__':print(json.dumps(executar(),indent=2,ensure_ascii=False))
