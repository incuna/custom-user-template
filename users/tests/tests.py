import mock

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from incuna_test_utils.testcases.request import RequestTestCase as BaseRequestTestCase

from .factories import UserFactory
from ..models import User
from ..import views


class RequestTestCase(BaseRequestTestCase):
    user_factory = UserFactory


class RegistrationViewTest(RequestTestCase):
    def test_get(self):
        request = self.create_request(auth=False)
        response = views.RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        data = {
            'email': 'a@p.com',
            'name': 'Name',
            'password1': 'test',
            'password2': 'test',
        }
        request = self.create_request(auth=False)
        view = views.RegisterView()
        view.request = request
        form = view.form_class(data=data)

        with mock.patch('django.contrib.messages.info') as info:
            with mock.patch('users.views.login') as login:
                with mock.patch('users.views.authenticate') as authenticate:
                    authenticate.return_value = 'user'
                    response = view.form_valid(form)
                    # a message was created
                    info.assert_called_once_with(request, _('Your profile has been created.'))
                    # the user was authenticated and logged in
                    login.assert_called_once_with(request, authenticate.return_value)

        # the user was created
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.name, data['name'])
        self.assertEqual(response['location'], reverse('users:edit'))


class ProfileViewTest(RequestTestCase):
    def test_get_anonymous(self):
        request = self.create_request(auth=False)
        response = views.ProfileView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = '{0}?next=/'.format(settings.LOGIN_URL)
        self.assertEqual(response['location'], redirect_url)


class ProfileEditViewTest(RequestTestCase):
    def test_get_anonymous(self):
        request = self.create_request(auth=False)
        response = views.ProfileEdit.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = '{0}?next=/'.format(settings.LOGIN_URL)
        self.assertEqual(response['location'], redirect_url)

    def test_post_anonymous(self):
        request = self.create_request(method='post', auth=False)
        response = views.ProfileEdit.as_view()(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = '{0}?next=/'.format(settings.LOGIN_URL)
        self.assertEqual(response['location'], redirect_url)

    def test_get(self):
        request = self.create_request()
        response = views.ProfileEdit.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        data = {
            'email': 'a@p.com',
            'name': 'New name',
        }
        request = self.create_request()
        view = views.ProfileEdit()
        view.request = request
        form = view.form_class(data=data, instance=request.user)
        self.assertTrue(form.is_valid())
        with mock.patch('django.contrib.messages.info') as info:
            response = view.form_valid(form)
            # a message was created
            info.assert_called_once_with(request, _('Your profile has been updated.'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.name, data['name'])


class CreateFormTest(TestCase):
    form_class = views.RegisterView.form_class

    def test_required(self):
        form = self.form_class(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue('This field is required.' in form.errors['password1'])
        self.assertTrue('This field is required.' in form.errors['password2'])
        self.assertTrue('This field is required.' in form.errors['email'])
        self.assertTrue('This field is required.' in form.errors['name'])

    def test_password(self):
        form = self.form_class(data={'password1': '1', 'password2': 2})
        self.assertFalse(form.is_valid())
        self.assertTrue("The two password fields didn't match." in form.errors['password1'])
        self.assertTrue("The two password fields didn't match." in form.errors['password2'])

    def test_duplicate(self):
        user = UserFactory.create()
        form = self.form_class(data={'email': user.email})
        self.assertFalse(form.is_valid())
        self.assertTrue("A user with that email address already exists." in form.errors['email'])

    def test_save(self):
        data = {
            'email': 'a@p.com',
            'name': 'Test',
            'password1': 'pwd',
            'password2': 'pwd',
        }
        form = self.form_class(data=data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.name, data['name'])


class UpdateFormTest(TestCase):
    form_class = views.ProfileEdit.form_class

    def test_password_not_required(self):
        form = self.form_class(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue('password1' not in form.errors)
        self.assertTrue('password2' not in form.errors)

    def test_save(self):
        user = UserFactory.create()
        data = {
            'email': 'a@p.com',
            'name': 'Test',
            'password1': 'pwd',
            'password2': 'pwd',
        }
        form = self.form_class(data=data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.name, data['name'])
