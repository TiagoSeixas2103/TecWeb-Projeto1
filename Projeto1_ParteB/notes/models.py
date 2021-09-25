from django.db import models


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return "{ID}. {TITULO}".format(ID = self.id,TITULO = self.title)
