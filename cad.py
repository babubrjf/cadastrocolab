# imports e misc
import time
from tabulate import tabulate
from google.colab import output
from google.auth import default
from google.colab import auth
import gspread
import pandas as pd

auth.authenticate_user()
creds, _ = default()
usuario = gspread.authorize(creds)

spreadsheet = usuario.open('sistema_translogistica')
worksheet0 = spreadsheet.get_worksheet(0)
worksheet1 = spreadsheet.get_worksheet(1)
worksheet2 = spreadsheet.get_worksheet(2)
worksheet3 = spreadsheet.get_worksheet(3)
worksheet4 = spreadsheet.get_worksheet(4)

# Função da tela inicial
def tela():
  output.clear()
  op = 1
  while op:
    print("1. Entrar")
    print("2. Cadastrar")
    print("0. Sair do sistema")
    op = int(input("Escolha uma das opções acima:"))

    if(op==1):
      login()
    if(op==2):
      nlogin()
    if(op==0):
      raise SystemExit
  
# Função de novo login & login existente
def login():
  output.clear()
  dados = worksheet4.get_all_values()
  user = input("Usuário: ")
  while True:
    try:
      posi = worksheet4.find(user)
      linha = posi.row
      break
    except gspread.CellNotFound:
      print("Usuário não encontrado!")
      time.sleep(3)
      output.clear()
      user = input("Usuário: ")
  senha = input("Senha: ")
  senhas = worksheet4.row_values(linha)
  time.sleep(3)
  output.clear()
  while senha not in senhas:
    print("Senha incorreta! Tente novamente.")
    time.sleep(3)
    output.clear()
    senha = input("Senha: ")
  nivel = worksheet4.cell(linha,7).value
  worksheet3.update_cell(2,4,user)
  if nivel == "ADMIN":
    menuadm()
  if nivel == "USUARIO":
    menuser()
  if nivel == "MOTORISTA":
    menumot()

def nlogin():
  output.clear()
  dados = worksheet4.get_all_values()
  if len(dados) == 0:
    cod = int(worksheet3.cell(2,3).value)
  else:
    cod = int(worksheet3.cell(2,3).value) + 1
  user = input("Digite o nome de usuário: ")
  users = worksheet4.col_values(2)
  while user in users:
    print("Esse nome de usuário já está sendo usado!")
    time.sleep(3)
    output.clear()
    user = input("Digite outro nome de usuário: ")
  senha = input("Digite a senha: ")
  nome = input("Digite seu nome (Ex: JOÃO DIAS): ")
  cnh = input("Digite sua CNH (11 dígitos): ")
  fone = input("Digite o telefone - (Ex: (XX)XXXXX-XXXX): ")
  nivel = "USUARIO"

  nLogin = [cod, user, senha, nome, cnh, fone, nivel]
  worksheet4.append_row(nLogin)
  worksheet3.update_cell(2,3,cod)

  print("Usuário cadastrado com sucesso!")
  time.sleep(3)
  output.clear()
  
# Função dos menus
def menuadm():
  output.clear()
  menu = 1
  while menu:
    print("=============== SISTEMA TRANSLOGÍSTICA ===============")
    print("1. Cadastrar início de viagem")
    print("2. Cadastrar fim de viagem")
    print("3. Cadastrar novo motorista")
    print("4. Listar viagens")
    print("5. Listar motoristas cadastrados")
    print("6. Listar valores")
    print("7. Atualizar cadastro de motoristas")
    print("8. Atualizar login de usuarios")
    print("9. Excluir cadastros")
    print("10. Excluir viagens")
    print("0. Log out")
    menu = int(input("Escolha uma das opções acima:"))

    if(menu==1):
      novaViagem()
    if(menu==2):
      fimViagem()
    if(menu==3):
      novoCadastro()
    if(menu==4):
      listaViagens()
    if(menu==5):
      listaCadastros()
    if(menu==6):
      listaValores()
    if(menu==7):
      attCadastro()
    if(menu==8):
      attLogin()
    if(menu==9):
      delCadastro()
    if(menu==10):
      delViagem()
    if(menu==0):
      tela()

