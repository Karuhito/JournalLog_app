import datetime
from django import forms
from .models import Goal, Todo, Schedule
from django.forms import modelformset_factory

# 時間の選択肢を10分刻みで生成（valueも文字列）
def time_choices(interval=15):
    choices = []
    for hour in range(0, 24):
        for minute in range(0, 60, interval):
            time_obj = datetime.time(hour, minute)
            label = f"{hour:02d}:{minute:02d}"
            choices.append((time_obj, label))
    return choices

# Goalフォーム
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title']
        labels = {
            'title': '目標タイトル',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Todoフォーム
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_done']
        labels = {
            'title': 'Todo内容',
            'is_done': '完了/未完了',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Todo内容'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        show_is_done = kwargs.pop('show_is_done', False)
        super().__init__(*args, **kwargs)
        if not show_is_done:
            self.fields.pop('is_done')


# Scheduleフォーム
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['title', 'start_time', 'end_time',]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '予定内容'
            }),
            'start_time': forms.Select(
                choices=time_choices(15),
                attrs={
                'class': "form-select time-select"
            }),
            "end_time": forms.Select(
                choices=time_choices(15),                
                attrs={  
                'class': "form-select time-select"
            }),
        }



# フォームセット
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

ScheduleFormSet = modelformset_factory(
    Schedule,
    form=ScheduleForm,
    extra=1,
    can_delete=False
    )