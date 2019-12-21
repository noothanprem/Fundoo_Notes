from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from colorful.fields import RGBColorField

# Create your models here.
class Img(models.Model):
    imgs= models.URLField(max_length=250)

class Label(models.Model):
    name = models.CharField(max_length=100,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='labeluser')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'label'
        verbose_name_plural = 'labels'


class Note(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='noteuser')
    title=models.CharField(max_length=50)
    note=models.TextField()
    label=models.ManyToManyField(Label,blank=True,related_name='label')
    collaborator=models.ManyToManyField(User,blank=True,related_name='collaborator')
    image=models.ImageField(blank=True)
    is_archieve=models.BooleanField(default=False)
    is_trash=models.BooleanField(default=False)
    color = RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'],blank=True,null=True)
    reminder = models.DateTimeField(blank=True,null=True)
    is_pin=models.BooleanField(default=False)
    url=models.URLField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'note'
        verbose_name_plural = 'notes'


class Tasks(models.Model):
    task_id = models.CharField(max_length=50)
    job_name = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.task_id} {self.job_name}'

# class Sample(models.Model):
#     title = models.CharField(max_length=500)
#     author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
#     #body = models.TextField(default="hello")
#     #created_at = models.DateTimeField(auto_now_add=True, editable=False)
#     #modified_at = models.DateTimeField(auto_now=True, editable=False)
#
#     def __str__(self):
#         return self.title

