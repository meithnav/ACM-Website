from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Companies,Transaction,FormCompany,FormStudent,Form
from .paytm import generate_checksum, verify_checksum
from django.http import HttpResponse
import xlwt
import datetime
# Create your views here.

MEMBER_LIST = ['60004190060', '60004190007', '60003190048', '60004190065', '60004190106', '60004190017', '60004190118', '60004190099', '60004190090', '60004190004', '60004190009', '60004190005', '60004190034', '60004190014', '60003190005', '60004190073', '60004190120', '60004190101', '60004190067', '60004190129', '60004190126', '60004190105', '60004190102', '60004190057', '60004190072', '60004190033', '60004190043', '60003190032', '60003190053', '60004190080', '60001190055', '60004190124', '60004190029', '60004190082', '60004190047', '60004190054', '60002190085', '60004190075', '60004190125', '60004190062', '60004190006', '60003190056', '60004190025', '60004190117', '60004190039', '60004200053', '60003190057', '60004190058', '60002190035', '60002190011', '60003190059', '60004190059', '60004190022', '60004190016', '6004190070', '60004190028', '60004190114', '60004190092', '60004190095', '60004190113', '60004190038', '60004190098', '60004200040', '60004190068', '60004200064', '60001190001', '60004190069', '60004190013', '60004190100', '60004190107', '60004190094', '60004190078', '60004190051', '60004190003', '60004190061', '60004190027', '60004190011', '60004190008', '60004190121', '60004190112', '60004190088', '60004190042', '60004190055', '60004190048', '60004190020', '60004190115', '60004190066', '60004190087', '60003190049', '60004190116', '60004190010', '60004190032', '60004190056', '60004190035', '60004190122', '60004190096', '60001190054', '60004190128', '60004190091', '60004190097', '60004190001', '60004200043']
COST = 50

# def initiate_payment(request):
#     if request.method == "GET":
#         return render(request, 'if/payments/pay.html')
#     #try:
#         #username = request.POST['username']
#         #password = request.POST['password']
#     uid = request.POST['uid']
#     amount = int(request.POST['amount'])
#         #user = authenticate(request, username=username, password=password)
#         #if user is None:
#         #    raise ValueError
#         #auth_login(request=request, user=user)
#     #except:
#     #return render(request, 'if/payments/pay.html', context={'error': 'Wrong Accound Details or amount'})

#     transaction = Transaction.objects.create(sap_id=uid, amount=amount)
#     transaction.save()
#     merchant_key = settings.PAYTM_SECRET_KEY

#     params = (
#         ('MID', settings.PAYTM_MERCHANT_ID),
#         ('ORDER_ID', str(transaction.order_id)),
#         ('CUST_ID', str(transaction.sap_id)),
#         ('TXN_AMOUNT', str(transaction.amount)),
#         ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
#         ('WEBSITE', settings.PAYTM_WEBSITE),
#         # ('EMAIL', request.user.email),
#         # ('MOBILE_N0', '9911223388'),
#         ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
#         ('CALLBACK_URL', 'http://127.0.0.1:8000/if/callback/'),
#         # ('PAYMENT_MODE_ONLY', 'NO'),
#     )

#     paytm_params = dict(params)
#     checksum = generate_checksum(paytm_params, merchant_key)
    
#     transaction.checksum = checksum
#     transaction.save()

