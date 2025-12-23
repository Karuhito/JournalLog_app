import django.forms as forms
from .models import Goal, Todo
from django.forms import modelformset_factory

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title',]

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'start_time', 'end_time']

GoalFormSet = modelformset_factory(
    Goal,
    form=GoalForm,
    extra=3,
    can_delete=False
)

TodoFormSet = modelformset_factory(
    Todo,
    form=TodoForm,
    extra=5,
    can_delete=False
)