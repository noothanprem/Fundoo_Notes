from django.urls import path,include
from django.conf.urls import url
from . import views
# from notes import views as noteviews

urlpatterns=[
    path('logout',views.Logout.as_view(), name='logout_view'),
    path('login',views.Login.as_view(), name='login_view'),
    path('register',views.Register.as_view(), name='register_view'),
    #path('noteshare',noteviews.NoteShare.as_view(), name='noteshare_view'),
    path('activate/<token>/',views.activate,name='activate'),
    path('forgotpassword',views.ForgotPassword.as_view(),name='forgotpassword_view'),
    #path('<Token>/', views.verify, name='verify'),
    path('resetpassword/<token>/', views.ResetPassword.as_view(), name='resetpassword'),
    path('sociallogin',views.sociallogin, name='sociallogin'),
    path('home',views.home, name='home'),

]