def menuser():
  output.clear()
  menu = 1
  while menu:
    print("=============== SISTEMA TRANSLOGÍSTICA ===============")
    print("1. Listar viagens")
    print("2. Listar motoristas livres")
    print("3. Listar valores")
    print("0. Log out")
    menu = int(input("Escolha uma das opções acima:"))

    if(menu==1):
      listaViagens()
    if(menu==2):
      listaCadastros()
    if(menu==3):
      listaValores()
    if(menu==0):
      tela()

def menumot():
  output.clear()
  menu = 1
  while menu:
    print("=============== SISTEMA TRANSLOGÍSTICA ===============")
    print("1. Listar minhas viagens")
    print("2. Listar meu cadastro")
    print("3. Listar valores")
    print("0. Log out")
    menu = int(input("Escolha uma das opções acima:"))

    if(menu==1):
      listaViagensM()
    if(menu==2):
      listaCadastrosM()
    if(menu==3):
      listaValores()
    if(menu==0):
      tela()
      
# Função para adicionar ou atualizar um registro na planilha
def novaViagem():
  output.clear()
  dados = worksheet0.get_all_values()
  if len(dados) == 0:
    cod = int(worksheet3.cell(2,1).value)
  else:
    cod = int(worksheet3.cell(2,1).value) + 1
  cadastros = worksheet1.get_all_values()
  print(tabulate(cadastros, headers=["CÓDIGO","VEÍCULO","PLACA","MOTORISTA","COMBUSTÍVEL","ODÔMETRO (KM)"], tablefmt = "fancy_grid"))
  codmotor = input("Digite o código do motorista que irá fazer a viagem: ")
  tipov = worksheet1.cell(codmotor,2).value
  placa = worksheet1.cell(codmotor,3).value
  motor = worksheet1.cell(codmotor,4).value
  tipoc = worksheet1.cell(codmotor,5).value
  odometro = worksheet1.cell(codmotor,6).value
  data = input("Digite a data da viagem (D/M/A): ")
  saida = input("Digite o horário de saída do motorista: ")
  local = input("Digite a cidade de partida: ")
  dest = input("Digite o destino: ")
  dist = 0
  odometrov = 0
  data2 = 0
  cheg = 0
  valor = 0

  nLinha = [cod, tipov, placa, motor, tipoc, odometro, data, saida, local , dest, dist, odometrov, data2, cheg, valor]
  worksheet0.append_row(nLinha)
  worksheet3.update_cell(2,1,cod)

  print("Viagem registrada com sucesso!")
  time.sleep(3)
  output.clear()

