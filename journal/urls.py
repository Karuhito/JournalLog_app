from django.urls import path
from journal.views.home import HomeScreenView
from journal.views.journal import JournalDetailView, JournalInitView
from journal.views.goal import UpdateGoalView, DeleteGoalView, CreateGoalView 
from journal.views.todo import UpdateTodoView, DeleteTodoView, CreateTodoView
from journal.views.schedule import UpdateScheduleView, DeleteScheduleView, CreateScheduleView

app_name = 'journal'

urlpatterns = [
    # ホーム画面関連のURLパターン
    path('', HomeScreenView.as_view(), name='home'),
    path('journal/<int:year>/<int:month>/<int:day>/init/', JournalInitView.as_view(), name='journal_init'),
    path('journal/<int:year>/<int:month>/<int:day>/', JournalDetailView.as_view(), name='journal_detail'),

    # todo関連のURLパターン
    path('journal/<int:year>/<int:month>/<int:day>/todo/create/', CreateTodoView.as_view(), name='create_todo'),
    path('journal/todo/update/<int:pk>/', UpdateTodoView.as_view(), name='update_todo'),
    path('journal/todo/delete/<int:pk>/', DeleteTodoView.as_view(), name='delete_todo'),
    
    # goal関連のURLパターン
    path('journal/<int:year>/<int:month>/<int:day>/goal/create/', CreateGoalView.as_view(), name='create_goal'),
    path('journal/goal/update/<int:pk>/', UpdateGoalView.as_view(), name='update_goal'),
    path('journal/goal/delete/<int:pk>/', DeleteGoalView.as_view(), name='delete_goal'),

    # schedule関連のURLパターン
    path('journal/<int:year>/<int:month>/<int:day>/schedule/create/', CreateScheduleView.as_view(), name='create_schedule'),
    path('journal/schedule/update/<int:pk>/', UpdateScheduleView.as_view(), name='update_schedule'),
    path('journal/schedule/delete/<int:pk>/', DeleteScheduleView.as_view(), name='delete_schedule'),

    # Reflection関連のURLパターン (URLだけ)
    # path('journal/<int:year>/<int:month>/<int:day>/reflection/create', views.CreateReflectionView.as_view(), name='create_reflection'),
    # path('journal/reflection/update/<int:pk>', views.UpdateReflectionView.as_view(), name='update_reflection'),
    # path('journal/reflection/delete/<int:pk>', views.DeleteReflectionView.as_view(), name='delete_reflection'),
]
