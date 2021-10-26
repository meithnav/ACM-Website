from django.shortcuts import render
from .models import Event, Photo


def events(request):
    events = Event.objects.all().order_by("-date")
    return render(request, "events/events.html", {"events": events})


def event_detail(request, event_name):
    event = Event.objects.get(title=event_name)
    photos = Photo.objects.filter(event=event)
    fivephotos = photos[:5]
    if len(fivephotos) >= 5:
        one = fivephotos[0]
        two = fivephotos[1]
        three = fivephotos[2]
        four = fivephotos[3]
        five = fivephotos[4]
        return render(
            request,
            "events/event_detail.html",
            {
                "one": one,
                "two": two,
                "three": three,
                "four": four,
                "five": five,
                "photos": photos,
                "event": event,
            },
        )
    else:

        return render(
            request, "events/event_detail.html", {"photos": photos, "event": event}
        )
