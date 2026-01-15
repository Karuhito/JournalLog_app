from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (TemplateView, DetailView, CreateView, DeleteView, UpdateView,)
from django.views import View
from django.http import HttpResponseForbidden
from .models import Journal, Todo, Goal
from datetime import date, datetime, timedelta
import calendar
from .forms import GoalFormSet, TodoFormSet, TodoForm, GoalForm

# Home画面のView
class HomeScreenView(LoginRequiredMixin, TemplateView):
    template_name = "journal/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()
        view_mode = self.request.GET.get("view", "month")

        context["view_mode"] = view_mode
        context["today"] = today

        # ======================
        # 月表示
        # ======================
        if view_mode == "month":
            year = int(self.request.GET.get("year", today.year))
            month = int(self.request.GET.get("month", today.month))

            cal = calendar.Calendar(firstweekday=6)
            month_days = cal.monthdatescalendar(year, month)

            journals = (
                Journal.objects
                .filter(
                    user=self.request.user,
                    date__year=year,
                    date__month=month
                )
                .prefetch_related("goals", "todos")
            )

            journal_map = {
                j.date: (j.goals.exists() or j.todos.exists())
                for j in journals
            }

            cal_data = []
            for week in month_days:
                week_row = []
                for day in week:
                    has_journal = journal_map.get(day, False)
                    week_row.append({
                        "day": day,
                        "is_today": day == today,
                        "is_other_month": day.month != month,
                        "has_journal": has_journal,
                        "url": (
                            f"/journal/{day.year}/{day.month}/{day.day}/"
                            if has_journal
                            else f"/journal/{day.year}/{day.month}/{day.day}/init/"
                        ),
                    })
                cal_data.append(week_row)

            context.update({
                "year": year,
                "month": month,
                "years": [y for y in range(today.year - 2, today.year + 5)],
                "months": list(range(1, 13)),
                "cal_data": cal_data,
            })

        # ======================
        # 週表示
        # ======================
        else:
            week_start_str = self.request.GET.get("week_start")

            if week_start_str:
                week_start = date.fromisoformat(week_start_str)
            else:
                week_start = today - timedelta(days=today.weekday())

            week_end = week_start + timedelta(days=6)

            journals = (
                Journal.objects
                .filter(
                    user=self.request.user,
                    date__range=(week_start, week_end)
                )
                .prefetch_related("goals", "todos")
            )

            journal_map = {
                j.date: (j.goals.exists() or j.todos.exists())
                for j in journals
            }

            week_data = []
            for i in range(7):
                day = week_start + timedelta(days=i)
                has_journal = journal_map.get(day, False)

                week_data.append({
                    "day": day,
                    "is_today": day == today,
                    "has_journal": has_journal,
                    "url": (
                        f"/journal/{day.year}/{day.month}/{day.day}/"
                        if has_journal
                        else f"/journal/{day.year}/{day.month}/{day.day}/init/"
                    ),
                })

            context.update({
                "week_start": week_start,
                "week_end": week_end,
                "prev_week": week_start - timedelta(days=7),
                "next_week": week_start + timedelta(days=7),
                "week_data": week_data,
            })

        return context
    
# Journal関連のView
class JournalDetailView(DetailView): # その日のGoalとTodoを表示するView
    template_name = 'journal/journal_detail.html'
    model = Journal
    
    def get_queryset(self):
        return Journal.objects.filter(user=self.request.user)

    def get_object(self, queryset = None):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        return get_object_or_404(Journal, user=self.request.user, date=date(year, month, day))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        journal = self.object
        context['goals'] = journal.goals.all()
        context['todos'] = journal.todos.all()
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        journal = self.object

        goals = journal.goals.all()
        todos = journal.todos.all()

        if not goals.exists() and not todos.exists():
            return redirect(
                'journal:journal_init',
                year=journal.date.year,
                month=journal.date.month,
                day=journal.date.day
            )
        
        context = self.get_context_data()
        return self.render_to_response(context)
    
from django.views import View

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
            prefix='goal'
        )
        todo_formset = TodoFormSet(
            request.POST,
            queryset=journal.todos.none(),
            prefix='todo'
        )

        print("GOAL VALID:", goal_formset.is_valid())
        print("TODO VALID:", todo_formset.is_valid())

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

            print("=== REDIRECT ===")
            return redirect(
                'journal:journal_detail',
                year=year,
                month=month,
                day=day
            )

        return render(request, self.template_name, {
            'goal_formset': goal_formset,
            'todo_formset': todo_formset,
            'journal': journal,
        })
    
