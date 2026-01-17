from django.urls import reverse
from .base import BaseCreateView, BaseDeleteView, BaseUpdateView
from ..models import Todo
from ..forms import TodoForm, TodoFormSet

class CreateTodoView(BaseCreateView):
    model = Todo
    formset_class = TodoFormSet
    prefix = "todo"
    template_name = "journal/todo_create.html"


class UpdateTodoView(BaseUpdateView):
    model = Todo
    form_class = TodoForm
    template_name = "journal/todo_update.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["show_is_done"] = True
        return kwargs

class DeleteTodoView(BaseDeleteView):
    model = Todo
    object_name = "Todo"
