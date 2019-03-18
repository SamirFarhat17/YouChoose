from django.db import models

# Create your models here.
class Video(models.Model):
    link = models.CharField(max_length = 400, default = '')
    # link, comments, etc...

    def __str__(self):
        return self.link
        
