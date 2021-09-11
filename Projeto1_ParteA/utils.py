import json

import sqlite3

from dataclasses import dataclass

@dataclass
class Cards:
    titulo: str = None
    detalhes: str = ''

class Database: 
    def __init__(self,nome):
        nome = nome+".db"
        self.conn = sqlite3.connect(nome)
        self.cursor = self.conn.cursor()
        self.card = self.cursor.execute("CREATE TABLE IF NOT EXISTS cards (titulo STRING, detalhes STRING NOT NULL);")

    def add(self, card):
        self.cursor.execute("INSERT INTO cards (titulo,detalhes) VALUES (?, ?);", (card.titulo,card.detalhes))
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT titulo, detalhes FROM cards;")
        cards = []
        for conteudo in cursor:
            titulo = conteudo[0]
            detalhes = conteudo[1]
            cards.append(Cards(titulo=titulo, detalhes=detalhes))
        return cards
        
    def update(self, entry):
        self.cursor.execute("UPDATE cards SET titulo = ? WHERE detalhes = ?;", (entry.titulo,entry.detalhes))
        self.cursor.execute("UPDATE cards SET detalhes = ? WHERE titulo = ?;", (entry.detalhes,entry.titulo))
        self.conn.commit()

    def delete(self, card_titulo):
        self.cursor.execute("DELETE FROM cards WHERE titulo = ?;", (card_titulo,))
        self.conn.commit()



def extract_route(requisicao):
    if requisicao.startswith('GET'):
        lista1 = requisicao.split("GET /")
    elif requisicao.startswith('POST'):
        lista1 = requisicao.split("POST /")
    elif requisicao.startswith('PUT'):
        lista1 = requisicao.split("PUT /")
    else:
        lista1 = requisicao.split("DELETE /")

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

def load_data(nomeDb):
    con = sqlite3.connect(nomeDb)
    cur = con.cursor()
    cursor = cur.execute("SELECT titulo, detalhes FROM cards;")
    car = []
    for conteudo in cursor:
        titulo = conteudo[0]
        detalhes = conteudo[1]
        car.append(Cards(titulo=titulo, detalhes=detalhes))

    return car
        




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