#     paytm_params['CHECKSUMHASH'] = checksum
#     print('SENT: ', checksum)
#     return render(request, 'if/payments/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        print(request.body)
        print(request.POST)
        received_data = dict(request.POST)
        print(received_data)

        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
            transaction = Transaction.objects.get(order_id=request.POST.get("ORDERID"))
            student = FormStudent.objects.get(sap_id=transaction.student.sap_id)
            response = {}
            response['SAP_ID']=student.sap_id
            response['FULL_NAME']=student.full_name
            if student.is_member:
                response['MEMBER_OF_ACM']="YES"
            else:
                response['MEMBER_OF_ACM']="NO"
            response['NO_OF_COMPANIES']=student.no_of_companies
            response['MID']=request.POST.get("MID")
            response['TXNID']=request.POST.get("TXNID")
            response['ORDERID']=request.POST.get("ORDERID")
            response['BANKTXNID']=request.POST.get("BANKTXNID")
            response['TXNAMOUNT']="₹ " +request.POST.get("TXNAMOUNT")
            response['TXNDATE']=request.POST.get("TXNDATE")
            response['BANKNAME']=request.POST.get("BANKNAME")
            if request.POST.get("STATUS") == "TXN_SUCCESS":
                response['STATUS']="SUCCESS"
                transaction.successful=True
                transaction.save()
                student.payment_verified=True
                student.save()
            elif request.POST.get("STATUS") == "TXN_FAILURE":
                response['STATUS']="FAILURE"
                student.delete()
            print(response)
        else:
            response = {}
            response['SAP_ID']=student.sap_id
            response['FULL_NAME']=student.full_name
            if student.is_member:
                response['MEMBER_OF_ACM']="YES"
            else:
                response['MEMBER_OF_ACM']="NO"
            response['NO_OF_COMPANIES']=student.no_of_companies
            response['MID']=request.POST.get("MID")
            response['TXNID']=request.POST.get("TXNID")
            response['ORDERID']=request.POST.get("ORDERID")
            response['BANKTXNID']=request.POST.get("BANKTXNID")
            response['TXNAMOUNT']="₹ " +request.POST.get("TXNAMOUNT")
            response['TXNDATE']=request.POST.get("TXNDATE")
            response['BANKNAME']=request.POST.get("BANKNAME")
            response['STATUS']="FAILURE"
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"
        
        return render(request, 'if/payments/callback.html', context=response)

def form2(request):
    com= FormCompany.objects.all()
    companies = []
    message = ""
    success = ""
    for c in com:
        x = []
        x.append(c.string())
        x.append(c.name)
        x.append(c.positionType)
        x.append(c.position)
        companies.append(x)
    if request.method == 'POST':
        name = request.POST.get("name")
        sap = request.POST.get("sap")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        whatsapp = request.POST.get("whatsapp")
        resume = request.POST.get("resume")
        department = request.POST.get("department")
        year = request.POST.get("year")
        is_member=False
        amount=0
        selected_companies = []
        for c in com:
            res = request.POST.get(c.string())
            if res is not None:
                selected_companies.append(c)
        if name=="":
            message = "Please Enter your Name"
        elif sap=="" or len(sap)!=11:
            message = "Please enter a 11 digit SAP ID"
        elif gender=="":
            message = "Please select a gender"
        elif email=="":
            message = "Please enter a valid Email ID"
        elif phone=="" or len(phone)!=10 or phone.isdigit()==False:
            message = "Please enter a valid Phone Number"
        elif whatsapp=="" or len(whatsapp)!=10 or whatsapp.isdigit()==False:
            message = "Please enter a valid Whatsapp Number"
        elif resume=="":
            message = "Please Enter a valid Drive Link of your Resume"
        elif department=="":
            message = "Please select a department"
        elif year=="":
            message = "Please select your year"
        elif len(selected_companies)==0:
            message = "Please select at least one company"
        
        if sap.isdigit():
            if sap[:4]=="6000":
                pass
            else:
                message = "Please enter a SAP ID starting with '6000' "
        else:
            message = "Please enter a SAP ID with only digits"


        if message!="":
            return render(request, "if/main/form2.html",{'companies':companies,'message':message})

        if sap in MEMBER_LIST:
            is_member=True
            
        if FormStudent.objects.filter(sap_id=sap).exists():
            student = FormStudent.objects.get(sap_id=sap)
            if student.payment_verified==True:
                message="You have already registered for Internship Fair"
                return render(request, "if/main/form2.html",{'companies':companies,'message':message})
            else:
                student.delete()
        
        no_of_companies = len(selected_companies)
        
        if message=="":
            student = FormStudent.objects.create(
                full_name = name,
                sap_id = sap,
                gender = gender,
                email_id = email,
                phone_no = phone,
                whatsapp_no = whatsapp,
                resume_drive_link = resume,
                department = department,
                year = year,
                is_member = is_member,
                amount = "",
            )
            for c in selected_companies:
                Form.objects.create(student=student,company=c)
            student.company_no_alloter()
            if student.is_member:
                if no_of_companies>3:
                    amount = (no_of_companies-3)*COST
                else:
                    amount = 0
                    student.payment_verified=True
            else:
                amount = no_of_companies * COST
                
            student.amount=amount
            student.save()
            if (amount==0):
                response = {}
                response['SAP_ID']=student.sap_id
                response['FULL_NAME']=student.full_name
                if student.is_member:
                    response['MEMBER_OF_ACM']="YES"
                else:
                    response['MEMBER_OF_ACM']="NO"
                response['NO_OF_COMPANIES']=student.no_of_companies
                response['MID']="-"
                response['TXNID']="-"
                response['ORDERID']="-"
                response['BANKTXNID']="-"
                response['TXNAMOUNT']="₹ 0" 
                response['TXNDATE']=datetime.datetime.now()
                response['BANKNAME']="-"
                response['STATUS']="SUCCESS"
                return render(request, "if/payments/callback.html",response)

            else:
                transaction = Transaction.objects.create(student=student, amount=student.amount)
                transaction.save()
                merchant_key = settings.PAYTM_SECRET_KEY
                params = (
                    ('MID', settings.PAYTM_MERCHANT_ID),
                    ('ORDER_ID', str(transaction.order_id)),
                    ('CUST_ID', str(transaction.student.sap_id)),
                    ('TXN_AMOUNT', str(transaction.amount)),
                    ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
                    ('WEBSITE', settings.PAYTM_WEBSITE),
                    # ('EMAIL', request.user.email),
                    # ('MOBILE_N0', '9911223388'),
                    ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
                    ('CALLBACK_URL', 'http://127.0.0.1:8000/if/callback/'),
                    # ('PAYMENT_MODE_ONLY', 'NO'),
                )

                paytm_params = dict(params)
                checksum = generate_checksum(paytm_params, merchant_key)
                
                transaction.checksum = checksum
                transaction.save()

                paytm_params['CHECKSUMHASH'] = checksum
                print('SENT: ', checksum)
                return render(request, 'if/payments/redirect.html', context=paytm_params)

    return render(request, "if/main/form2.html",{'companies':companies,'message':message,'success':success})

