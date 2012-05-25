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
        print u'Código: %s ' % i.attributes['Codigo'].value
        print u'Nome: %s ' % i.attributes['Nome'].value
        print u'Última atualização: %s ' % i.attributes['Data'].value
        print u'Abertura: %s ' % i.attributes['Abertura'].value.replace(',','.')
        print u'Mínimo: %s ' % i.attributes['Minimo'].value.replace(',','.')
        print u'Máximo: %s ' % i.attributes['Maximo'].value.replace(',','.')
        print u'Atual: %s ' % i.attributes['Ultimo'].value.replace(',','.')
        print u'Oscilação: %s ' % i.attributes['Oscilacao'].value.replace(',','.')
        print ''
