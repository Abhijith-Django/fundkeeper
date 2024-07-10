from django.shortcuts import render,redirect

from django.views.generic import View

from budget.forms import ExpenseForm,IncomeForm,RegistrationForm,LoginForm,SummaryForm

from budget.models import Expense,Income

from django.contrib import messages

from django.db.models import Sum

from django.utils import timezone

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from budget.decorators import signin_required

from django.utils.decorators import method_decorator # function decorator => method decorator

import datetime


 
@method_decorator(signin_required,name="dispatch")
class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()

        qs=Expense.objects.filter(user_object=request.user).order_by("-created_date") #login user object expense

        return render(request,"expense_add.html",{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

            # form_instance.instance.user_object=request.user

            # form_instance.save()     only for modelform

            data=form_instance.cleaned_data

            Expense.objects.create(**data,user_object=request.user)

            messages.success(request,"expense has been created")

            print("expense has been created")

            return redirect("expense-add")
        
        else:

            messages.error(request,"expense not created")

            return render(request,"expense_add.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

        

        id=kwargs.get("pk")

        expense_object=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_object)

        return render(request,"expense_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

       

        id=kwargs.get("pk")

        expense_object=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_object,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"expense updated")

            return redirect("expense-add")
        
        else:

            messages.error(request,"failed to update")

            return render(request,"expense_edit.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):


        id=kwargs.get("pk")

        qs=Expense.objects.get(id=id)

        return render(request,"expense_detail.html",{"data":qs})


@method_decorator(signin_required,name="dispatch")
class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):
         

        id=kwargs.get("pk")

        Expense.objects.get(id=id).delete()

        messages.success(request,"expense deleted")

        return redirect("expense-add")

@method_decorator(signin_required,name="dispatch")
class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):
 

        current_month=timezone.now().month

        current_year=timezone.now().year

        expense_list=Expense.objects.filter(created_date__month=current_month,created_date__year=current_year,user_object=request.user)

        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

        print(expense_total)

        expense_category_total=expense_list.values("category").annotate(total=Sum("amount"))

        print(expense_category_total)

        expense_priority=expense_list.values("priority").annotate(total=Sum("amount"))

        print(expense_priority)

        data={
            "expense_total":expense_total,
            "expense_category":expense_category_total,
            "expense_priority":expense_priority
        }

        return render(request,"expense_summary.html",data)

@method_decorator(signin_required,name="dispatch")
class IncomeCreateView(View):

    def get(self,request,*args,**kwargs):
 

        form_instance=IncomeForm()

        qs=Income.objects.filter(user_object=request.user).order_by("-created_data")

        return render(request,"income_add.html",{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):

        form_instance=IncomeForm(request.POST)

        if form_instance.is_valid():

            # form_instance.save()

            data=form_instance.cleaned_data

            Income.objects.create(**data,user_object=request.user)

            messages.success(request,"income has created")

            return redirect("income-add")
        
        else:

            messages.error(request,"income has not created")

            return render(request,"income_add.html",{"form":form_instance})
    

@method_decorator(signin_required,name="dispatch")
class IncomeUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        income_object=Income.objects.get(id=id)

        form_instance=IncomeForm(instance=income_object)

        return render(request,"income_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        income_object=Income.objects.get(id=id)

        form_instance=IncomeForm(instance=income_object,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"income updated")

            return redirect("income-add")
        
        else:

            messages.error(request,'income not updated')

            return redirect(request,"income_edit.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")     
class IncomeDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Income.objects.get(id=id)

        return render(request,"income_detail.html",{"data":qs})
    

@method_decorator(signin_required,name="dispatch")
class IncomeDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Income.objects.get(id=id).delete()

        messages.success(request,"income deleted")

        return redirect("income-add")
    

class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            # form_instance.save()

            data=form_instance.cleaned_data

            User.objects.create_user(**data)#this will encrypt the password

            return redirect("signin")
        
        else:

            return render(request,"register.html",{"form":form_instance})
        

class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("dash-board")
        

        messages.error(request,"authentication failed invalid credential")
           
        return render(request,"login.html",{"form":form_instance})
        

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    

class DashBoardView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        expense_list=Expense.objects.filter(user_object=request.user,created_date__month=current_month,created_date__year=current_year)
        
        print(expense_list,"expense_list")

        income_list=Income.objects.filter(user_object=request.user,created_data__month=current_month,created_data__year=current_year)

        print(income_list,"income_list")

        form_instance=SummaryForm()

        total_expense=expense_list.values("amount").aggregate(total=Sum("amount"))

        total_income=income_list.values("amount").aggregate(total=Sum("amount"))

        print(total_expense,"expense")

        print(total_income,"income")

        monthly_expense={}

        monthly_income={}

        for month in range(1,13):

            start_date=datetime.date(current_year,month,1)
            if month==12:
                end_date=datetime.date(current_year+1,1,1)

            else:
                end_date=datetime.date(current_year,month+1,1)

            monthly_expense_total=Expense.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date).aggregate(total=Sum("amount"))["total"]
            
            monthly_expense[start_date.strftime("%B")]=monthly_expense_total if monthly_expense_total else 0

            monthly_income_total=Income.objects.filter(user_object=request.user,created_data__gte=start_date,created_data__lte=end_date).aggregate(total=Sum("amount"))["total"]

            monthly_income[start_date.strftime("%B")]=monthly_income_total if monthly_income_total else 0

            print(monthly_expense)

            print(monthly_income)


        return render(request,"dashboard.html",{
            "expense":total_expense,
            "income":total_income,
            "form":form_instance,
            "monthly_expense":monthly_expense,
            "monthly_income":monthly_income
            }
            )
    
    def post(self,request,*args,**kwargs):

        form_instance=SummaryForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            start_date=data.get("start date")

            end_date=data.get("end date")

            expense_list=Expense.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date)
        
            print(expense_list,"expense_list")

            income_list=Income.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date)

            print(income_list,"income_list")

            form_instance=SummaryForm()

            total_expense=expense_list.values("amount").aggregate(total=Sum("amount"))

            total_income=income_list.values("amount").aggregate(total=Sum("amount"))

            print(total_expense,"expense")

            print(total_income,"income")

            return render(request,"dashboard.html",{"expense":total_expense,"income":total_income,"form":form_instance})
    



            