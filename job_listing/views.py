from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import JobPosting,Filter
from django.db.models import F
from django.contrib.auth.decorators import login_required
from .import forms

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, password_validation, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views import generic
from .forms import UserForm
from django.template import Context
from django.template.loader import get_template

from datetime import date


def suggestion_view(request):
    form=forms.SuggestionForm()
    if request.method == 'POST':
        form=forms.SuggestionForm(request.POST)
        if form.is_valid():
            send_mail(
                'suggestion from{}'.format(form.cleaned_data['name']),
                form.cleaned_data['suggestion'],
                '{name}<{email}>'.format(**form.cleaned_data),
                ['nishitbodawala@gmail.com']
            )
            messages.add_message(request,messages.SUCCESS,'Thanks for your suggestion!')

            return HttpResponseRedirect(reverse('suggestion'))

    return render(request,'suggestion_form.html',{'form':form})


"""def job_posting(request):
    context = {"name": JobPosting.objects.all()}
    return render(request, 'posting.html', context)"""






"""if request.method == "POST":
        form=forms.JobPostingForm(request.POST)
        if form.is_valid():
            print("new job is updatet")

            return HttpResponseRedirect(reverse('fillform'))"""


def fill_form(request):
    form=forms.JobPostingForm()
    if request.method == "POST":
        form = forms.JobPostingForm(request.POST)
        if form.is_valid():
            form.save()
            print("new job is updatet")
            return HttpResponseRedirect(reverse('fillform'))
    return render(request, 'posting.html', {'name1': form})






def job_opening(request):
    form = forms.FilterForm()
    if request.method == "POST":
        form = forms.FilterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('job_opening'))
    query_set=JobPosting.objects.all()[::-1]
    context = {'name': query_set[:5],}
    return render(request, 'job_opening.html',context)


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        errors = []
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('dashboard')
            else:
                errors.append('User is inactive.')
        else:
            errors.append('Wrong password or email.')

        return render(request, self.template_name, {'errors': errors})

class LogoutView(View):
	def get(self, request):
		logout(request)

		return HttpResponseRedirect('/');


class RegisterView(View):
    form_class = UserForm
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        errors = []

        if form.is_valid():
            try:
                user = form.save(commit=False)

                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                cpassword = request.POST['password_confirmation']

                if password != cpassword:
                    errors.append("The two password fields didn't match.")
                    return render(request, self.template_name, {'form': form, 'errors': errors})

                password_validation.validate_password(password)

                user.set_password(password)
                user.save()

                user = authenticate(email=email, password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('dashboard')
            except Exception:
                errors.append('Something went wrong!')
        else:
            er = form.errors
            for i in er:
                errors.append(er[i][0])

        return render(request, self.template_name, {'form': form, 'errors': errors})


class DashboardView(LoginRequiredMixin, View):
	redirect_field_name = ''
	template_name = 'dashboard.html'

	def get(self, request):
		job_list = JobPosting.objects.all()



		return render(request, self.template_name, {'object_list':job_list })


