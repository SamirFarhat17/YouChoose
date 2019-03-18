from django.db import models

# Create your models here.



class Channel(models.Model):
    link = models.CharField(max_length = 400, null=True, blank=True)
    # link, comments, etc...

    def __str__(self):
        return self.link
