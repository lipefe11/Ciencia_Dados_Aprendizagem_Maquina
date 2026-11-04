from pathlib import Path
import hashlib
import json
import sys
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import analise as a


class TestDadosReais(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.osc,cls.mun,cls.qualidade,cls.fonte=a.preparar()

    def test_integridade_das_fontes(self):
        for nome,campo in [('oscs_assistencia_social_20260806.csv','sha256_recorte_osc'),
                            ('populacao_ibge_2022.json','sha256_populacao')]:
            h=hashlib.sha256((a.ROOT/'dados/brutos'/nome).read_bytes()).hexdigest()
            self.assertEqual(h,self.fonte[campo])

    def test_recorte_e_chaves(self):
        raw=pd.read_csv(a.ROOT/'dados/brutos/oscs_assistencia_social_20260806.csv',dtype=str)
        self.assertEqual(len(raw),self.fonte['linhas_recorte'])
        self.assertTrue(raw.Area_Assistencia_social.eq('1').all())
        self.assertTrue(self.osc.cnpj.is_unique)
        self.assertEqual(len(raw),len(self.osc))

    def test_grupos_disjuntos(self):
        tr,va,te=a.dividir(self.osc)
        grupos=[set(f.cnpj_raiz) for f in [tr,va,te]]
        self.assertFalse(grupos[0]&grupos[1]);self.assertFalse(grupos[0]&grupos[2]);self.assertFalse(grupos[1]&grupos[2])
        for f in [tr,va,te]: self.assertEqual(set(f.nao_ativa),{0,1})
        self.assertEqual(a.FEATURES,['idade_anos','uf','natureza_juridica'])

    def test_contagens_e_populacao(self):
        ativas=self.osc[self.osc.ativa_no_mapa]
        correspondentes=ativas[ativas.cd_municipio.isin(self.mun.cd_municipio)]
        self.assertEqual(int(self.mun.oscs_ativas.sum()),len(correspondentes))
        self.assertTrue(self.mun.cd_municipio.is_unique)
        self.assertTrue(self.mun.populacao_2022.gt(0).all())
        np.testing.assert_allclose(self.mun.oscs_por_100mil,
            self.mun.oscs_ativas/self.mun.populacao_2022*100000)

    def test_alvo_observado(self):
        np.testing.assert_array_equal(self.osc.nao_ativa,self.osc.situacao_cadastral.ne('Ativa').astype(int))
        self.assertEqual(set(self.osc.situacao_cadastral),{'Ativa','Inapta','Suspensa','Nula ou Baixada'})

    def test_sql_por_uf_conserva_contagens(self):
        consultas=a.sql(self.osc,self.mun)
        por_uf=consultas['02_ativas_por_uf']
        self.assertEqual(len(por_uf),27)
        self.assertEqual(int(por_uf.oscs_ativas.sum()),int(self.mun.oscs_ativas.sum()))


if __name__=='__main__':unittest.main()
