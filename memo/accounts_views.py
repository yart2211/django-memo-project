from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView
from django.views.generic import RedirectView


class RegisterFormView(generic.FormView):
    form_class = UserCreationForm
    # Текущая ссылка /memo/login/
    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/memo/login/?next=/memo/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration/registration.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginView(FormView):
    success_url = '/memo/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "registration/login.html"

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
             redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    url = '/memo/login/'
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

