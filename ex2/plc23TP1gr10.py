import re
import json

# Função que vai guardar a informação do ficheiro CSV num Diciconário               
def filtrar_csv(fd):

    # Vai dividir o descritor de ficheiro por linhas
    lista_linhas = re.split('\n', fd)
    dados = []
    nomes_invertidos = []
    # Iterar as linhas
    for linha in lista_linhas:
        # Criar um dicionário vazio para cada linha
        dict_linhas = {
            "id": "",
            "index": "",
            "data": "",
            "nome": "",
            "idade": "",
            "genero": "",
            "morada": "",
            "modalidade": "",
            "clube": "",
            "email": "",
            "federado": "",
            "aprovado": ""
        }

        # Se a linha não é vazia
        if linha:
            # Iterar as colunas e guardar a informação de cada uma no Dicionário
            coluna = re.split(',', linha)
            if (re.search(r'[0-9a-z]{24}', coluna[0])):
                dict_linhas["id"] = coluna[0]
            if (re.search(r'[0-9]{1,2}', coluna[1])):
                dict_linhas["index"] = coluna[1]
            if (re.search(r'20[1-2][0-9]-[0-1][0-9]-[0-3][0-9]', coluna[2])):
                dict_linhas["data"] = coluna[2]

            # Identificar o género:
            if (re.search(r'M|F', coluna[6])):
                dict_linhas["genero"] = coluna[6]

            # Normalizar os nomes:    
            if (re.search(r'[A-Z][a-z]+', coluna[3])):
                # Se o género for Feminino, escreve o nome pela ordem do documento
                if dict_linhas["genero"] == 'F' and re.search(r'[A-Z][a-z]+', coluna[4]):
                    dict_linhas["nome"] = coluna[3] + " " + coluna[4]

                else:
                # Caso seja Masculino, inverte a ordem e guarda os nomes trocados num array
                    if (re.search(r'[A-Z][a-z]+', coluna[4])):
                        dict_linhas["nome"] = coluna[4] + " " + coluna[3]
                        nomes_invertidos.append({
                            "Nome Original": coluna[3] + " " + coluna[4],
                            "Nome Invertido": coluna[4] + " " + coluna[3]
                        })

            if (re.search(r'[1-3][0-9]', coluna[5])):
                dict_linhas["idade"] = coluna[5]
            
            if (re.search(r'[A-Z][a-z]+', coluna[7])):
                dict_linhas["morada"] = coluna[7]
            if (re.search(r'[A-Za-zÀ-ÿ]+', coluna[8])):
                dict_linhas["modalidade"] = coluna[8]
            if (re.search(r'[A-Za-z]+', coluna[9])):
                dict_linhas["clube"] = coluna[9]
            if (re.search(r'[a-z.]+[a-z]+@[a-z.]+', coluna[10])):
                dict_linhas["email"] = coluna[10]
            if (re.search(r'true|false', coluna[11])):
                dict_linhas["federado"] = coluna[11]
            if (re.search(r'true|false', coluna[12])):
                dict_linhas["aprovado"] = coluna[12]

        # Se o id não estiver vazio, dá append para o array
        if (dict_linhas["id"] != ""):
            dados.append(dict_linhas)

    return dados, nomes_invertidos


# Devolve uma string com a idade mais alta e mais baixa
def extremos_idade(dados):

    maior_idade = 0
    menor_idade = 100

    for dado in dados:

        idade = dado["idade"]

        # Verifica que a idade não é uma string vazia
        if idade:
            idade = int(idade) #converte idade de string para int

            if idade > maior_idade:
                maior_idade = idade
            
            if idade < menor_idade:
                menor_idade = idade

    return[menor_idade, maior_idade]


# Devolve um dicionário com a distribuição por Género no total
def genero_total(dados):

    # Dicionário onde vai ser guardada a distribuição por Género
    dict_genero = {"M":0,"F":0}

    # Iterar todos os dados 
    for dado in dados:
        genero = dado["genero"]
        # Se o género é Masculino, incrementa o valor da chave M
        if genero == "M":
            dict_genero["M"] += 1
        # Se o género é Feminino, incrementa o valor da chave F
        elif genero == "F":
            dict_genero["F"] += 1

    return dict_genero


