from django.shortcuts import render, redirect
from .models import Note

def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        new_note = Note()
        new_note.title = title
        new_note.content = content
        new_note.save()
        # TAREFA: Utilize o title e content para criar um novo Note no banco de dados
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})

def delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        Note.objects.filter(id=id).delete()
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})

def update(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        new_note = Note()
        new_note.title = title
        new_note.content = content
        new_note.id = id
        new_note.save()
        #note = Note()
        #note.objects = Note.objects.filter(id=id)
        #note.title = title
        #note.content = content
        #note.save()
        #Note.objects.filter(id=id).delete()
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})