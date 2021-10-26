from django.db import models
from django.utils.text import slugify


def upload_path_handler(instance, filename):
    return "images/events/{title}/{file}".format(
        title=instance.event.title, file=filename
    )


class Event(models.Model):
    image = models.ImageField(upload_to="images/events")
    title = models.CharField(max_length=255)
    description = models.TextField()  # A brief summary about the event
    about = models.TextField(
        default=""
    )  # Question to be answered: WHAT IS THIS EVENT ABOUT?
    when = models.TextField(
        default=""
    )  # Question to be answered: WHEN IS IT HAPPENING?
    you = models.TextField(default="")  # Question to be answered: WHAT'S IN IT FOR YOU?
    reg_link = models.TextField(default="", blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.title

    def summary(self):
        return self.description[:125] + "..."

    def pub_date_pretty(self):
        return self.date.strftime("%b %e %Y")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)


class Photo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    desc = models.TextField()
    pic = models.ImageField(upload_to=upload_path_handler)

    def __str__(self):
        return self.event.title + "_" + self.desc
