from django.urls import path, include
from courses import views

app_name='courses'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('detail/<int:pk>/', views.detail_pk, name='detail_pk'),
    path('detail/<slug:slug>/', views.detail_slug, name='detail_slug'),
    path('detail/<slug:slug>/inscricao/', views.enrollment, name='enrollment')

]