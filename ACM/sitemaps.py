from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['home', 'submit', 'resources', 'contact', 'events','loc_home','ASCII','teams', 'blog']

    def location(self, item):
        return reverse(item)