# Devolve um dicionário com as modalidades praticadas em cada ano
def modalidade_ano(dados):

    dict_anual = {}

    # Iterar os dados
    for dado in dados:
        
        # Guardar o ano da data numa variável
        padrao = re.search(r'[0-9]{4}', dado["data"])

        # Se ano não é vazio
        if padrao:
            ano = padrao.group() 
        # Caso o ano não seja uma chave do dicionário, adiciona como chave
            if ano not in dict_anual:
                dict_anual[ano] = {}
        
        modalidade = dado["modalidade"]
        # Caso a modalidade não esteja como um valor no respetivo ano, adiciona como chave
        if modalidade not in dict_anual[ano]:
            dict_anual[ano][modalidade] = 1
        else:
            # Caso o ano e a modalidade já existam no dicionário, incrementa
            dict_anual[ano][modalidade] += 1

    # Ordenar as modalidades por ordem alfabética dentro de cada ano
    for ano, modalidades in dict_anual.items():
        dict_anual[ano] = dict(sorted(modalidades.items()))
    
    # Ordenar os anos por ordem crescente
    dict_anual = dict(sorted(dict_anual.items()))

    return dict_anual


# Devolve um dicionário com o total de modalidades praticadas
def modalidade_total(dados):

    dict_total = {}
    # Iterar os dados
    for dado in dados:

        modalidade = dado["modalidade"]
        # Verificar a string é vazia
        if modalidade:
            # Se a modalidade não for uma chave do dicionário, adiciona como chave
            if modalidade not in dict_total.keys():
                dict_total[modalidade] = 1
            else:
            # Caso a modalidade já exista como chave, incremeta o valor
                dict_total[dado["modalidade"]] += 1

    #Ordenar as modalidades por ordem alfabética
    dict_total = dict(sorted(dict_total.items()))

    return dict_total


def percentagem_aptos(dados):

    dict_aptos = {"true": 0, "false": 0}

    # Iterar os dados
    for dado in dados:

        aprovado = dado["aprovado"]

        if aprovado == "true":
            dict_aptos["true"] += 1

        elif aprovado == "false":
            dict_aptos["false"] += 1
    
    # Somar o número de aprovados e não aprovados
    total_aprovados = dict_aptos["true"] + dict_aptos["false"]

    # Verificar se não vamos dividir por 0
    if total_aprovados > 0:
        percentagem_true = (dict_aptos["true"] / total_aprovados) * 100
        percentagem_false = (dict_aptos["false"] / total_aprovados) * 100
    else:
        percentagem_true = 0.0
        percentagem_false = 0.0

    return[percentagem_true, percentagem_false]


# Abrir o ficheiro emd.csv e executar a função filtrar_csv
ficheiro_filtrado = []
with open("emd.csv") as file:
    fd = file.read()
    ficheiro_filtrado, nomes_invertidos = filtrar_csv(fd)


# Guardar os nomes trocados num ficheiro em formato JSON
with open("nomes_invertidos.json", "w") as json_file:
    json.dump(nomes_invertidos, json_file, indent=4)


# ---------------------------------------------------------------------
# GERAR AS PÁGINAS HTML ONDE SERÃO IMPRIMIDOS OS RESULTADOS DAS FUNÇÕES
# ---------------------------------------------------------------------

idades = extremos_idade(ficheiro_filtrado) 

def gerar_html_extremos_idade(idades):  

    html = "<html>\n<head></head>\n<body>\n"
    
    # Adicionar um título
    html += "<h2>Extremos de Idade</h2>\n"

    # Adicionar parágrafos com as idades
    html += f"<p>Menor Idade: {idades[0]} anos</p>\n"
    html += f"<p>Maior Idade: {idades[1]} anos</p>\n"
    
    html += "</body>\n</html>"

    return html

html_extremos_idade = gerar_html_extremos_idade(idades)

# Escrever a string HTML no ficheiro idades.html
with open("idades.html", "w") as file:
    file.write(html_extremos_idade)



generos = genero_total(ficheiro_filtrado)

