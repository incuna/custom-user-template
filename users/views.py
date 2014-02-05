from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import UserCreateForm, UserEditForm
from .models import User


def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Follows the general idea from https://docs.djangoproject.com/en/dev/topics/class-based-views/#decorating-the-class.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


class ProfileObjectMixin(object):
    model = User

    def get_object(self):
        return self.request.user


@class_view_decorator(login_required)
class ProfileView(ProfileObjectMixin, DetailView):
    template_name = 'users/user.html'


class RegisterView(CreateView):
    form_class = UserCreateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:edit')

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)
        password = form.cleaned_data["password1"]
        username = self.object.email
        user = authenticate(username=username, password=password)
        messages.info(self.request, _('Your profile has been created.'))
        login(self.request, user)
        return response


@class_view_decorator(login_required)
class ProfileEdit(ProfileObjectMixin, UpdateView):
    form_class = UserEditForm
    success_url = reverse_lazy('users:detail')

    def form_valid(self, form):
        response = super(ProfileEdit, self).form_valid(form)
        messages.info(self.request, _('Your profile has been updated.'))
        return response

    def get_success_url(self):
        return self.request.GET.get('next', super(ProfileEdit, self).get_success_url())
