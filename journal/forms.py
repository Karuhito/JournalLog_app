import datetime
from django import forms
from .models import Goal, Todo
from django.forms import modelformset_factory

# 時間の選択肢を10分刻みで生成（valueも文字列）
def time_choices(interval=10):
    choices = [('', '---')]
    for hour in range(0, 24):
        for minute in range(0, 60, interval):
            label = f"{hour:02d}:{minute:02d}"
            choices.append((label, label))  # value と label を文字列に統一
    return choices

# Goalフォーム
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'is_done']
        labels = {
            'title': '目標タイトル',
            'is_done': '達成 / 未達成',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        show_is_done = kwargs.pop('show_is_done', False)
        super().__init__(*args, **kwargs)

        if not show_is_done:
            self.fields.pop('is_done')

# Todoフォーム
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

    class Meta:
        model = Todo
        fields = ['title', 'start_time', 'end_time','is_done']
        labels = {
            'title': 'Todo内容',
            'is_done': '完了/未完了',
            'start_time': '開始時刻',
            'end_time': '終了時刻',
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
        self.fields['start_time'].required = False
        self.fields['end_time'].required = False

    def clean_start_time(self):
        data = self.cleaned_data.get('start_time')
        if data in ("", None):
            return None
        return data

    def clean_end_time(self):
        data = self.cleaned_data.get('end_time')
        if data in ("", None):
            return None
        return data

# フォームセット
GoalFormSet = modelformset_factory(Goal, form=GoalForm, extra=1, can_delete=False)
TodoFormSet = modelformset_factory(Todo, form=TodoForm, extra=1, can_delete=False)