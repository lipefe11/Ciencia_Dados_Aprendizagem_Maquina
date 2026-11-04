"""Gera os dois PDFs a partir das saídas existentes de analise.py."""
from pathlib import Path
from xml.sax.saxutils import escape
import csv
import json
import textwrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                               TableStyle, PageBreak, Image, Preformatted)

ROOT = Path(__file__).resolve().parents[1]
PAGE = landscape(A4)
INK = colors.HexColor("#16324f")
TEAL = colors.HexColor("#157f82")
STYLES = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=INK, spaceAfter=18),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=TEAL, spaceBefore=10, spaceAfter=9),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=11, leading=16, alignment=TA_LEFT, spaceAfter=10),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=9, leading=12, spaceAfter=7),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9, leading=12),
}


def p(text, style="body"):
    return Paragraph(escape(text).replace("\n", "<br/>"), STYLES[style])


def title(text):
    return p(text, "title")


def tabela(rows, widths=None):
    data = [[p(str(v), "cell") for v in row] for row in rows]
    tab = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    tab.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#deedf0")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f2f5f8")]),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
        ("RIGHTPADDING", (0,0), (-1,-1), 9),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LINEBELOW", (0,0), (-1,0), 1, TEAL),
    ]))
    return tab


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(TEAL)
    canvas.line(42, 32, PAGE[0]-42, 32)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(INK)
    canvas.drawString(42, 19, "Pescadores Web | Dados reais: Ipea / Mapa das OSCs e IBGE / Censo 2022")
    canvas.drawRightString(PAGE[0]-42, 19, str(doc.page))
    canvas.restoreState()


def pdf(path, story):
    path.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(str(path), pagesize=PAGE, leftMargin=42, rightMargin=42,
                      topMargin=32, bottomMargin=44, title=path.stem.replace("_", " "),
                      author="Projeto Pescadores Web").build(story, onFirstPage=rodape, onLaterPages=rodape)


