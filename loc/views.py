from django.shortcuts import render
from .models import Sponsors


def loc(request):
    sponsors = Sponsors.objects.all()
    return render(request, "loc/loc.html",{'sponsors':sponsors})

