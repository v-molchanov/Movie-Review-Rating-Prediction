from django.db import models

class Review(models.Model):
    text = models.TextField('Text')
    rating = models.IntegerField('Rating', max_length=10)
    publish_date = models.DateTimeField('Publish date')

    def __str__(self):
        return self.text
    
