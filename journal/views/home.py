from django.views.generic import TemplateView
import calendar
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, timedelta
from ..models import Journal

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