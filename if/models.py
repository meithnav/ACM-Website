from django.db import models
from django.utils.text import slugify

class Companies(models.Model):
    Company_name = models.CharField(max_length=255)
    about_company = models.TextField()
    job_description = models.TextField()
    role = models.TextField()
    job_requirement = models.TextField(blank=True)
    mandatory_skills = models.TextField()
    stipend = models.CharField(max_length=100)
    Company_url = models.URLField()
    Company_age = models.IntegerField()
    loctaion = models.TextField()
    perks = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="images/intern_fair")
    mode_of_internship = models.CharField(max_length=100)

    def __str__(self):
        return self.Company_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.Company_name)
        super(Companies, self).save(*args, **kwargs)

class FormCompany(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    positionType = models.CharField(max_length=200)

    def string(self):
        return str(self.name)+"|"+str(self.positionType)+"|"+str(self.position)
    
    def string2(self):
        return str(self.name)+"|"+str(self.positionType)

    def __str__(self):
        return str(self.name)+"|"+str(self.positionType)+"|"+str(self.position)

class FormStudent(models.Model):
    full_name = models.CharField(max_length=200)
    sap_id = models.CharField(unique=True,max_length=11)
    gender = models.CharField(max_length=6)
    email_id = models.EmailField(max_length=150)
    phone_no = models.CharField(max_length=10)
    whatsapp_no = models.CharField(max_length=10)
    resume_drive_link = models.URLField(max_length=500)
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    is_member = models.BooleanField(default=False)
    amount = models.CharField(max_length=5)
    payment_verified = models.BooleanField(default=False)
    no_of_companies = models.IntegerField(default=0)
    payment_receipt = models.FileField(upload_to="images/if_receipt",blank=True,null=True)
    refund_amount = models.CharField(max_length=5,default=0)
    refund_saved = models.BooleanField(default=False)


    def __str__(self):
        return str(self.sap_id)+" "+str(self.full_name)

class Form(models.Model):
    student = models.ForeignKey(FormStudent,on_delete=models.CASCADE)
    company = models.ForeignKey(FormCompany,on_delete=models.CASCADE)
    attended = models.BooleanField(default=True)

    def __str__(self):
        return str(self.student)+"-"+str(self.company)

class Transaction(models.Model):
    student = models.ForeignKey(FormStudent,on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)
    successful = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id + 400)
        return super().save(*args, **kwargs)

