from django.shortcuts import render


def ASCII(request):
    return render(request, "ascii/ASCII.html")
