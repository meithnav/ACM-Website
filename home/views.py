from django.shortcuts import render
from events import models as eventmodel
from datetime import datetime

# Create your views here.
def home(request):
    if request.method == "GET":
        events = eventmodel.Event.objects.filter(
            date__gte=datetime.now().date()
        ).order_by("date")[:2]
        events_2020 = eventmodel.Event.objects.filter(date__year=2020)
        d = {
            "event1": events_2020[0],
            "event2": events_2020[1],
            "event3": events_2020[2],
            "event4": events_2020[3],
            "events": events,
        }
        return render(request, "home/home.html", d)


def submit(request):
    return render(request, "home/submit.html")


def resources(request):
    return render(request, "home/Resources.html")
