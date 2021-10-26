from django.shortcuts import render
from .models import Contact


def contact(request):
    error = ""
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        try:
            new_contact = Contact.objects.create(
                fname=firstname,
                lname=lastname,
                email=email,
                subject=subject,
                message=message,
            )
            new_contact.save()
            error = "no"
        except:
            error = "yes"
    return render(request, "contact/contactus.html", {"error": error})
