from django.db import models
from django.contrib.auth.models import User

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class House(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    chambre = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=1 ,null=True)
    contact=models.DecimalField(max_digits=20, decimal_places=1,null=True)
    website_url = models.URLField(max_length=200,null=True) 

    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'house' 
    def __str__(self):
        return self.title

class Bookmark(models.Model):
    favorites=models.ManyToManyField(User,related_name="favorite",default=None,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    houses = models.ManyToManyField(House, related_name='bookmarks')
