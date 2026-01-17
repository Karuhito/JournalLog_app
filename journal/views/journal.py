from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView
from journal.models import Journal
from journal.forms import GoalFormSet, TodoFormSet

class JournalDetailView(LoginRequiredMixin, DetailView):
    model = Journal
    template_name = 'journal/journal_detail.html'

    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']

        journal = get_object_or_404(
            Journal,
            user=self.request.user,
            date=date(year, month, day)
        )

        # 👇 ここでリダイレクト判定
        if not journal.goals.exists() and not journal.todos.exists():
            return redirect(
                'journal:journal_init',
                year=journal.date.year,
                month=journal.date.month,
                day=journal.date.day
            )

        return journal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        journal = self.object

        context['goals'] = journal.goals.all()
        context['todos'] = journal.todos.all()
        context['schedules'] = journal.schedules.order_by("start_time")

        return context
    
class JournalInitView(LoginRequiredMixin, View):
    template_name = 'journal/journal_init.html'
    login_url = 'accounts:login'

    def get(self, request, year, month, day):
        journal, _ = Journal.objects.get_or_create(
            user=request.user,
            date=date(year, month, day)
        )

        goal_formset = GoalFormSet(
            queryset=journal.goals.none(),
            prefix='goal'
        )

        todo_formset = TodoFormSet(
            queryset=journal.todos.none(),
            prefix='todo'
        )

        return render(request, self.template_name, {
            'goal_formset': goal_formset,
            'todo_formset': todo_formset,
            'journal': journal,
        })

    def post(self, request, year, month, day):
        journal = get_object_or_404(
        Journal,
        user=request.user,
        date=date(year, month, day)
        )

        goal_formset = GoalFormSet(
            request.POST,
            queryset=journal.goals.none(),
            prefix="goal"
        )
        todo_formset = TodoFormSet(
            request.POST,
            queryset=journal.todos.none(),
            prefix="todo"
        )

        if goal_formset.is_valid() and todo_formset.is_valid():
            goals = goal_formset.save(commit=False)
            todos = todo_formset.save(commit=False)

            for goal in goals:
                if goal.title:
                    goal.journal = journal
                    goal.save()

            for todo in todos:
                if todo.title:
                    todo.journal = journal
                    todo.save()

            return redirect(
                "journal:journal_detail",
                year=year,
                month=month,
                day=day
            )

        return render(request, self.template_name, {
            "goal_formset": goal_formset,
            "todo_formset": todo_formset,
            "journal": journal,
        })
