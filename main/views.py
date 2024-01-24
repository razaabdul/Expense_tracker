from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
# from .models import Transaction  # Import your Transaction model
from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout   
import matplotlib.pyplot as plt
from calendar import HTMLCalendar
from datetime import datetime
import calendar
import numpy as np 
import calendar
from io import BytesIO
import base64
from collections import Counter
# from fpdf import FPDF
from django.template.loader import get_template
plt.switch_backend('agg') # used to solve main thread error
def repeated(request):
    exp=expense.objects.filter(user=request.user,transaction_type="PAYED")
    cat=Category.objects.filter(user=request.user)
    str=""
    v=0
    dict={}       
    for c in cat:
        for e in exp:
            if c.name == e.category_name.name and e.transaction_type == "PAYED": 
                    c.val += float(e.amount)
        v=c.val
        str=c.name
        if str in dict:
            dict[str]=(v)
        else:
            dict[str]=v
            print(str,"=============",v)
        for key in list(dict.keys()):
            if dict[key]==0:
                del dict[key]
    lab=list(dict.keys())
    size=list(dict.values())
    dict2={}
    value=[]
    v=[]
    c=0
    for e in exp:
        str=e.category_name
        amt=e.amount
        if str in dict2: 
            value=[dict2[str][0]+1,dict2[str][1]+(float(amt))]
            dict2[str]=value
            c += float(amt)
        else:
            value=[1,float(amt)]
            dict2[str]=value 
            c += float(amt)   
    print("======>",c)    
    dictt=(dict2.items())
    print("----------------------",dictt)
       
    plt.figure()  
    plt.pie(size,labels=lab,radius=0.9,autopct="%0.1f%%",startangle=150)
    plt.savefig('main/static/pie_chart.png')
    return render(request,'repeated_category.html',{'d':dictt,'total':c,'catt':cat})

def user_info(request):
    return render(request,'user_info.html')
def graph(request):
    user_Profile=profile.objects.filter(user=request.user).first()
    user_expense=expense.objects.filter(user=request.user,transaction_type="PAYED").order_by('-id')
    cat=Category.objects.filter(user=request.user)
    exp=expense.objects.filter(user=request.user)   
    str=""
    v=0
    Total_exp=0
    dict={}  
    for ex in user_expense:
        Total_exp+=float(ex.amount)  
    print("----=>",Total_exp)           
    for c in cat:
        for e in exp:
            if c.name == e.category_name.name and e.transaction_type == "PAYED": 
                    print(c.name,"---------",e.category_name)
                    c.val += float(e.amount)
          

                             
        v=c.val
        # print("v---------------",v)   
        str=c.name
        if str in dict:
            dict[str]=v
        else:
            dict[str] = v
    # print("dsds",dict)    

    for key in list(dict.keys()):
        if dict[key]==0:
            del dict[key]
            
    lab=list(dict.keys())
    # print("----lab----",lab)
    size=list(dict.values())
    # print("size----------------",size)
    plt.figure()  
    plt.pie(size,labels=lab,shadow=True,radius=0.9,autopct="%0.1f%%",startangle=150)
    plt.savefig('main/static/pie_chart.png')
    
    return render(request,'graph.html',context={'profile':user_Profile,'expense':user_expense,'total':Total_exp})

def monthly_expense(request,year=datetime.now().year,month=datetime.now().strftime('%B')):
    global  select_month_name
    expense_date=expense.objects.all()
    user_Profile=profile.objects.filter(user=request.user).first()
    dict={}
    value=0
    income=0
    month_exp=0
    select_month_name=month
    if request.GET.get('months'):
        select_month_name=request.GET.get('months')
    select_month_name=select_month_name.capitalize()
    current_m=list(calendar.month_name).index(select_month_name) #it will convert string into integer value (list(calender.month name select your months from calender))
    expense_date=expense.objects.filter(user=request.user,date__month=current_m,transaction_type="PAYED").order_by()[::1]
    Income=expense.objects.filter(user=request.user,date__month=current_m,transaction_type="RECIEVED")
    for ex in expense_date:
        value+=float(ex.amount)
        month_exp=value
    for inc in Income:
        income+=inc.amount

    for e in expense_date:
        dict[e.category_name.name]=float(e.amount)


    if month_exp <= 0:
        messages.info(request,"No expenses in this month") 
        redirect('/monthly_expense/')

    lab=list(dict.keys())
    print("==============",lab)
    size=list(dict.values()) 
    print("=======v=====",size) 
          
    plt.figure(select_month_name)  
    plt.pie(size,labels=lab,radius=0.9,autopct="%0.1f%%",startangle=150)
    plt.axis('equal')
    plt.title(select_month_name)
    plt.savefig('main/static/pie_chart_2.png')
    return render(request,"monthly_expense.html",context={'total_income':income,'profile':user_Profile,'expense':expense_date,'monthly_expense':month_exp,'m_name':select_month_name})
