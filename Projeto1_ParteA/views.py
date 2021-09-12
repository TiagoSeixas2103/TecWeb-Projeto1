from os import error, replace
from utils import load_data, load_template, build_response, delete_note, update_note,add_notes
import urllib
import json

def index(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus

        #titulo=Sorvete+de+banana 
        #detalhes=Coloque+uma+banana+no+congelador+e+espere.+Pronto%21+1%2B1%3D
        for chave_valor in corpo.split('&'):
            if chave_valor.startswith("titulo"):
                params["titulo"] = urllib.parse.unquote_plus(chave_valor[chave_valor.find("=")+1:], encoding="utf-8", errors="replace")
            if chave_valor.startswith("detalhes"):
                params["detalhes"] = urllib.parse.unquote_plus(chave_valor[chave_valor.find("=")+1:], encoding="utf-8", errors="replace")
        
        add_notes(params)

        return build_response(code=303, reason="See Other", headers="Location: /")

    


    note_template = load_template('components/note.html')
    notes_li = [
        #note_template.format(titulo=dados["titulo"], detalhes=dados["detalhes"])
        note_template.format(id = dados.id, titulo=dados.titulo, detalhes=dados.detalhes)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return build_response()+load_template('index.html').format(notes=notes).encode()

def delete(request):

    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus

        #titulo=Sorvete+de+banana 
        #detalhes=Coloque+uma+banana+no+congelador+e+espere.+Pronto%21+1%2B1%3D
        id = urllib.parse.unquote_plus(corpo[corpo.find("=")+1:], encoding="utf-8", errors="replace")
        print("esse é o id:")
        
        delete_note(int(id))

        return build_response(code=303, reason="See Other", headers="Location: /")


    note_template = load_template('components/note.html')
    notes_li = [
        #note_template.format(titulo=dados["titulo"], detalhes=dados["detalhes"])
        note_template.format(id = dados.id, titulo=dados.titulo, detalhes=dados.detalhes)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return build_response()+load_template('index.html').format(notes=notes).encode()


def update(request):

    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params ={}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus

        #titulo=Sorvete+de+banana 
        #detalhes=Coloque+uma+banana+no+congelador+e+espere.+Pronto%21+1%2B1%3D
        id = urllib.parse.unquote_plus(corpo[corpo.find("=")+1:], encoding="utf-8", errors="replace")
        for chave_valor in corpo.split('&'):
            if chave_valor.startswith("titulo"):
                params["titulo"] = urllib.parse.unquote_plus(chave_valor[chave_valor.find("=")+1:], encoding="utf-8", errors="replace")
            if chave_valor.startswith("detalhes"):
                params["detalhes"] = urllib.parse.unquote_plus(chave_valor[chave_valor.find("=")+1:], encoding="utf-8", errors="replace")
        
        int_id = int(id.split("&")[0])
        
        update_note(int_id, params)

        return build_response(code=303, reason="See Other", headers="Location: /")


    note_template = load_template('components/note.html')
    notes_li = [
        #note_template.format(titulo=dados["titulo"], detalhes=dados["detalhes"])
        note_template.format(id = dados.id, titulo=dados.titulo, detalhes=dados.detalhes)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return build_response()+load_template('index.html').format(notes=notes).encode()