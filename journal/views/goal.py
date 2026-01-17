from django.urls import reverse
from .base import BaseCreateView, BaseDeleteView, BaseUpdateView
from ..models import Goal
from ..forms import GoalFormSet, GoalForm

class CreateGoalView(BaseCreateView):
    model = Goal
    formset_class = GoalFormSet
    prefix = "goal"
    template_name = "journal/goal_create.html"

class UpdateGoalView(BaseUpdateView):
    model = Goal
    form_class = GoalForm
    template_name = "journal/goal_update.html"

class DeleteGoalView(BaseDeleteView):
    model = Goal
    object_name = "Goal"


    


