from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.HomeScreenView.as_view(), name='home'),
    path('journal/<int:year>/<int:month>/<int:day>/', views.JournalInitView.as_view(), name='journal_init'),
    path('journal/<int:year>/<int:month>/<int:day>', views.JournalDetailView.as_view(), name='journal_detail'),
    # todo関連のURLパターン
    path('journal/<int:year>/<int:month>/<int:day>/todo/create/', views.CreateTodoView.as_view(), name='create_todo'),
    path('journal/todo/update/<int:pk>/', views.UpdateTodoView.as_view(), name='update_todo'),
    path('journal/todo/delete/<int:pk>/', views.DeleteTodoView.as_view(), name='delete_todo'),

    # goal関連のURLパターン
    path('journal/<int:year>/<int:month>/<int:day>/goal/create/', views.CreateGoalView.as_view(), name='create_goal'),
    path('journal/goal/update/<int:pk>/', views.UpdateGoalView.as_view(), name='update_goal'),
    path('journal/goal/delete/<int:pk>/', views.DeleteGoalView.as_view(), name='delete_goal'),
]