def fimViagem():
  output.clear()
  dados = worksheet0.get_all_values()
  if len(dados) == 0:
    cod = int(worksheet3.cell(2,1).value)
  else:
    cod = int(worksheet3.cell(2,1).value) + 1
  viagens = worksheet0.get_all_values()
  print(tabulate(viagens, headers=["CÓDIGO","VEÍCULO","PLACA","MOTORISTA","TIPO DE COMBUSTÍVEL","ODÔMETRO INICIAL","DATA(SAÍDA)","HORÁRIO(SAÍDA)","PARTIDA","DESTINO","DISTÂNCIA (em KM)","ODÔMETRO FINAL","DATA(CHEGADA)","HORÁRIO(CHEGADA)","VALOR"], tablefmt = "fancy_grid"))
  codviagem = input("Digite o código da viagem que irá finalizar: ")
  output.clear()
  cadastros = worksheet1.get_all_values()
  print(tabulate(cadastros, headers=["CÓDIGO","VEÍCULO","PLACA","MOTORISTA","COMBUSTÍVEL","ODÔMETRO (KM)"], tablefmt = "fancy_grid"))
  codmotor = input("Digite o código do motorista que fez a viagem: ")
  tipov = worksheet0.cell(codviagem,2).value
  placa = worksheet0.cell(codviagem,3).value
  motor = worksheet0.cell(codviagem,4).value
  tipoc = worksheet0.cell(codviagem,5).value
  odometrov = worksheet0.cell(codviagem,6).value
  odometro = worksheet1.cell(codmotor,6).value
  data = worksheet0.cell(codviagem,7).value
  saida = worksheet0.cell(codviagem,8).value
  local = worksheet0.cell(codviagem,9).value
  dest = worksheet0.cell(codviagem,10).value
  data2 = input("Digite a data da chegada (D/M/A): ")
  cheg = input("Digite horário de chegada do motorista: ")
  dist = input("Digite a distância da viagem: ")
  odometro = int(odometro)+int(dist)
  odometrov = odometro
  viagem = worksheet0.find(codviagem)
  linha = viagem.row
  combustivel = worksheet0.cell(linha, 5).value
  valores = worksheet2.find(combustivel)
  linhac = valores.row
  valorc = worksheet2.cell(linhac, 2).value
  valorviagem = int(dist)*float(valorc)
  worksheet1.update_cell(codmotor,6,odometro)
  worksheet0.update_cell(codviagem,11,dist)
  worksheet0.update_cell(codviagem,12,odometrov)
  worksheet0.update_cell(codviagem,13,data2)
  worksheet0.update_cell(codviagem,14,cheg)
  worksheet0.update_cell(codviagem,15,valorviagem)

  attLinha = [cod, tipov, placa, motor, tipoc, odometro, data, saida, local , dest, dist, odometrov, data2, cheg, valorviagem]
  worksheet3.update_cell(2,1,cod)

  print("Viagem finalizada com sucesso!")
  time.sleep(3)
  output.clear()

def novoCadastro():
  output.clear()
  dados = worksheet1.get_all_values()
  if len(dados) == 0:
    cod = int(worksheet3.cell(2,2).value)
  else:
    cod = int(worksheet3.cell(2,2).value) + 1
  nome = input("Digite o nome do motorista: ")
  cnh = int(input("Digite a CNH (11 DÍGITOS): "))
  telefone = input("Digite o telefone ((XX)XXXXX-XXXX): ")
  veiculo = input("Digite tipo e modelo do veículo (TIPO-MODELO): ")
  placa = input("Digite a placa do veículo (ABC-1234): ")
  comb = input("Digite o tipo de combustível: ")
  odometro = int(input("Digite a quilometragem do veículo: "))
  status = "LIVRE"
  user = input("Digite o usuário do motorista: ")
  users = worksheet4.col_values(2)
  while user in users:
    print("Esse nome de usuário já está sendo usado!")
    time.sleep(3)
    output.clear()
    user = input("Digite outro nome de usuário: ")

  cadLinha = [cod, nome, cnh, telefone, veiculo, placa, comb, odometro, status, user]
  worksheet1.append_row(cadLinha)
  worksheet3.update_cell(2,2)

  print("Motorista cadastrado com sucesso!")
  time.sleep(3)
  output.clear()

