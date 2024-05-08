from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('doctor-signup/',views.doctor_signup,name='doctor-signup'),
    path('patient-signup/',views.patient_signup,name='patient-signup'),
    path('doctor-login/',views.user_login,name='doctor-login'),
    path('patient-login/',views.user_login,name='patient-login'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    # path('profile/<str:pk>/',views.profile,name='profile'),
    path('pass change/',views.pass_change,name='pass_change'),
    path('pass change2/',views.pass_change2,name='pass_change2'),
    path('change data/',views.change_user_data,name='change_data'),
    path('create_blog/',views.create_post,name='create_blog'),
    path('blog_list/',views.blog_list,name='blog_list'),
    path('my_blogs/',views.my_blogs,name='my_blogs'),
    path('my_blogs/<int:pk>',views.blog_details,name='blog_details'),
    path('edit_blog/<int:pk>',views.edit_blog,name='edit_blog'),
    path('delete_blog/<int:pk>',views.delete_blog,name='delete_blog'),
]