# -*- coding: utf-8 -*-

import sys, time
try:
   from urllib.request import Request, build_opener
except:
   from urllib2 import Request as Request
   from urllib2 import build_opener
from xml.dom import minidom
from multiprocessing import Pool, freeze_support

stocks = ['ABEV3','BBAS3','BBDC3','BBDC4','BBSE3','BRAP4','BRFS3','BRKM5','BRML3','BRPR3',
          'BVMF3','CCRO3','CESP6','CIEL3','CMIG4','CPFE3','CPLE6','CRUZ3','CSAN3','CSNA3',
          'CTIP3','CYRE3','DTEX3','ECOR3','ELET3','ELET6','EMBR3','ENBR3','ESTC3','FIBR3',
          'GFSA3','GGBR4','GOAU4','GOLL4','HGTX3','HYPE3','ITSA4','ITUB4','JBSS3','KLBN11',
          'KROT3','LAME4','LREN3','MRFG3','MRVE3','MULT3','NATU3','OIBR4','PCAR4','PETR3',
          'PETR4','POMO4','QUAL3','RENT3','RUMO3','SANB11','SBSP3','SMLE3','SUZB5','TBLE3',
          'TIMP3','UGPA3','USIM5','VALE3','VALE5','VIVT4']

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
    return [code, name, atualizacao, abertura, minimo, maximo, ultimo, oscilacao]

def terminal_print():
    pool = Pool(len(stocks))
    contrib = pool.map(getStock, stocks)
    for istock, (code, name, atualizacao, abertura, minimo, maximo, ultimo, oscilacao) in zip(stocks, contrib):
        print(("%s %s -> ultima cotacao: %s " % (code, name, ultimo)))

if __name__ == '__main__':
    start = time.strftime("%d %b %Y %H:%M:%S (UTC)", time.gmtime())
    print('Start %s' % start)
    if sys.platform == "win32":
        freeze_support()
    terminal_print()
    finish = time.strftime("%d %b %Y %H:%M:%S (UTC)", time.gmtime())
    print('Finished %s' % finish)

