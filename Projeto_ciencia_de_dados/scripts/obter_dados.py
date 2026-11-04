"""Obtém dados públicos oficiais, sem gerar observações artificiais."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import tempfile
import urllib.request
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OSCS = 'https://mapaosc.ipea.gov.br/download/20260806_MOSC_baseDivulgacao.csv'
IBGE = 'https://apisidra.ibge.gov.br/values/t/4714/n6/all/v/93/p/2022'
PAGINA = 'https://mapaosc.ipea.gov.br/base-dados'
COLS = ['cnpj','tx_razao_social_osc','natureza_juridica','matriz_filial',
        'situacao_cadastral','dt_fundacao_osc','removida_do_mosc',
        'cd_municipio','municipio_nome','UF_Sigla','Area_Assistencia_social']


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()


def obter(arquivo_osc=None, arquivo_ibge=None, root=ROOT):
    raw=root/'dados/brutos'
    raw.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        original=Path(arquivo_osc) if arquivo_osc else Path(tmp)/'mapaosc.csv'
        if not arquivo_osc: urllib.request.urlretrieve(OSCS,original)
        total=0
        partes=[]
        for chunk in pd.read_csv(original,sep=';',dtype=str,usecols=COLS,
                                 encoding='utf-8',encoding_errors='replace',chunksize=100000):
            total+=len(chunk)
            partes.append(chunk.loc[chunk.Area_Assistencia_social.eq('1'),COLS])
        recorte=pd.concat(partes,ignore_index=True)
        # Apenas seleção de linhas e colunas; valores não são gerados nem imputados.
        destino=raw/'oscs_assistencia_social_20260806.csv'
        recorte.to_csv(destino,index=False,lineterminator='\n')
        pop=raw/'populacao_ibge_2022.json'
        if arquivo_ibge: shutil.copyfile(arquivo_ibge,pop)
        else: urllib.request.urlretrieve(IBGE,pop)
        registros=json.loads(pop.read_text(encoding='utf-8-sig'))
        assert registros[1]['D2N']=='População residente'
        manifesto={'origem':'dados públicos observados; sem simulação',
            'fonte_osc':OSCS,'pagina_fonte_osc':PAGINA,'fonte_populacao':IBGE,
            'periodo_osc':'Coleta agosto/2026, conforme portal; arquivo 20260806',
            'periodo_populacao':'Censo Demográfico 2022, SIDRA tabela 4714, variável 93',
            'extraido_em':'2026-11-04','separador_original':';','encoding':'UTF-8 com substituição de caracteres inválidos já existentes na fonte',
            'filtro':"Area_Assistencia_social == '1'",'colunas_retidas':COLS,
            'linhas_original':total,'linhas_recorte':len(recorte),
            'sha256_original_osc':sha(original),'sha256_recorte_osc':sha(destino),
            'sha256_populacao':sha(pop),'bytes_original_osc':original.stat().st_size}
        (raw/'FONTES.json').write_text(json.dumps(manifesto,ensure_ascii=False,indent=2),encoding='utf-8')
    return manifesto


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--arquivo-osc',type=Path)
    parser.add_argument('--arquivo-ibge',type=Path)
    args=parser.parse_args()
    print(json.dumps(obter(args.arquivo_osc,args.arquivo_ibge),ensure_ascii=False,indent=2))
