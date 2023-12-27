from django.urls import path
from review_management import views



app_name = 'review'

urlpatterns = [
    path('review_view/<int:id>', views.review_view, name = 'review_view'),
    path('add_review_view', views.add_review_view, name = 'add_review_view'),
]