def ler_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def gerar():
    r=json.loads((ROOT/'resultados/resumo.json').read_text(encoding='utf-8'))
    story=[title('Pescadores Web\nPerfil e distribuição das OSCs'),
        p('Análise de Ciência de Dados com fontes públicas reais','h2'),
        p('Pergunta: qual é o perfil e a distribuição das OSCs de assistência social e como os dados cadastrais podem apoiar o planejamento de parcerias?'),
        p('Fontes: Ipea / Mapa das OSCs, coleta agosto/2026, e IBGE / Censo Demográfico 2022, população municipal. Extração em 4 de novembro de 2026. Não se utilizam registros artificiais de doações ou estoque.'),
        tabela([['Recorte de CNPJs','Ativas no Mapa','Municípios do Censo','CNPJs no DF'],
                [r['oscs_assistencia'],r['ativas_no_mapa'],r['municipios_censo'],r['oscs_df']]],[189]*4),
        Spacer(1,16),p('CNPJs representam estabelecimentos, incluindo filiais. Situação cadastral não mede capacidade, qualidade, saúde financeira ou necessidade social. O documento original do TCC foi preservado.'),
        PageBreak(),title('Procedência, preparação e avaliação'),
        p('A base integral do Ipea tem 1.113.949 registros. O filtro Area_Assistencia_social = 1 seleciona 58.184 estabelecimentos; 11 colunas são preservadas. O JSON do Censo contém 5.570 municípios. Filtro, URLs e hashes SHA-256 ficam em dados/brutos/FONTES.json.'),
        tabela([['Fase CRISP-DM','Aplicação'],['Negócio','Contextualizar o setor para o planejamento de parcerias.'],
            ['Dados','Microdados reais do Ipea e população municipal real do IBGE.'],
            ['Preparação','Validar chaves, datas, UF e junção por código municipal. Sem imputar OSCs.'],
            ['Modelagem','Regressão em log, K-means e classificação com baseline.'],
            ['Avaliação','Regressão: teste municipal; classificação: raízes de CNPJ disjuntas.'],
            ['Implementação','Painel de contexto; confirmar organizações nas fontes antes de parceria.']],[135,620]),
        Spacer(1,12),p('Nomes municipais parcialmente corrompidos na fonte são preservados no arquivo bruto. Os nomes usados na agregação vêm do IBGE, por junção de código. A taxa combina contagem de 2026 com população de 2022, sem ser uma taxa oficial de 2026.','small'),
        PageBreak(),title('Perfil e distribuição territorial'),Image(str(ROOT/'Dashboard/01_visao_geral.png'),width=715,height=440),
        PageBreak(),title('Dispersão e regressão linear'),Image(str(ROOT/'Dashboard/02_dispersao_regressao.png'),width=755,height=337),
        p(f"R² do teste em escala log: {r['regressao']['r2_teste_log']:.3f}. MAE após transformação inversa: {r['regressao']['mae_teste_oscs']:.2f} OSCs. Associação transversal entre população e contagem; não demonstra causalidade ou crescimento futuro.",'small'),
        PageBreak(),title('Classificação e interpretação dos resultados'),
        p(f"Alvo: situação diferente de Ativa. Preditores: idade cadastral, UF e natureza jurídica. Treino: {r['n_treino']}; validação: {r['n_validacao']}; teste: {r['n_teste']}. Matriz e filiais da mesma raiz não atravessam partições. Escolha pelo F1 na validação: {r['classificador_escolhido']}."),
        p('Resultado no teste reservado, após reajuste em treino + validação:'),]
    rows=ler_csv(ROOT/'dados/tratados/metricas_teste.csv')
    rows[0]=['Modelo','Acurácia','Precisão','Recall','F1','ROC-AUC','AP']
    story += [tabela([[v if i==0 or j==0 else f'{float(v):.3f}' for j,v in enumerate(row)] for i,row in enumerate(rows)],[170]+[97.5]*6),
        Spacer(1,12),p('A situação cadastral observada já está na fonte e deve ser consultada diretamente. O modelo é um exercício metodológico, não uma previsão de encerramento, dificuldade financeira ou capacidade de atendimento. O teste não é temporal.'),
        p('Precisão: positivos previstos confirmados. Recall: não ativas identificadas. F1 combina ambos. AP é average precision. A acurácia da maioria ilustra por que é necessário comparar métricas.','small'),
        PageBreak(),title('Modelos e recorte do Distrito Federal'),Image(str(ROOT/'Dashboard/03_modelos.png'),width=715,height=440),
        PageBreak(),title('Conclusões, limites e fontes'),
        p(f"Dos {r['municipios_censo']} municípios do Censo, {r['municipios_com_osc_ativa']} têm ao menos uma OSC ativa no recorte. Há {r['oscs_df']} CNPJs no Distrito Federal, incluindo as diferentes situações cadastrais. A contagem não comprova disponibilidade de serviços."),
        p(f"K-means: {r['municipios_clusterizados']} municípios com ao menos cinco OSCs ativas; k = {r['k']}, silhueta {r['silhueta']:.3f}. Os grupos são exploratórios, sem rótulos de carência ou impacto."),
        p('Próxima etapa: verificar potenciais parceiros nas fontes, atualizar as datas e acompanhar a completude cadastral. Para analisar falta de estoque são necessários registros reais de movimentações e demanda, ausentes dessas bases. Não existe integração automática ao Laravel.'),
        p('Fontes oficiais e referências','h2'),
        p('Ipea: mapaosc.ipea.gov.br/base-dados; arquivo 20260806_MOSC_baseDivulgacao.csv. IBGE: apisidra.ibge.gov.br/values/t/4714/n6/all/v/93/p/2022. Extração em 4/11/2026. URLs completas e SHA-256 em FONTES.json.','small'),
        p('Contextualização: artigo HYB Panorama das ONGs no Brasil (9/4/2026) e publicação institucional do IDIS sobre Panorama das ONGs (20/1/2026). Não são as fontes dos registros analisados. Referências completas em docs/REFERENCIAS.md.','small')]
    pdf(ROOT/'docs/Pescadores_Web_Analise.pdf',story)
    story=[title('Pescadores Web\nConsultas SQL com dados reais'),
        p('Oito consultas SQLite sobre o recorte real de assistência social do Ipea e população municipal do IBGE. As tabelas completas estão em resultados/sql/.'),
        p('Tabelas extensas são mostradas parcialmente para preservar a legibilidade. O banco MySQL do TCC não é acessado ou alterado.'),PageBreak()]
    blocos=(ROOT/'sql/consultas.sql').read_text(encoding='utf-8').split('-- CONSULTA ')[1:]
    for i,bloco in enumerate(blocos):
        nome,q=bloco.split('\n',1);nome=nome.strip()
        story += [title(nome.replace('_',' ')),Preformatted(q.strip(),ParagraphStyle('code',fontName='Courier-Bold',fontSize=9,leading=12,textColor=INK)),Spacer(1,16)]
        rows=ler_csv(ROOT/f'resultados/sql/{nome}.csv')
        story += [tabela(rows[:11],[755/len(rows[0])]*len(rows[0])),Spacer(1,8),p(f'Exibidas {min(10,len(rows)-1)} de {len(rows)-1} linhas. Arquivo completo: resultados/sql/{nome}.csv','small')]
        if i<len(blocos)-1:story.append(PageBreak())
    pdf(ROOT/'docs/Pescadores_Web_Consultas_SQL.pdf',story)

if __name__=='__main__':
    gerar()
    print('PDFs com dados reais gerados.')
