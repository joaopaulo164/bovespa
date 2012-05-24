# -*- coding: utf-8 -*-

import urllib2
from xml.dom import minidom

acao = ['PETR4', 'BBDC4', 'OGXP3']

for y in acao:
    url = 'http://www.bmfbovespa.com.br/Pregao-Online/ExecutaAcaoAjax.asp?intEstado=1&CodigoPapel=%s' % y
    request = urllib2.Request(url)
    request.add_header("User-Agent", 'Mozilla/13.0')
    opener = urllib2.build_opener()
    site = opener.open(request).read()
    xmldoc = minidom.parseString(site)
    x = xmldoc.getElementsByTagName('Papel')
    for i in x:
        codigo     = i.attributes['Codigo'].value
        nome       = i.attributes['Nome'].value
        data_atual = i.attributes['Data'].value
        abertura   = i.attributes['Abertura'].value.replace(',','.')
        minimo     = i.attributes['Minimo'].value.replace(',','.')
        maximo     = i.attributes['Maximo'].value.replace(',','.')
        atual      = i.attributes['Ultimo'].value.replace(',','.')
        oscilacao  = i.attributes['Oscilacao'].value.replace(',','.')
        
        print u'Código: %s' % codigo
        print u'Nome: %s' % nome
        print u'Última atualização: %s' % data_atual
        print u'Abertura: %s' % abertura
        print u'Mínimo: %s' % minimo
        print u'Máximo: %s' % maximo
        print u'Atual: %s' % atual
        print u'Oscilação: %s' % oscilacao
        print ''

raw_input()
