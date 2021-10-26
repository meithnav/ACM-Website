from django.db import models
from django.utils.text import slugify


class ProblemStatements(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    soln_type = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    company_logo = models.ImageField(upload_to="images/loc/statements")

    def __str__(self):
        return self.title

    def summary(self):
        return self.description[:100]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ProblemStatements, self).save(*args, **kwargs)


class Sponsors(models.Model):

    PARTNER_CHOICES = [
        ('Tech Partner', 'Tech Partner'),
        ('Power Sponsor', 'Power Sponsor'),
        ('Associate Sponsor', 'Associate Sponsor'),
        ('Gifting Partner', 'Gifting Partner'),
        ('Education Abroad Partner','Education Abroad Partner'),
    ]

    logo = models.ImageField(upload_to="images/loc/sponsors")
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=2000, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    partner_type = models.CharField(max_length=200,choices=PARTNER_CHOICES,default='Tech Partner')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Sponsors, self).save(*args, **kwargs)




class Transaction(models.Model):
    uid = models.CharField(unique=True,max_length=20)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