# Goal関連のView
class CreateGoalView(LoginRequiredMixin, View):
    template_name = 'journal/goal_create.html'
    login_url = 'accounts:login'

    def get(self, request, year, month, day):
        journal = get_object_or_404(
            Journal,
            user=request.user,
            date=date(year, month, day)
        )
        formset = GoalFormSet(queryset=Goal.objects.none())
        return render(request, self.template_name, {
            'journal': journal,
            'formset': formset,
        })

    def post(self, request, year, month, day):
        journal = get_object_or_404(
            Journal,
            user=request.user,
            date=date(year, month, day)
        )
        formset = GoalFormSet(request.POST, queryset=Goal.objects.none())
        if formset.is_valid():
            goals = formset.save(commit=False)
            for goal in goals:
                if not goal.title:
                    continue
                goal.journal = journal
                goal.save()
            return redirect('journal:journal_detail', year=year, month=month, day=day)

        return render(request, self.template_name, {
            'journal': journal,
            'formset': formset,
        })
        
# goalの完了・未完了切り替えView
class ToggleGoalDoneView(LoginRequiredMixin, View):
    def post(self, request, pk):
        goal = get_object_or_404(
            Goal,
            pk=pk,
            journal__user=request.user
        )
        goal.is_done = not goal.is_done
        goal.save()

        journal = goal.journal
        return redirect(
            'journal:journal_detail',
            year=journal.date.year,
            month=journal.date.month,
            day=journal.date.day
        )

# Goalの編集View
class UpdateGoalView(UpdateView):
    template_name = 'journal/goal_update.html'
    model = Goal
    form_class = GoalForm

    def get_queryset(self):
        return Goal.objects.filter(journal__user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['show_is_done'] = True
        return kwargs

    def get_success_url(self):
        journal = self.object.journal
        return reverse('journal:journal_detail', kwargs={
            'year': journal.date.year,
            'month': journal.date.month,
            'day': journal.date.day,
        })
class DeleteGoalView(DeleteView):
    template_name = 'journal/goal_delete.html'
    model = Goal

    def get_queryset(self):
        return Goal.objects.filter(journal__user=self.request.user)
    
    def get_success_url(self):
        journal = self.object.journal
        return reverse('journal:journal_detail', kwargs={
            'year': journal.date.year,
            'month': journal.date.month,
            'day': journal.date.day,
        })

# Todo関連のView
# TodoCreateView

class CreateTodoView(LoginRequiredMixin, View):
    template_name = 'journal/todo_create.html'
    login_url = 'accounts:login'

    def get(self, request, year, month, day):
        journal = get_object_or_404(
            Journal,
            user=request.user,
            date=date(year, month, day)
        )
        formset = TodoFormSet(queryset=Todo.objects.none())
        return render(request, self.template_name, {
            'journal': journal,
            'formset': formset,
        })

    def post(self, request, year, month, day):
        journal = get_object_or_404(
            Journal,
            user=request.user,
            date=date(year, month, day)
        )
        formset = TodoFormSet(request.POST, queryset=Todo.objects.none())
        if formset.is_valid():
            todos = formset.save(commit=False)
            for todo in todos:
                if not todo.title:
                    continue
                todo.journal = journal
                todo.save()
            return redirect('journal:journal_detail', year=year, month=month, day=day)

        return render(request, self.template_name, {
            'journal': journal,
            'formset': formset,
        })

# todo の完了・未完了切り替えView
class ToggleTodoDoneView(LoginRequiredMixin, View):
    def post(self, request, pk):
        todo = get_object_or_404(
            Todo,
            pk=pk,
            journal__user=request.user
        )
        todo.is_done = not todo.is_done
        todo.save()

        journal = todo.journal
        return redirect(
            'journal:journal_detail',
            year=journal.date.year,
            month=journal.date.month,
            day=journal.date.day
        )
    
# TodoDetailView
class DetailTodoView(DetailView):
    template_name = 'journal/todo_detail.html'
    model = Todo

    def get_queryset(self):
        # ログインユーザーのTodoのみ表示
        return Todo.objects.filter(journal__user=self.request.user)

# TodoUpdateView
class UpdateTodoView(UpdateView):
    template_name = 'journal/todo_update.html'
    model = Todo
    form_class = TodoForm  # ← fields を消す

    def get_queryset(self):
        return Todo.objects.filter(journal__user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['show_is_done'] = True  # ← ここが肝
        return kwargs

    def get_success_url(self):
        journal = self.object.journal
        return reverse('journal:journal_detail', kwargs={
            'year': journal.date.year,
            'month': journal.date.month,
            'day': journal.date.day
        })

# TodoDeleteView
class DeleteTodoView(DeleteView):
    template_name = 'journal/todo_delete.html'
    model = Todo

    def get_queryset(self):
        return Todo.objects.filter(journal__user=self.request.user)

    def get_success_url(self):
        journal = self.object.journal
        return reverse('journal:journal_detail', kwargs={
            'year': journal.date.year,
            'month': journal.date.month,
            'day': journal.date.day
        })