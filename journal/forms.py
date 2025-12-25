import datetime
import django.forms as forms
from .models import Goal, Todo
from django.forms import modelformset_factory

def time_choices(interval=10):
    choices = [('', '---')]
    for hour in range(0, 24):
        for minute in range(0, 60, interval):
            time = datetime.time(hour, minute)
            label = f"{hour:02d}:{minute:02d}"
            choices.append((time, label))
    return choices

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title','is_done',]
        labels = {
            'title': '目標タイトル',
            'detail': '詳細',
            'is_done': '達成/未達成',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TodoForm(forms.ModelForm):
    start_time = forms.ChoiceField(
        label='開始時刻',
        choices=time_choices(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    end_time = forms.ChoiceField(
        label='終了時刻',
        choices=time_choices(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


    class Meta:
        model = Todo
        fields = ['title', 'start_time', 'end_time','is_done',]
        labels = {
            'title': 'Todo内容',
            'is_done': '完了/未完了',
            'start_time': '開始時刻',
            'end_time': '終了時刻',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Todo内容'
            }),
        }

GoalFormSet = modelformset_factory(
    Goal,
    form=GoalForm,
    extra=1,
    can_delete=False
)

TodoFormSet = modelformset_factory(
    Todo,
    form=TodoForm,
    extra=1,
    can_delete=False
)