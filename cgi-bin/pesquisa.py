#!/usr/local/bin/python3
import cgi
import cgitb
import time
cgitb.enable()
arguments = cgi.FieldStorage()

import postgresql
import subprocess
import os
def ping(ip):
  with open(os.devnull, "wb") as limbo:
   return(subprocess.Popen(["ping", "-w", "2", "-n", "1", ip],stdout=limbo, stderr=limbo).wait()==0)
##   return(subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],stdout=limbo, stderr=limbo).wait()==0)


print("Content-Type: text/plain;charset=utf-8")
print("")
print(time.strftime("%d/%m/%Y")+" "+time.strftime("%I:%M:%S"))
##time.sleep(10)
db = postgresql.open("pq://postgres@<IP>/mkData")
dbresult=db.query("""
SELECT
 mp.codpessoa,
 mp.nome_razaosocial,
 mp.fone01,
 mp.fone02,
 mp.fax,
 mc.codconexao,
 mc.username,
 mc.password,
 mc.mac_address_considerado,
 mc.cd_assinante,
 mc.conexao_bloqueada,
 mc.contrato,
 mc.codplano_acesso,
 mti.numero_ip,
 mpa.ssid,
 mpa.nas_address,
 mpa.localizacao,
 mpa.responde_pelo_servidor,
 mpa.longitude,
 mpa.latitude,
 mpa.endereco,
 mpa.cidade,
 mpa.porta_api,
 mpa.bairro,
 ms.descricao,
 ms.localizacao,
 ms.acesso_user,
 ms.acesso_password,
 ms.ip_comunicacao,
 ms.porta_api,
 mmb.descricao,
 mpla.descricao,
 'nao testado' as teste_ip_mc,
 'nao testado' as teste_ip_mpa,
 'nao testado' as teste_ip_ms
FROM mk_pessoas mp
LEFT JOIN mk_conexoes mc
ON mp.codpessoa = mc.codcliente
LEFT JOIN mk_tabela_ips mti
ON mc.codendereco_ip = mti.codip
LEFT JOIN mk_pontos_acesso mpa
ON mc.codponto_acesso = mpa.codpontoacesso
LEFT JOIN mk_servidores ms
ON mc.codservidor = ms.codmovimento
LEFT JOIN mk_motivos_bloqueio mmb
ON mc.motivo_bloqueio = mmb.codmotbloq
LEFT JOIN mk_planos_acesso mpla
ON mc.codplano_acesso = mpla.codplano

"""+"WHERE fone01 like '%"+arguments['tel'].value[-8:]+"' or mc.contrato = 0" + arguments['contrato'].value + " or fone02 like '%"+arguments['tel'].value[-8:]+"' or fax like '%"+arguments['tel'].value[-8:]+"'")

label = ("codpessoa", "nome_razaosocial", "fone01", "fone02", "fax", "codconexao", "username", "password", "mac_address_considerado", "cd_assinante", "conexao_bloqueada", "contrato", "codplano_acesso", "numero_ip", "ssid", "nas_address", "localizacao", "responde_pelo_servidor", "longitude", "latitude", "endereco", "cidade", "porta_api", "bairro", "descricao_servidor", "localizacao", "acesso_user", "acesso_password", "ip_comunicacao", "porta_api", "mod_bloqueio", "plano", "teste_ip_mc","teste_ip_mpa","teste_ip_ms")
tabela = []
for x in dbresult:
 tabela.append(dict(zip(label,x)))

for linha in tabela:
 if isinstance(linha['numero_ip'],str): linha['teste_ip_mc']='ok' if ping(linha['numero_ip'].strip()) else 'fora'
 if isinstance(linha['nas_address'],str): linha['teste_ip_mpa']='ok' if ping(linha['nas_address'].strip()) else 'fora'
 if isinstance(linha['ip_comunicacao'],str): linha['teste_ip_ms']='ok' if ping(linha['ip_comunicacao'].strip()) else 'fora'
 for coluna in linha:
  if isinstance(linha[coluna],str): linha[coluna]=linha[coluna].strip()

import dicttoxml
f = open(arguments['ramal'].value+'.xml','w')
f.truncate()
f.write('<?xml version="1.0" encoding="UTF-8" ?>')
f.write('<root>')
f.write('<tabela>')
f.write(dicttoxml.dicttoxml(tabela,False))
f.write('</tabela>')
f.write("<controle>")
f.write("<ramal>"+arguments['ramal'].value+"</ramal>")
f.write("<tel>"+arguments['tel'].value+"</tel>")
f.write("<contrato>"+arguments['contrato'].value+"</contrato>")
f.write("<data_hora>"+time.strftime("%d/%m/%Y")+" "+time.strftime("%I:%M:%S")+"</data_hora>")
f.write("</controle>")
f.write('</root>')
f.close()
print(time.strftime("%d/%m/%Y")+" "+time.strftime("%I:%M:%S"))
print("OK")