def attCadastro():
  output.clear()
  cadastros = worksheet1.get_all_values()
  print(tabulate(cadastros, headers=["CÓDIGO","MOTORISTA","CNH","TELEFONE","VEÍCULO","PLACA","COMBUSTÍVEL","ODÔMETRO","STATUS","USUÁRIO"], tablefmt = "fancy_grid"))
  cod = input("Digite o código do cadastro a ser atualizado: ")
  try:
    cell = worksheet1.find(cod)
    if cell:
      coluna = cell.col
      linha = cell.row
      nome = input("Digite o nome do motorista: ")
      cnh = int(input("Digite a CNH (11 DÍGITOS): "))
      telefone = input("Digite o telefone ((XX)XXXXX-XXXX): ")
      veiculo = input("Digite tipo e modelo do veículo (TIPO-MODELO): ")
      placa = input("Digite a placa do veículo (ABC-1234): ")
      comb = input("Digite o tipo de combustível: ")
      odometro = int(input("Digite a quilometragem do veículo: "))
      user = input("Digite o usuário do motorista: ")
      users = worksheet4.col_values(2)
      while user in users:
        print("Esse nome de usuário já está sendo usado!")
        time.sleep(3)
        output.clear()
        user = input("Digite outro nome de usuário: ")
      worksheet1.update_cell(linha, coluna + 1, nome)
      worksheet1.update_cell(linha, coluna + 2, cnh)
      worksheet1.update_cell(linha, coluna + 3, telefone)
      worksheet1.update_cell(linha, coluna + 4, veiculo)
      worksheet1.update_cell(linha, coluna + 5, placa)
      worksheet1.update_cell(linha, coluna + 6, comb)
      worksheet1.update_cell(linha, coluna + 7, odometro)
      worksheet1.update_cell(linha, coluna + 9, user)
      print("Atualizado com sucesso!")
      time.sleep(3)
      output.clear()
  except gspread.exceptions.CellNotFound:
    print("Cadastro não encontrado no sistema!")
    time.sleep(3)
    output.clear()

def attLogin():
  output.clear()
  cadastros = worksheet4.get_all_values()
  print(tabulate(cadastros, headers=["CÓDIGO","USUARIO","SENHA","NOME","CNH","TELEFONE","NIVEL"], tablefmt = "fancy_grid"))
  cod = input("Digite o código do login a ser atualizado: ")
  try:
    cell = worksheet4.find(cod)
    if cell:
      coluna = cell.col
      linha = cell.row
      user = input("Digite o usuário do motorista: ")
      users = worksheet4.col_values(2)
      while user in users:
        print("Esse nome de usuário já está sendo usado!")
        time.sleep(3)
        output.clear()
        user = input("Digite outro nome de usuário: ")
      senha = input("Digite a senha: ")
      nome = input("Digite o nome completo do usuário: ")
      cnh = int(input("Digite a CNH (11 DÍGITOS): "))
      telefone = input("Digite o telefone ((XX)XXXXX-XXXX): ")
      print("Qual o nível do usuário?")
      print("1. Gerente")
      print("2. Motorista")
      print("3. Usuário")
      nivel = input("Escolha uma das opções acima:")
      if(nivel== "1"):
        nivel = "ADMIN"
      if(nivel== "2"):
        nivel = "MOTORISTA"
      if(nivel== "3"):
        nivel = "USUARIO"
      worksheet4.update_cell(linha, coluna + 1, user)
      worksheet4.update_cell(linha, coluna + 2, senha)
      worksheet4.update_cell(linha, coluna + 3, nome)
      worksheet4.update_cell(linha, coluna + 4, cnh)
      worksheet4.update_cell(linha, coluna + 5, telefone)
      worksheet4.update_cell(linha, coluna + 6, nivel)
      print("Atualizado com sucesso!")
      time.sleep(3)
      output.clear()
  except gspread.exceptions.CellNotFound:
    print("Cadastro não encontrado no sistema!")
    time.sleep(3)
    output.clear()
    
# Funções para excluir os registros da planilha
def delCadastro():
  output.clear()
  cadastros = worksheet1.get_all_values()
  print(tabulate(cadastros, headers=["CÓDIGO","VEÍCULO","PLACA","MOTORISTA","COMBUSTÍVEL","ODÔMETRO"], tablefmt = "fancy_grid"))
  cod = input("Digite o código do motorista que será excluido: ")
  try:
    cell = worksheet1.find(cod)
    if cell:
      worksheet1.delete_row(cell.row)
      print("Cadastro excluído com sucesso!")
      time.sleep(3)
      output.clear()
  except gspread.exceptions.CellNotFound:
    print("Cadastro não encontrado no sistema!")
    time.sleep(3)
    output.clear()


