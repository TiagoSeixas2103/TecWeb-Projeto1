import sqlite3

from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    titulo: str = None
    detalhes: str = ''

class Database: 
    def __init__(self,nome):
        nome = nome+".db"
        self.conn = sqlite3.connect(nome)
        self.cursor = self.conn.cursor()
        self.note = self.cursor.execute("CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, titulo STRING, detalhes STRING NOT NULL);")

    def add(self, note):
        self.cursor.execute("INSERT INTO note (titulo,detalhes) VALUES (?, ?);", (note.titulo,note.detalhes))
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT id, titulo, detalhes FROM note;")
        notes = []
        for conteudo in cursor:
            id = conteudo[0]
            titulo = conteudo[1]
            detalhes = conteudo[2]
            notes.append(Note(id=id, titulo=titulo, detalhes=detalhes))
        return notes
        
    def update(self, entry):
        self.cursor.execute("UPDATE note SET titulo = ? WHERE id = ?;", (entry.titulo,entry.id))
        self.cursor.execute("UPDATE note SET detalhes = ? WHERE id = ?;", (entry.detalhes,entry.id))
        self.conn.commit()

    def delete(self, note_id):
        self.cursor.execute("DELETE FROM note WHERE id = ?;", (note_id,))
        self.conn.commit()

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

def load_data():
    banco_de_dados = Database("notes")
    notes = banco_de_dados.get_all()
    return notes

def add_notes(note):
    banco_de_dados =  Database("notes")
    banco_de_dados.add(Note(titulo=note["titulo"], detalhes=note["detalhes"]))

def delete_note(id):
    banco_de_dados = Database("notes")
    banco_de_dados.delete(id)

def update_note(id, note):
    banco_de_dados = Database("notes")
    banco_de_dados.update(Note(id=id, titulo=note["titulo"], detalhes=note["detalhes"]))

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