import json

def extract_route(requisicao):
    if requisicao.startswith('GET'):
        lista1 = requisicao.split("GET /")
    else:
        lista1 = requisicao.split("POST /")

    lista2 = lista1[1].split(" ")
    return lista2[0]

def read_file(path):
    lista = str(path).split(".")
    if lista[-1]=="txt" or lista[-1]=="html" or lista[-1]=="css" or lista[-1]=="js":
        with open(path, "rt") as file:
            text = file.read()
            return text.encode()
    else:
        with open(path, "rb") as file:
            binary = file.read()
        return binary

def load_data(nomeJson):
    filePath = "data/"+nomeJson
    with open(filePath, "rt", encoding="utf-8") as text:
        content = text.read()
        contentPython = json.loads(content)
        return contentPython

def load_template(file_path):
    file = open("templates/"+file_path,encoding="utf-8")
    content = file.read()
    file.close()
    return content

def build_response(body='', code=200, reason='OK', headers=''):
    response = "HTTP/1.1 "+str(code)+" "+reason
    if headers == '':
        response += "\n\n"+body
    else:
        response += "\n"+headers+"\n\n"
    
    return str(response).encode()