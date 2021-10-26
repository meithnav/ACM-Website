from django.db import models


class Core_committee(models.Model):
    name = models.CharField(max_length=255)
    post = models.CharField(max_length=255, null=False)
    pic = models.ImageField(upload_to="images/team")
    position = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Core_committee, self).save(*args, **kwargs)
