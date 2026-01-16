from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    # ホーム画面関連のURLパターン
    path('', views.HomeScreenView.as_view(), name='home'),
    path('journal/<int:year>/<int:month>/<int:day>/init/', views.JournalInitView.as_view(), name='journal_init'),
    path('journal/<int:year>/<int:month>/<int:day>/', views.JournalDetailView.as_view(), name='journal_detail'),

    # todo関連のURLパターン
    path('journal/<int:year>/<int:month>/<int:day>/todo/create/', views.CreateTodoView.as_view(), name='create_todo'),
    path('journal/todo/update/<int:pk>/', views.UpdateTodoView.as_view(), name='update_todo'),
    path('journal/todo/delete/<int:pk>/', views.DeleteTodoView.as_view(), name='delete_todo'),
    path('journal/todo/<int:pk>/', views.DetailTodoView.as_view(), name='todo_detail'),
    
    # goal関連のURLパターン
    path('journal/<int:year>/<int:month>/<int:day>/goal/create/', views.CreateGoalView.as_view(), name='create_goal'),
    path('journal/goal/update/<int:pk>/', views.UpdateGoalView.as_view(), name='update_goal'),
    path('journal/goal/delete/<int:pk>/', views.DeleteGoalView.as_view(), name='delete_goal'),

    # schedule関連のURLパターン
    path('journal/<int:year>/<int:month>/<int:day>/schedule/create/', views.CreateScheduleView.as_view(), name='create_schedule'),
    path('journal/schedule/update/<int:pk>/', views.UpdateScheduleView.as_view(), name='update_schedule'),
    path('journal/schedule/delete/<int:pk>/', views.DeleteScheduleView.as_view(), name='delete_schedule'),

    # Reflection関連のURLパターン (URLだけ)
    # path('journal/<int:year>/<int:month>/<int:day>/reflection/create', views.CreateReflectionView.as_view(), name='create_reflection'),
    # path('journal/reflection/update/<int:pk>', views.UpdateReflectionView.as_view(), name='update_reflection'),
    # path('journal/reflection/delete/<int:pk>', views.DeleteReflectionView.as_view(), name='delete_reflection'),
]