def export_excel_all(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename= Student List of IF.xls'
    wb = xlwt.Workbook(encoding='utf-8')

    # General Sheet
    ws=wb.add_sheet('Student and Company List')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True

    columns = ['SAP ID','Full Name','Gender','Email','Mobile','Whatsapp','Resume Link','Department','Year','Member of ACM?','Company','Position type','Position']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    
    font_style=xlwt.XFStyle()
    rows=Form.objects.filter(student__payment_verified=True).values_list('student__sap_id','student__full_name','student__gender','student__email_id','student__phone_no','student__whatsapp_no','student__resume_drive_link','student__department','student__year','student__is_member','company__name','company__positionType','company__position')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    
    #Sheet with Student Details
    ws=wb.add_sheet('Student List')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True

    columns = ['SAP ID','Full Name','Member of ACM?','No. of Companies','Payment Verified?','Amount']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style) 

    font_style=xlwt.XFStyle()
    rows=FormStudent.objects.filter(payment_verified=True).values_list('sap_id','full_name','is_member','no_of_companies','payment_verified','amount')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)

    
    # Sheet for each Company
    companies = FormCompany.objects.all()
    for company in companies:
        ws=wb.add_sheet('Student List for '+str(company.id))
        font_style=xlwt.XFStyle()
        font_style.font.bold=True
        ws.write(0,0,"Student List of "+company.string(),font_style)
        row_num = 1

        columns = ['SAP ID','Full Name','Gender','Email','Mobile','Whatsapp','Resume Link','Department','Year','Member of ACM']
        for col_num in range(len(columns)):
            ws.write(row_num,col_num,columns[col_num],font_style)
        
        font_style=xlwt.XFStyle()
        rows=Form.objects.filter(company=company,student__payment_verified=True).values_list('student__sap_id','student__full_name','student__gender','student__email_id','student__phone_no','student__whatsapp_no','student__resume_drive_link','student__department','student__year','student__is_member')
        for row in rows:
            row_num+=1
            for col_num in range(len(row)):
                ws.write(row_num,col_num,str(row[col_num]),font_style)
        



    wb.save(response)
    return response

def if_home(request):
    companies = Companies.objects.all()
    i = 0
    cols = []
    temp = []
    for company in companies:
        i = i + 1
        temp.append(company)
        if i == 6:
            cols.append(temp)
            i = 0
            temp = []
    if companies.count() < 6 or companies.count() % 6 > 0:
        cols.append(temp)
    return render(request, 'if/main/if.html',{'cols':cols,'range':range(len(cols))})

def job_profile(request):
    companies = Companies.objects.all().order_by("Company_name")
    return render(request, 'if/main/JobProfile.html',{'companies':companies})