def transaction(request):
    user_Profile=profile.objects.filter(user=request.user).first()
    user_expense=expense.objects.filter(user=request.user).order_by('-id')
    if request.method=="GET":
        st=request.GET.get('search')
        
        if st!=None:
            user_expense=expense.objects.filter(category_name=st)
            # current_l=(calendar.month_name).index(user_expense)
    total=0
    for exp in user_expense:
         total += exp.amount

    income=user_income.objects.filter(user=request.user).order_by('-id')

     
    return render(request,"transaction_detail.html",context={'profile':user_Profile,'expense':user_expense,'income':income })

def home(request, id=None):
    user_Profile=profile.objects.filter(user=request.user).first()
    user_expense=expense.objects.filter(user=request.user).order_by('-id')
    exp=expense.objects.filter(user=request.user,transaction_type="PAYED")
    t_income=expense.objects.filter(user=request.user,transaction_type="RECIEVED")

    if request.GET.get('search'):
        month_name=request.GET.get('search')
        month_name=month_name.capitalize()
        current_month=list(calendar.month_name).index(month_name)
        user_expense=expense.objects.filter(user=request.user,date__month=current_month,transaction_type="PAYED").order_by('-id')

    total_exp=0
    total_inc=0
    for ex in exp:
         total_exp += ex.amount
    for inc in t_income:
        total_inc += inc.amount    


    income=user_income.objects.filter(user=request.user).order_by('-id')

    return render(request,'home.html', context={'profile':user_Profile,'expense':user_expense,'income':income,'total':total_exp,'total_inc':total_inc})

def add(request):
    user_profile=profile.objects.filter(user=request.user).first()
    USER_INCOME=user_income.objects.all()[::-1]
    category_namee=Category.objects.filter(user=request.user)
    payment_mode=Paymentmode.objects.all()
    cat=Category.objects.filter(user=request.user)

    if request.method=="POST":
        cat_id=request.POST.get('cat_name')
        cat_name = Category.objects.get(id=cat_id)
        amount=request.POST.get('amount')
        mode_id=request.POST.get('pay_mode')
        mode_type=Paymentmode.objects.get(id=mode_id)
        person=request.POST.get('person')
        date=request.POST.get('date')
        transaction_type=request.POST.get('transaction_type')
        income=request.POST.get('income_hidden')



        if transaction_type == "RECIEVED":
            user_profile.balance += float(amount)
        else:         
            if user_profile.balance > float(amount):
                user_profile.expenses += float(amount)
                user_profile.balance -= float(amount)   

            else:
                messages.info(request,'insufficient balance')
                return redirect("/add/")
        if user_profile.balance  == 0:
            if request.method == 'POST':
                amount = float(request.POST.get('amount',0))
                if amount > 0:
                    user_profile.balance += amount
                    user_profile.save()
                    return redirect('/home/') 
                else:    
                    messages.info(request,"oops!! your balance is less than Expenses ")
                    return redirect('/add/')  
        expenses=expense(date=date,category_name=cat_name,person=person,amount=amount,payment_mode=mode_type,transaction_type=transaction_type,user=request.user)
        expenses.save()

        user_profile.save()
        return redirect('/home/')
    contextt={"categoryy":category_namee,
    'pay_mode':payment_mode,
    'cat':cat
    
    }
    return render(request,'add_detail.html',contextt)    
def loginn(request):
 
    if request.method=="POST":
        data=request.POST
        username=data.get('username')
        password=data.get('password')
        

        if  not User.objects.filter(username=username).exists():
            messages.error(request,'invalid usernamee')
            return redirect('/login/')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'invalid username')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/home/')    
                    
    return render(request,'login.html')

def add_category_byuser(request):
    if request.method=="POST":
        
        category_byuser=request.POST.get('add_category')
        value=request.POST.get('val')

        cat = Category.objects.create(user=request.user,val=value,name=category_byuser)
        cat.save()
        return redirect('/add/')

    return render(request,'add_detail.html')