def gerar_html_genero_total(dict_generos):

    html = "<html>\n<head></head>\n<body>\n"
    
    # Adicionar um título
    html += "<h2>Distribuição por Género</h2>\n"

    # Adicionar parágrafos com a distribuição por gênero
    html += f"<p>Género Masculino: {dict_generos['M']} pessoas</p>\n"
    html += f"<p>Género Feminino: {dict_generos['F']} pessoas</p>\n"
    
    html += "</body>\n</html>"

    return html

html_genero_total = gerar_html_genero_total(generos)

# Escrever a string HTML no ficheiro generos.html
with open("generos.html", "w") as file:
    file.write(html_genero_total)



dados_modalidades_anual = modalidade_ano(ficheiro_filtrado)

def gerar_html_modalidade_ano(dados_modalidade):

    html = "<html>\n<head></head>\n<body>\n"

    # Adicionar um título
    html += "<h2>Modalidades por Ano</h2>\n"

    # Adiciona títulos para cada ano e parágrafos para as modalidades e o número de praticantes
    for ano, modalidades in dados_modalidade.items():
        html += f"<h4>{ano}</h4>\n"
        for modalidade, total in modalidades.items():
            html += f"<p>{modalidade}: {total}</p>\n"

    html += "</body>\n</html>"

    return html

html_modalidade_ano = gerar_html_modalidade_ano(dados_modalidades_anual)

# Escrever a string HTML no ficheiro modalidades_anual.html
with open("modalidades_anual.html", "w") as file:
    file.write(html_modalidade_ano)



dados_modalidades_total = modalidade_total(ficheiro_filtrado)

def gerar_html_modalidades_total(dados_modalidades):
    html = "<html>\n<head></head>\n<body>\n"

    # Adicionar um título
    html += "<h2>Modalidades no Total</h2>\n"
    
    for modalidade, total in dados_modalidades.items():
        # Criar parágrafos diretamente
        html += f'<p>{modalidade}: {total}</p>\n'
    
    html += "</body>\n</html>"

    return html

html_modalidades_total = gerar_html_modalidades_total(dados_modalidades_total)

# Escrever a string HTML no ficheiro modalidades_total.html
with open("modalidades_total.html", "w") as file:
    file.write(html_modalidades_total)



aptos = percentagem_aptos(ficheiro_filtrado)

def gerar_html_percentagem_aptos(dados_aptos):

    html = "<html>\n<head></head>\n<body>\n"
    
    # Adicione um título
    html += "<h1>Percentagem de Aptos</h1>\n"

    # Adicione parágrafos com as percentagens
    html += f"<p>Aptos: {dados_aptos[0]:.2f}%</p>\n"
    html += f"<p>Não Aptos: {dados_aptos[1]:.2f}%</p>\n"
    
    html += "</body>\n</html>"

    return html


html_percentagem_aptos = gerar_html_percentagem_aptos(aptos)

# Escrever a string HTML no arquivo aptos.html
with open("aptos.html", "w") as file:
    file.write(html_percentagem_aptos)


conteudo_index = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
    <h1>Processador de Registos de Exames Médicos Desportivos</h1>
    
    <!-- Link para a página idades.html -->
    <a href="idades.html"></a><br>

    <!-- Link para a página generos.html -->
    <a href="generos.html">Ir para Géneros</a><br>

    <!-- Link para a página modalidades_anual.html -->
    <a href="modalidades_anual.html">Ir para Modalidades por Ano</a><br>

    <!-- Link para a página modalidades_total.html -->
    <a href="modalidades_total.html">Ir para Modalidades no Total</a><br>

    <!-- Link para a página aptos.html -->
    <a href="aptos.html">Ir para Aptos</a><br>

    <!-- Iframe para a página idades.html -->
    <iframe src="idades.html" width="600" height="400"></iframe>

    <!-- Iframe para a página generos.html -->
    <iframe src="generos.html" width="600" height="400"></iframe>

    <!-- Iframe para a página modalidades_anual.html -->
    <iframe src="modalidades_anual.html" width="600" height="400"></iframe>

    <!-- Iframe para a página modalidades_total.html -->
    <iframe src="modalidades_total.html" width="600" height="400"></iframe>

    <!-- Iframe para a página aptos.html -->
    <iframe src="aptos.html" width="600" height="400"></iframe>
</body>
</html>
"""

with open("index.html", "w") as file:
    file.write(conteudo_index)
