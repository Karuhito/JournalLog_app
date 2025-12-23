from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model, login

from .forms import SignupForm

User = get_user_model()

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('journal:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response