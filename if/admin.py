from django.contrib import admin
from .models import Companies,Form,FormCompany,FormStudent,Transaction

admin.site.register(Companies)
class FormCompanyAdmin(admin.ModelAdmin):
    search_fields = ["name"]
admin.site.register(FormCompany,FormCompanyAdmin)
class FormStudentAdmin(admin.ModelAdmin):
    search_fields = ["full_name","sap_id"]
admin.site.register(FormStudent,FormStudentAdmin)
class FormAdmin(admin.ModelAdmin):
    search_fields = ["student__full_name","company__name"]
admin.site.register(Form,FormAdmin)
admin.site.register(Transaction)