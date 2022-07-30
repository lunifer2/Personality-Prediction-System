from  .import views
from django.urls import path

urlpatterns = [
    path('',views.user_login),
    path('info/',views.info),
    path('register/',views.register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('login/',views.user_login,name='login'),
    path('profile/',views.profile,name='profile'),
    path('results_id/<str:id>',views.result_id,name='result_id'),
]