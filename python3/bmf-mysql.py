# -*- coding: utf-8 -*-
# use python27

import sys
import urllib.request, urllib.error, urllib.parse
from xml.dom import minidom
from multiprocessing import Pool, freeze_support

import MySQLdb
from datetime import datetime
from time import sleep
from getpass import getpass


stocks = ['ABEV3','BBAS3','BBDC3','BBDC4','BBSE3','BRAP4','BRFS3','BRKM5','BRML3','BRPR3',
          'BVMF3','CCRO3','CESP6','CIEL3','CMIG4','CPFE3','CPLE6','CRUZ3','CSAN3','CSNA3',
          'CTIP3','CYRE3','DTEX3','ECOR3','ELET3','ELET6','EMBR3','ENBR3','ESTC3','FIBR3',
          'GFSA3','GGBR4','GOAU4','GOLL4','HGTX3','HYPE3','ITSA4','ITUB4','JBSS3','KLBN11',
          'KROT3','LAME4','LREN3','MRFG3','MRVE3','MULT3','NATU3','OIBR4','PCAR4','PETR3',
          'PETR4','POMO4','QUAL3','RENT3','RUMO3','SANB11','SBSP3','SMLE3','SUZB5','TBLE3',
          'TIMP3','UGPA3','USIM5','VALE3','VALE5','VIVT4']

def getStock(istock):
    url = 'http://www.bmfbovespa.com.br/Pregao-Online/ExecutaAcaoAjax.asp?intEstado=1&CodigoPapel=%s' % istock
    request = urllib.request.Request(url)
    request.add_header("User-Agent", 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0')
    opener = urllib.request.build_opener()
    site = opener.open(request).read()
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

def mysql_save():
    HOSTNAME = input("Hostname: ")
    USERNAME = input("Username: ")
    PASSWORD = getpass("Senha: ")
    DATABASE = input("Database: ")
    
    try:
        db = MySQLdb.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD, db=DATABASE)
    except MySQLdb.Error as e:
        raise e
    
    try:
        cursor = db.cursor()
        cursor.execute("SHOW TABLES LIKE 'stock';")
        rows = cursor.fetchone()
        if rows == None: 
            cursor.execute("""
                create table `stock` (
                    `code` VARCHAR(50) NOT NULL,
                    `dh_consulta` VARCHAR(50) NOT NULL,
                    `name` VARCHAR(50),
                    `atualizacao` VARCHAR(50), 
                    `abertura` VARCHAR(50), 
                    `minimo` VARCHAR(50), 
                    `maximo` VARCHAR(50), 
                    `ultimo` VARCHAR(50), 
                    `oscilacao` VARCHAR(50), 
                    primary key (`code`, `dh_consulta`)
                )""")
            db.commit()
    except MySQLdb.Error as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()

    if sys.platform == "win32":
        freeze_support()
    pool = Pool(len(stocks))
    contrib = pool.map(getStock, stocks)
    
    try:
        db = MySQLdb.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD, db=DATABASE)
    except MySQLdb.Error as e:
        raise e

    try:
        cursor = db.cursor()
        dh_consulta = datetime.now()

        for istock, (code, name, atualizacao, abertura, minimo, maximo, ultimo, oscilacao) in zip(stocks, contrib):
            cursor.execute("insert into `stock` (`code`,`dh_consulta`,`name`,`atualizacao`,"+
                           "`abertura`,`minimo`,`maximo`,`ultimo`,`oscilacao`) "+
                           "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                           (code, dh_consulta, name, atualizacao, abertura, minimo, maximo, ultimo, oscilacao))
            db.commit()
            
        print(("Atualizado em %s" % dh_consulta))

    except MySQLdb.Error as e:
        db.rollback()
        raise e

    finally:
        cursor.close()
        db.close()
        
if __name__ == '__main__':
    if sys.platform == "win32":
        freeze_support()
    mysql_save()