def income(request):
    user_profile=profile.objects.filter(user=request.user).first()
    USER_INCOME=user_income.objects.all()
    extra_incomee=extra_income.objects.filter(user=request.user)

    if request.method =="POST":
   
        person=request.POST.get('person')
        Income=request.POST.get('income')
        purpose=request.POST.get('purpose')


        
        user_profile.balance += float(Income)

        user_profile.income += float(Income)
        

        U_INCOME=user_income(u_income=Income,person=person,purpose=purpose,user=request.user)
        U_INCOME.save()
        user_profile.save()
        return redirect('/home/')

    
    
    return render(request,"home.html")

def register(request):
    if request.method=="POST":
        data=request.POST
        first_name=data.get('firstname')
        last_name=data.get('lastname')
        username=data.get('username')
        password =data.get('password')
    
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'user already exists')
            return redirect('/login/')
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            )

    
        
        user.set_password(password) 
        user.save()
        user_profile =profile.objects.create(
            user=user,
            income = 0
             )
        user_profile.save()
       
        

        messages.info(request,'account created successfully')
        return redirect('/login/') 
    
    return render(request,'login.html')
def index(request):
    return render(request,'index.html')
def new(request):
    return render(request,'new.html')

def user_logout(request):
    logout(request)
    messages.success(request,())
    return redirect('/login/')    

def update(request,id):
    update_expense=expense.objects.get(id=id)
    user_profilee=profile.objects.get(user=update_expense.user)
    payment_mode=Paymentmode.objects.all()
    all_category=Category.objects.all()
  

    if request.method=="POST":
        user_person = request.POST.get('person')
        cat_id = request.POST.get('cat_name')
        date=request.POST.get('date')
        cat_name = Category.objects.get(id=cat_id)
        amount = request.POST.get('amount')
        pay_mod_id = request.POST.get('pay_mode')
        pay_mode_name = Paymentmode.objects.get(id=pay_mod_id)
        trans_type = request.POST.get('transaction_type')
        
        if update_expense.transaction_type == "RECIEVED":
            if trans_type == "RECIEVED":
                if float(user_profilee.balance) - float(update_expense.amount) + float(amount) >= 0 :
                         
                  
                        user_profilee.balance = float(user_profilee.balance) - float(update_expense.amount) + float(amount)
                      
                        user_profilee.save()
                        
                        update_expense.person = user_person
                        update_expense.category_name = cat_name
                        update_expense.amount = amount
                        update_expense.date=date 
                        update_expense.payment_mode = pay_mode_name
                        update_expense.transaction_type = trans_type
                        
                          
                        
                        update_expense.save()
                        messages.info(request, 'Transition update successfully')
                        return redirect('/home/')
                else:
                        messages.info(request, 'insufficient income')  
                        return redirect(f"/update/{update_expense.id}/")
                


            else:
                if (float(user_profilee.balance) - float(update_expense.amount)) >= float(amount):
                         
                        user_profilee.balance = float(user_profilee.balance) - float(update_expense.amount) - float(amount)
                    
                        user_profilee.expenses = float(user_profilee.expenses) + float(amount)
                        user_profilee.save()

                        update_expense.person = user_person
                        update_expense.category_name = cat_name
                        update_expense.date=date 
                        update_expense.amount = amount
                        update_expense.payment_mode = pay_mode_name
                        update_expense.transaction_type = trans_type
                        
                            
                        
                        update_expense.save()
                        messages.info(request, 'Transition update successfully')
                        return redirect('/home/')
                else:
                        messages.info(request, 'expense is too high according to Balance')  
                        return redirect(f"/update/{update_expense.id}/")
            


        else:
             if trans_type == "PAYED":
                if (float(user_profilee.balance) + float(update_expense.amount)) >= float(amount)  :
                        
                        user_profilee.balance= float(user_profilee.balance) + float(update_expense.amount) - float(amount)
                        user_profilee.expenses = float(user_profilee.expenses) - float(update_expense.amount) + float(amount)
                        user_profilee.save()
       
                        update_expense.person = user_person
                        update_expense.date=date                       
                        update_expense.category_name = cat_name
                        update_expense.amount = amount
                        update_expense.payment_mode = pay_mode_name
                        update_expense.transaction_type = trans_type
                          
                       
                        update_expense.save()
                        messages.info(request, 'Transition update successfully')
                        return redirect('/home/')
                else:
                        messages.info(request, 'expense is too high according Balance')  
                        return redirect(f"/update/{update_expense.id}/")
            
             else:
                
                  
                    user_profilee.balance = float(user_profilee.balance) + float(update_expense.amount) + float(amount)
                    user_profilee.expenses = float(user_profilee.expenses) - float(update_expense.amount)
                    
                    user_profilee.save()
                    
                    update_expense.person = user_person
                    update_expense.category_name = cat_name
                    update_expense.amount = amount
                    update_expense.date=date 
                    update_expense.payment_mode = pay_mode_name
                    update_expense.transaction_type = trans_type

                    update_expense.save()
                    messages.info(request, 'Transition update successfully')
                    return redirect('/home/')
    
    update_data={'updatee':user_profilee,
    'p_mode':payment_mode,
    'category':all_category,
    "update_expense": update_expense}

    return render(request,'update.html',update_data)    

