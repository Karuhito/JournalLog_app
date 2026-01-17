from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from django.views import View
from datetime import date

from ..models import Journal

class BaseCreateView(LoginRequiredMixin, View):
    """
    複数のモデルに対応できるフォームセット用 CreateView の共通基底クラス
    """
    model = None             # 対象モデル（Goal, Todo, Scheduleなど）
    formset_class = None     # 使用するフォームセット
    prefix = None            # フォームセットのprefix
    template_name = None     # テンプレート名

    login_url = "accounts:login"

    def get_journal(self, request, year, month, day):
        """
        Journalオブジェクトを取得（存在しなければ404）
        """
        return get_object_or_404(
            Journal,
            user=request.user,
            date=date(year, month, day)
        )
    
    def before_save(self, obj):
        """
        保存前の追加処理用（必要に応じてオーバーライド）
        """
        pass

    def get(self, request, year, month, day):
        journal = self.get_journal(request, year, month, day)
        formset = self.formset_class(
            queryset=self.model.objects.none(),
            prefix=self.prefix
        )
        return render(request, self.template_name, {
            "journal": journal,
            "formset": formset,
        })

    def post(self, request, year, month, day):
        journal = self.get_journal(request, year, month, day)
        formset = self.formset_class(
            request.POST,
            queryset=self.model.objects.none(),
            prefix=self.prefix
        )

        if formset.is_valid():
            instances = formset.save(commit=False)
            for obj in instances:
                if not getattr(obj, "title", None):
                    continue
                self.before_save(obj)
                obj.journal = journal
                obj.save()
            return redirect(
                "journal:journal_detail",
                year=year,
                month=month,
                day=day
            )

        return render(request, self.template_name, {
            "journal": journal,
            "formset": formset,
        })
    
class BaseUpdateView(LoginRequiredMixin, UpdateView):
    
    def get_queryset(self):
        return self.model.objects.filter(
            journal__user=self.request.user
        )
    
    def get_success_url(self):
        journal = self.object.journal
        return reverse(
            "journal:journal_detail",
            kwargs={
                'year': journal.date.year,
                'month': journal.date.month,
                'day': journal.date.day,
            }
        )




class BaseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "journal/common/confirm_delete.html"

    def get_queryset(self):
        return super().get_queryset().filter(journal__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        journal = self.object.journal

        context["object_name"] = self.object_name
        context["cancel_url"] = reverse(
            "journal:journal_detail",
            kwargs={
                "year": journal.date.year,
                "month": journal.date.month,
                "day": journal.date.day,
            }
        )
        return context
    