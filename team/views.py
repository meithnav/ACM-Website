from django.shortcuts import render, redirect, get_object_or_404
from .models import Core_committee
from random import shuffle


def teams(request):
    comittee = Core_committee.objects.all().order_by("position")
    comittee = list(comittee)
    one = comittee.pop(0)
    two = comittee.pop(0)
    three = comittee.pop(0)
    four = comittee.pop(0)
    five = comittee.pop(0)
    shuffle(comittee)
    return render(
        request,
        "team/core.html",
        {
            "one": one,
            "two": two,
            "three": three,
            "four": four,
            "five": five,
            "committee": comittee,
        },
    )
