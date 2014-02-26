import datetime
def fator_vencimento(date):
 return(str((datetime.datetime.strptime(date, '%d/%m/%Y').date() - datetime.datetime.strptime('07/10/1997', '%d/%m/%Y').date()).days))

def valorpag(vlr):
 return(vlr.replace('.','').replace(',','').rjust(10,'0'))

def modulo_11(num, base=9, r=0):
 soma=0
 fator=2
 for i in range(len(num)-1,-1,-1):
  soma+=int(num[i])*fator
  if (fator==base):
   fator = 1
  fator+=1
 if (r==0):
  soma*=10
  digito = soma % 11;
  if (digito == 10):
   digito = 0
  return(str(digito))
 else:
  return(str(soma % 11))

def digitoVerificador_barra(numero):
 resto = int(modulo_11(numero,9,1))
 if (resto == 0 or resto == 1 or resto == 10):
  dv = 1
 else:
  dv = 11 - resto
 return(str(dv))


def modulo_10(num):        
 mult = 2
 sum = 0
 for i in range(len(num)-1, -1, -1):
  x = (int(num[i]) * mult)
  if(x >= 10):
   x = (x % 10) + 1
  sum += x
  if(mult == 2):
   mult = 1
  else:
   mult = 2
 if(not (sum % 10)):
  sum = 0
 else:
  sum = 10 - (sum % 10)
 return(str(sum))


def monta_linha_digitavel(codigo):
 campo1 = codigo[0:3] + codigo[3] + codigo[19] + codigo[20:24]
 campo1 = campo1 + modulo_10(campo1)
 campo2 = codigo[24:34]
 campo2 = campo2 + modulo_10(campo2)
 campo3 = codigo[34:44]
 campo3 = campo3 + modulo_10(campo3)
 campo4 = codigo[4]
 campo5 = codigo[5:9]+codigo[9:19]
 return(campo1+campo2+campo3+campo4+campo5)

codigobanco = '033'
fixo = '9'
nummoeda = '9'
ios = '0'
fatorvencimento=fator_vencimento('dd/mm/2014')
valor=valorpag('70,00')
carteira='102'
codigocliente='<meu codigo>'
nnum='<serial de boletos>'
nossonumero=(nnum+modulo_11(nnum)).rjust(13,'0')


barra = codigobanco+nummoeda+fatorvencimento+valor+fixo+codigocliente+nossonumero+ios+carteira
barra = barra[:4]+digitoVerificador_barra(barra)+barra[4:]
def exibe(barra):
 print(barra)
 print(barra[0:5]+'.'+barra[5:10]+' '+barra[10:15]+'.'+barra[15:21]+' '+barra[21:26]+'.'+barra[26:32]+' '+barra[32]+' '+barra[33:])

exibe(monta_linha_digitavel(barra))

