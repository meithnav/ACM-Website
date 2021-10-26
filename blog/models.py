from django.db import models

# Create your models here.


def upload_path_handler(instance, filename):
    return "images/blogs/{title}/{file}".format(
        title=instance.blog.title, file=filename
    )


class Author(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='images/authors')
    detail = models.TextField(default='')
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    type = models.CharField(default='',max_length=50)
    keywords = models.TextField(default='')
    summary = models.TextField(default='',max_length=225)
    click_counter = models.IntegerField(default=0)
    main_img = models.ImageField(upload_to="images/blogs")
    date = models.DateField()
    content = models.TextField(default='')

    def short_summary(self):
        return self.summary[:50]+"..."

    def __str__(self):
        return str(self.author) + "_" + self.title