def delete(request,id):
    user_expense = expense.objects.get(id=id)
    user_profilee=profile.objects.get(user=user_expense.user)
    if user_expense.transaction_type=="PAYED":
        user_profilee.balance = float( user_profilee.balance) + float(user_expense.amount)
        user_profilee.expenses = float(user_profilee.expenses) - float(user_expense.amount)
        user_profilee.save()
    else:
        if user_expense.amount > user_profilee.balance:
          messages.info(request,'can not delete expense , your expense will be negative ')
          return redirect('/home/')
        user_profilee.balance = float(user_profilee.balance) - float(user_expense.amount)
        # user_profilee.income = float(user_profilee.income) - float(user_expense.amount)graph
        user_profilee.save() 

        
        
      

   
    user_expense.delete()

    return redirect('/home/')  
def indeex(request):
    return render(request,'index.html')
def income_update(request,id):
    update_query = user_income.objects.get(id=id)
    user_profilee=profile.objects.get(user=update_query.user)

    if request.method=="POST":
        update_person=request.POST.get('person')
        update_deposite=request.POST.get('amount')
        update_purpose=request.POST.get('Purpose')
        

        user_profilee.balance = float(user_profilee.balance) - float(update_query.u_income)
        user_profilee.income = float(user_profilee.income)- float(update_query.u_income)
      
        update_query.person = update_person
        update_query.u_income = update_deposite
        update_query.purpose = update_purpose

      
        user_profilee.balance = float(user_profilee.balance) + float(update_deposite)
        user_profilee.income = float(user_profilee.income) + float(update_deposite)

        user_profilee.save()
        update_query.save()
        return redirect('/home/')
    
    return render(request,'update_income.html',{'update_user_income':update_query}) 

def delete_income(request,id):
    user_income_profile=user_income.objects.get(id=id)
    update_profile= profile.objects.get(user=user_income_profile.user) 
    if update_profile.balance - user_income_profile.u_income>0:
        update_profile.balance -= float(user_income_profile.u_income)
        user_income_profile.delete()
        update_profile.save()
    return redirect('/home/')
    return render(request,'home.html')

def date_hist(request,year=datetime.now().year,month=datetime.now().strftime('%B'),day=datetime.now):
    month=month.capitalize()
    year=year
    month_number=list(calendar.month_name).index(month)
    month_number=int(month_number)
   
    dict={}
    monthly_sum=0
    for i in range(13):
        monthly_sum=0
        if i==0:
            continue
    
        expense_date=expense.objects.filter(user=request.user,date__year=year,date__month=i,transaction_type="PAYED").order_by()[::1]
        for ex in expense_date:
            monthly_sum += ex.amount
            print(ex.category_name,'====>',i,'------',monthly_sum)
        dict[i]=monthly_sum


    lab=list(dict.keys())

    size=list(dict.values())  
          
    plt.figure()  
    plt.pie(size,labels=lab,radius=1.1,autopct="%0.1f%%",startangle=150)
    plt.axis('equal')
    plt.savefig('main/static/pie_chart_2.png')




    return render(request,'date_history.html',{
        'event_list':expense_date,
        'month_number':month_number,
        'year':year
    })

