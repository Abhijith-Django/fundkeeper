from django.urls import path

from api import views

from rest_framework.routers import DefaultRouter

from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()

router.register("expenses",views.ExpenseViewSet,basename="expense")

router.register("incomes",views.IncomeViewSet,basename="incomes")


urlpatterns=[
    path("register/",views.UserCreationView.as_view()),
    path("expenses/summary/",views.ExpenseSummaryView.as_view()),
    path('incomes/summary/',views.IncomeSummaryView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
]+router.urls