def delViagem():
  output.clear()
  viagens = worksheet0.get_all_values()
  print(tabulate(viagens, headers=["CÓDIGO","VEÍCULO","PLACA","MOTORISTA","TIPO DE COMBUSTÍVEL","ODÔMETRO INICIAL","DATA(SAÍDA)","HORÁRIO(SAÍDA)","PARTIDA","DESTINO","DISTÂNCIA (em KM)","ODÔMETRO FINAL","DATA(CHEGADA)","HORÁRIO(CHEGADA)","VALOR"], tablefmt = "fancy_grid"))
  cod = input("Digite o código da viagem que será excluido: ")
  try:
    cell = worksheet0.find(cod)
    if cell:
      worksheet0.delete_row(cell.row)
      print("Viagem excluída com sucesso!")
      time.sleep(3)
      output.clear()
  except gspread.exceptions.CellNotFound:
    print("Viagem não encontrada no sistema!")
    time.sleep(3)
    output.clear()
    
# Funções para listar os registros do motorista logado
def listaViagensM():
  output.clear()
  op = "1"
  while op == "1":
    user = worksheet3.cell(2,4).value
    placa = worksheet1.cell(worksheet1.find(user).row, 6).value
    viagens = worksheet0.get_all_values()
    viagensM = []
    for i in range(len(viagens)):
      if placa in viagens[i]:
        viagensM.append(viagens[i])
    print(tabulate(viagensM, headers=["CÓDIGO","VEÍCULO","PLACA","MOTORISTA","TIPO DE COMBUSTÍVEL","ODÔMETRO INICIAL","DATA(SAÍDA)","HORÁRIO(SAÍDA)","PARTIDA","DESTINO","DISTÂNCIA (em KM)","ODÔMETRO FINAL","DATA(CHEGADA)","HORÁRIO(CHEGADA)","VALOR"], tablefmt = "fancy_grid"))
    op = input("Digite 0 p/ voltar ao menu: ")
  output.clear()

def listaCadastrosM():
  output.clear()
  op = "1"
  while op == "1":
    user = worksheet3.cell(2,4).value
    cad = worksheet1.cell(worksheet1.find(user).row, 6).value
    cadastro = worksheet1.get_all_values()
    cadastroM = []
    for i in range(len(cadastro)):
      if cad in cadastro[i]:
        cadastroM.append(cadastro[i])
        print(tabulate(cadastroM, headers=["CÓDIGO","NOME","CNH","TELEFONE","VEICULO","PLACA","TIPO DE COMBUSTÍVEL","ODOMETRO","STATUS","USUARIO"], tablefmt = "fancy_grid"))
    op = input("Digite 0 p/ voltar ao menu: ")
  output.clear()


# Funções para listar os registros da planilha
def listaViagens():
  output.clear()
  op = "1"
  while op == "1":
    viagens = worksheet0.get_all_values()
    print(tabulate(viagens, headers=["CÓDIGO","VEÍCULO","PLACA","MOTORISTA","TIPO DE COMBUSTÍVEL","ODÔMETRO INICIAL","DATA(SAÍDA)","HORÁRIO(SAÍDA)","PARTIDA","DESTINO","DISTÂNCIA (em KM)","ODÔMETRO FINAL","DATA(CHEGADA)","HORÁRIO(CHEGADA)","VALOR"], tablefmt = "fancy_grid"))
    op = input("Digite 0 p/ voltar ao menu: ")
  output.clear()

def listaCadastros():
  output.clear()
  op = "1"
  while op == "1":
    cadastros = worksheet1.get_all_values()
    print(tabulate(cadastros, headers=["CÓDIGO","MOTORISTA","CNH","TELEFONE","VEÍCULO","PLACA","COMBUSTÍVEL","ODÔMETRO","STATUS","USUÁRIO"], tablefmt = "fancy_grid"))
    op = input("Digite 0 p/ voltar ao menu: ")
  output.clear()

def listaValores():
  output.clear()
  op = "1"
  while op == "1":
    valores = worksheet2.get_all_values()
    print(tabulate(valores, headers=["COMBUSTÍVEL","VALOR"], tablefmt = "fancy_grid"))
    op = input("Digite 0 p/ voltar ao menu: ")
  output.clear()
  
tela()