def yearly_expense(request,year=datetime.now().year,month=datetime.now().strftime('%B'),day=datetime.now()):
    # p=profile.objects.filter(user=request.user).first()


    select_year=str(year)
    value=0

   
    dict={}
    dict1={}
    
    if request.GET.get('yearly'):
        select_year=request.GET.get('yearly')
        # month_name=month_name.capitalize()
    # current_y=list(calendar.isleap(year)).index(year_name) #it will convert string into integer value (list(calender.month name select your months from calender))
    expense_date=expense.objects.filter(user=request.user,date__year=select_year,transaction_type="PAYED").order_by()[::1]
    
    for ex in expense_date:
        value+=float(ex.amount)
   
    for i in range(13):
        expense_sum=0
        income_sum=0
        if i==0:
            continue 
        expense_date=expense.objects.filter(user=request.user,date__year=select_year,date__month=i,transaction_type="PAYED").order_by()[::1]
        for ex in expense_date:
            expense_sum += ex.amount
        dict[i]=expense_sum 
        expense_datee=expense.objects.filter(user=request.user,date__year=select_year,date__month=i,transaction_type="RECIEVED").order_by()[::1]
        for exp in expense_datee:
            income_sum += exp.amount   
        dict1[i]=income_sum
        
    
    months=['Jan','Feb','Mar','apr','may','Jun','July','Aug','Sep','Oct','Nov','Dec']
    income=list(dict1.values())  

    
     
    xpos=np.arange(len(months)) 
    yxps=np.arange(len(income))  
    # print("--->",xpos)      
    expenses=list(dict.values())
    for i,v in enumerate(expenses): # to show graph amount on graph
        plt.text(i,v,str(v),ha='center',size=5,weight='bold')  
    for i,v in enumerate(income): # to show graph amount on graph
        plt.text(i,v,str(v),ha='center',size=5,weight='bold')  
    
    plt.xticks(yxps,months)

                   
    plt.bar(xpos,expenses,width=0.3 ,color='red',alpha=0.7,label='Expenses')
    plt.bar(xpos+0.3,income,width=0.3,color='darkblue',alpha=0.7,label='Income')

    plt.xlabel('months')
    plt.ylabel('Amount ($)')
    plt.title('Annual Income And Expense of'+select_year)
    plt.legend()
    plt.tight_layout()
    buffer=BytesIO()
    plt.savefig(buffer,format='png')
    plt.close
    graph=base64.b64encode(buffer.getvalue()).decode('utf-8')

          
    plt.figure()
      
  
    return render(request,'yearly_expense.html',{'graph':graph,'expense_sum':value,'income_sum':income_sum})


# def print_pdf(request):


def generate_pdf(request,year=datetime.now().year,month=datetime.now().strftime('%B'),day=datetime.now):
    # user_transactions = expense.objects.filter(user=request.user)
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="user_transaction_report.pdf"'
    month_name=select_month_name
    month_name=month_name.capitalize()
    l=list(calendar.month_name).index(month_name)
    # Create a BytesIO buffer to receive the PDF data .
    p =canvas.Canvas(response)
    p.drawString(100, 750, "User Transaction Report")
    lst=[]
    y = 700
    user_transaction=expense.objects.filter(user=request.user,date__month=l,transaction_type="PAYED")
    for transaction in user_transaction:
        p.drawString(500, y, f"Amount: {transaction.amount}")
        p.drawString(100, y, f"person: {transaction.person}")
        p.drawString(200, y, f"category: {transaction.category_name}")
        p.drawString(300, y, f"Date: {transaction.date}")

        # p.drawString(200, y, f"tracsaction: {transaction.transaction_type}")
        y -= 20

    # Close the PDF object cleanly and we're done.
    p.showPage()
    p.save()

    return response


# def delete_cat(request,category_id):
#     catt=Category.objects.filter(user=request.user,pk=category_id)
#     p=profile.objects.filter(user=request.user).first()
#     e=expense.objects.filter(user=request.user)

#     for exp in e:
            
#         if exp.transaction_type=="PAYED":
#             p.expenses=float(p.expenses)-float(exp.amount)
#             p.balance=float(p.balance)+float(exp.amount)
#             p.save()
#         elif exp.transaction_type=="RECIEVED": 
#             p.balance=float(p.balance)-float(exp.amount)    
#             p.save()
#             exp.save()  
#         else:
#             messages.info(request,'')      


    
#     catt.delete()
#     return redirect('/add/')
# def category(request):
#     cat=Category.objects.filter(user=request.user)
#     return render(request,'cat_page.html',{'cat':cat})