def job_single(request,id):
    try:
        company = Companies.objects.get(id=id)
    except Companies.DoesNotExist:
        return render(request, 'if/main/JobSingle.html')
    return render(request, 'if/main/JobSingle.html',{'company':company})

def form(request):
    return render(request, 'if/main/proof_form.html')

def form3(request):
    com= FormCompany.objects.all().order_by("name")
    companies_total = FormCompany.objects.all().count()
    companies = []
    categories = []
    message = ""
    success = ""
    category_set= set()
    for c in com:
        category_set.add(c.name+"|"+c.positionType)
    for category in category_set:
        x = []
        x.append(category.split("|")[0]+" ["+category.split("|")[1]+"]")
        sub_category = FormCompany.objects.filter(name=category.split("|")[0],positionType=category.split("|")[1])
        y=[]
        for sub in sub_category:
            y.append(sub)
        x.append(y)
        categories.append(x)
    categories.sort()
    for c in com:
        x = []
        x.append(c.string())
        x.append(c.name)
        x.append(c.positionType)
        x.append(c.position)
        companies.append(x)
    if request.method == 'POST':
        name = request.POST.get("name")
        sap = request.POST.get("sap")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        whatsapp = request.POST.get("whatsapp")
        resume = request.POST.get("resume")
        department = request.POST.get("department")
        year = request.POST.get("year")
        proof = request.FILES.get("paymentconfirmation")
        is_member=False
        amount=0
        selected_companies = []
        selected_companies2 = set()
        for c in com:
            res = request.POST.get(c.string())
            if res is not None:
                selected_companies.append(c)
        for c in selected_companies:
            selected_companies2.add(c.string2())
        if name=="":
            message = "Please Enter your Name"
        elif sap=="" or len(sap)!=11:
            message = "Please enter a 11 digit SAP ID"
        elif gender=="":
            message = "Please select a gender"
        elif email=="":
            message = "Please enter a valid Email ID"
        elif phone=="" or len(phone)!=10 or phone.isdigit()==False:
            message = "Please enter a valid Phone Number"
        elif whatsapp=="" or len(whatsapp)!=10 or whatsapp.isdigit()==False:
            message = "Please enter a valid Whatsapp Number"
        elif resume=="":
            message = "Please Enter a valid Drive Link of your Resume"
        elif department=="":
            message = "Please select a department"
        elif year=="":
            message = "Please select your year"
        elif len(selected_companies2)==0:
            message = "Please select at least one company"
        
        if sap.isdigit():
            if sap[:3]=="600":
                pass
            else:
                message = "Please enter a SAP ID starting with '600' "
        else:
            message = "Please enter a SAP ID with only digits"
        
        if message!="":
            return render(request, "if/main/form3.html",{'categories':categories,'companies':companies,'companies_total':companies_total,'message':message})

        if sap in MEMBER_LIST:
            is_member=True
        
        if FormStudent.objects.filter(sap_id=sap).exists():
            message="You have already registered for Internship Fair"
            return render(request, "if/main/form3.html",{'categories':categories,'companies':companies,'companies_total':companies_total,'message':message})
        
        no_of_companies = len(selected_companies2)
        if is_member:
            if no_of_companies>3:
                if proof is None or proof=="":
                    message="Please submit your Payment proof"
        else:
            if proof is None or proof=="":
                message="Please submit your Payment proof"
        
        if message=="":
            student = FormStudent.objects.create(
                full_name = name,
                sap_id = sap,
                gender = gender,
                email_id = email,
                phone_no = phone,
                whatsapp_no = whatsapp,
                resume_drive_link = resume,
                department = department,
                year = year,
                is_member = is_member,
                amount = "",
                payment_receipt = proof,
                no_of_companies = len(selected_companies2)
            )
            for c in selected_companies:
                Form.objects.create(student=student,company=c)
            if student.is_member:
                if no_of_companies>3:
                    amount = (no_of_companies-3)*COST
                else:
                    amount = 0
            else:
                amount = no_of_companies * COST
                
            student.amount=amount
            student.save()
            success = "Yes"
            response = {}
            response["FULL_NAME"]=student.full_name
            response["SAP_ID"]=student.sap_id
            if student.is_member:
                response["IS_MEMBER"]="Yes"
            else:
                response["IS_MEMBER"]="No"
            response["NO_OF_COMPANIES"]=student.no_of_companies
            response["NO_OF_INTERVIEWS"]=len(selected_companies)
            response["AMOUNT"]=student.amount
            comp = []
            for c in selected_companies:
                x = []
                x.append(c.name)
                x.append(c.positionType)
                x.append(c.position)
                comp.append(x)
            response["COMPANIES"]=comp
            return render(request,"if/main/proof_form.html",response)
        else:
            return render(request, "if/main/form3.html",{'categories':categories,'companies':companies,'companies_total':companies_total,'message':message})

    return render(request, "if/main/form3.html",{'categories':categories,'companies':companies,'companies_total':companies_total,'message':message,'success':success})


