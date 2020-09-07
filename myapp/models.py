from django.db import models

# Create your models here.


class Character(models.Model):
    cid = models.IntegerField()
    name = models.CharField(max_length=100)
    mainPicSrc = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return f"{self.cid}, {self.name}"


class Movie(models.Model):
    mid = models.IntegerField()
    title = models.CharField(max_length=20)
    mainPicSrc = models.CharField(max_length=256)
    star = models.CharField(max_length=10)
    summary = models.TextField()
    characters = models.ManyToManyField(Character)

    def __str__(self):
        return f"{self.mid}, {self.title}"


class Comment(models.Model):
    comment_text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text
