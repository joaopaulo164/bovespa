# -*- coding: utf-8 -*-

try:
   from urllib.request import Request, build_opener
except:
   from urllib2 import Request as Request
   from urllib2 import build_opener
from xml.dom import minidom
import time

stocks = ['RUMO3','BBAS3','SMLE3','MRVE3','BBSE3','JBSS3','WEGE3','ITSA4','TBLE3','BBDC3',
          'CESP6','CCRO3','CPFE3','HGTX3','CYRE3','ITUB4','ESTC3','ENBR3','BVMF3','BBDC4',
          'OIBR4','RADL3','CIEL3','MULT3','CMIG4','EQTL3','NATU3','HYPE3','VIVT4','PETR4',
          'SBSP3','BRML3','LREN3','CSAN3','PCAR4','KROT3','LAME4','BRFS3','UGPA3','MRFG3',
          'ECOR3','ABEV3','SANB11','GGBR4','GOAU4','EMBR3','CTIP3','RENT3','USIM5','QUAL3',
          'CPLE6','PETR3','TIMP3','BRKM5','KLBN11','SUZB5','BRAP4','FIBR3','CSNA3','VALE5',
          'VALE3','BRPR3','DTEX3','ELET3','ELET6','GFSA3','GOLL4','POMO4']

def getStock(istock):
    url = 'http://www.bmfbovespa.com.br/Pregao-Online/ExecutaAcaoAjax.asp?intEstado=1&CodigoPapel=%s' % istock
    req = Request(url)
    req.add_header("User-Agent", 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0')
    opener = build_opener()
    site = opener.open(req).read()
    xmldoc = minidom.parseString(site)
    x = xmldoc.getElementsByTagName('Papel')
    for i in x:
        code        = i.attributes['Codigo'].value
        name        = i.attributes['Nome'].value
        atualizacao = i.attributes['Data'].value
        abertura    = i.attributes['Abertura'].value.replace(',','.')
        minimo      = i.attributes['Minimo'].value.replace(',','.')
        maximo      = i.attributes['Maximo'].value.replace(',','.')
        ultimo      = i.attributes['Ultimo'].value.replace(',','.')
        oscilacao   = i.attributes['Oscilacao'].value.replace(',','.')
    print(("%s %s -> ultima cotacao: %s " % (code, name, ultimo)))

def terminal_print():
    for i in stocks:
        getStock(i)
        
if __name__ == '__main__':
    start = time.strftime("%d %b %Y %H:%M:%S (UTC)", time.gmtime())
    print('Start %s' % start)
    terminal_print()
    finish = time.strftime("%d %b %Y %H:%M:%S (UTC)", time.gmtime())
    print('Finished %s' % finish)