def closed_register(request):
    return render(request,'if/main/closed.html')

def refund(request):
    # forms = Form.objects.all()
    # for i in forms:
    #     i.attended=True
    #     i.save()

    # students = FormStudent.objects.all().order_by("full_name")
    # for s in students:
    #     s.refund_amount=0
    #     s.refund_saved=False
    #     s.save()
    if request.method=="GET":
        students = FormStudent.objects.all().order_by("full_name")
        refund=[]
        for student in students:
            x=[]
            x.append(student.id)
            x.append(student.full_name)
            if student.refund_saved:
                refund_amount=student.refund_amount
            else:
                refund_amount=0
                unattended_interviews = Form.objects.filter(student=student,attended=False)
                unattended_categories = set()
                for interview in unattended_interviews:
                    unattended_categories.add(interview.company.string2())
                
                attended_interviews = Form.objects.filter(student=student,attended=True)
                attended_categories = set()
                for interview in attended_interviews:
                    attended_categories.add(interview.company.string2())
                
                for c in attended_categories:
                    if c in unattended_categories:
                        unattended_categories.remove(c)
                
                if len(unattended_categories)==0:
                    refund_amount=0
                else:
                    if student.is_member:
                        if (student.no_of_companies-len(unattended_categories))<=3:
                            refund_amount=student.amount
                        else:
                            refund_amount=len(unattended_categories)*50
                    else:
                        refund_amount=len(unattended_categories)*50
            x.append(student.amount)
            x.append(student.is_member)
            x.append(refund_amount)
            if student.payment_receipt=="":
                x.append("")
            else:
                x.append(student.payment_receipt.url)
            if student.refund_saved:
                x.append("Yes")
            else:
                x.append("")
            refund.append(x)   
        return render(request,'if/main/refund.html',{"refund":refund})
    elif request.method=="POST":
        students = FormStudent.objects.all().order_by("full_name")
        for student in students:
            check=request.POST.get(str(student.id))
            if check is not None:
                print(student.full_name)
                refund_amount=request.POST.get("r"+str(student.id))
                student.refund_amount=refund_amount
                student.refund_saved=True
                student.save()
        return render(request,'if/main/refund.html')
        
            
        

def refund_detail(request,id):
    refund_amount=0
    student = FormStudent.objects.get(id=id)

    total_interviews = Form.objects.filter(student=student)
    total_categories = set()
    for interview in total_interviews:
        total_categories.add(interview.company.string2())
    
    unattended_interviews = Form.objects.filter(student=student,attended=False)
    unattended_categories = set()
    for interview in unattended_interviews:
        unattended_categories.add(interview.company.string2())
    
    attended_interviews = Form.objects.filter(student=student,attended=True)
    attended_categories = set()
    for interview in attended_interviews:
        attended_categories.add(interview.company.string2())
        
    for c in attended_categories:
        if c in unattended_categories:
            unattended_categories.remove(c)
    
    if student.refund_saved:
        refund_amount=student.refund_amount
    else:
        if len(unattended_categories)==0:
            refund_amount=0
        else:
            if student.is_member:
                if (student.no_of_companies-len(unattended_categories))<=3:
                    refund_amount=student.amount
                else:
                    refund_amount=len(unattended_categories)*50
            else:
                refund_amount=len(unattended_categories)*50
    
    return render(request,'if/main/refund_detail.html',{"total_interviews":total_interviews,
                                                        "total_categories":total_categories,
                                                        "unattended_interviews":unattended_interviews,
                                                        "unattended_categories":unattended_categories,
                                                        "amount_paid":student.amount,
                                                        "refund_amount":refund_amount,
                                                        "student":student})


def changing(request):
    if request.method == "GET":
        monke_company1 = FormCompany.objects.get(name="Yocket", positionType="Non Tech", position="SEO")

        form = Form.objects.filter(company=monke_company1).update(attended=False)

        print(form)
        return HttpResponse(form)