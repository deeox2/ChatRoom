from django.db import models

class Messages(models.Model):
    username = models.TextField()
    message = models.TextField()

    def __unicode__(self):
        return self.message
