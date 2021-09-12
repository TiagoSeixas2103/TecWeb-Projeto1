from os import error, replace
from utils import load_data, load_template, build_response, delete_note, update_note,add_notes
import urllib

def index(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}

        for chave_valor in corpo.split('&'):
            if chave_valor.startswith("titulo"):
                params["titulo"] = urllib.parse.unquote_plus(chave_valor[chave_valor.find("=")+1:], encoding="utf-8", errors="replace")
            if chave_valor.startswith("detalhes"):
                params["detalhes"] = urllib.parse.unquote_plus(chave_valor[chave_valor.find("=")+1:], encoding="utf-8", errors="replace")
        
        add_notes(params)

        return build_response(code=303, reason="See Other", headers="Location: /")

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(id = dados.id, titulo=dados.titulo, detalhes=dados.detalhes)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return build_response()+load_template('index.html').format(notes=notes).encode()

def delete(request):

    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]

        id = urllib.parse.unquote_plus(corpo[corpo.find("=")+1:], encoding="utf-8", errors="replace")
        print("esse é o id:")
        
        delete_note(int(id))

        return build_response(code=303, reason="See Other", headers="Location: /")

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(id = dados.id, titulo=dados.titulo, detalhes=dados.detalhes)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return build_response()+load_template('index.html').format(notes=notes).encode()

def update(request):

    if request.startswith('POST'):
        request = request.replace('\r', '') 

        partes = request.split('\n\n')
        corpo = partes[1]
        params ={}

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
        note_template.format(id = dados.id, titulo=dados.titulo, detalhes=dados.detalhes)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return build_response()+load_template('index.html').format(notes=notes).encode()