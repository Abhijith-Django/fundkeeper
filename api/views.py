from django.shortcuts import render

# Create your views here.

from django.utils import timezone

from django.db.models import Sum

from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet

from rest_framework import authentication,permissions

from api.serializers import UserSerializer,ExpenseSerializer,IncomeSerializer

from api.permissions import OwnerOnly

from budget.models import Expense,Income

class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        
class ExpenseViewSet(ModelViewSet):

    serializer_class=ExpenseSerializer

    queryset=Expense.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]

    def list(self,request,*args,**kwargs):

        qs=Expense.objects.filter(user_object=request.user)

        serializer_instance=ExpenseSerializer(qs,many=True)

        return Response(data=serializer_instance.data)
    
    def perform_create(self,serializer):
        
        return serializer.save(user_object=self.request.user)
    

class ExpenseSummaryView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        all_expenses=Expense.objects.filter(
                                              user_object=request.user,

                                              created_date__month=current_month,

                                              created_date__year=current_year
                                           )
        
        expense_total=all_expenses.values("amount").aggregate(total=Sum("amount")) 

        category_summary=all_expenses.values("category").annotate(total=Sum("amount")) 

        priority_summary=all_expenses.values("priority").annotate(total=Sum("amount"))

        data={
            "total_expense":expense_total,
            "category_summary":category_summary,
            "priority_summary":priority_summary
        }

        return Response(data=data)





class IncomeViewSet(ModelViewSet):

    serializer_class=IncomeSerializer

    queryset=Income.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]

    def list(self,request,*args,**kwargs):

        qs=Income.objects.filter(user_object=request.user)

        serializer_instance=IncomeSerializer(qs,many=True)

        return Response(data=serializer_instance.data)
    
    def perform_create(self, serializer):

        return serializer.save(user_object=self.request.user)
    
class IncomeSummaryView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        all_incomes=Income.objects.filter(
                                            user_object=request.user,

                                            created_data__month=current_month,

                                            created_data__year=current_year
                                         )
        
        income_total=all_incomes.values("amount").aggregate(total=Sum("amount"))

        income_category=all_incomes.values("category").annotate(total=Sum("amount"))

        data={
            "total_income":income_total,
            "income_category":income_category,
        }

        return Response(data=data)

    
 

