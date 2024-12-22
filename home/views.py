from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from home.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

def index(request):
  context = {
    'segment': 'index'
  }
  return render(request, 'pages/index.html', context)

def pricing(request):
  return render(request, 'pages/examples/pricing.html')

# Dashboard
def dashboard(request):
  context = {
    'parent': 'dashboard',
    'segment': 'dashboard'
  }
  return render(request, 'pages/dashboards/dashboard.html', context)

@login_required(login_url='/accounts/login/')
def alternative(request):
  context = {
    'parent': 'dashboard',
    'segment': 'alternative'
  }
  return render(request, 'pages/dashboards/alternative.html', context)

# Components
@login_required(login_url='/accounts/login/')
def buttons(request):
  context = {
    'parent': 'components',
    'segment': 'buttons'
  }
  return render(request, 'pages/components/buttons.html', context)

@login_required(login_url='/accounts/login/')
def cards(request):
  context = {
    'parent': 'components',
    'segment': 'cards'
  }
  return render(request, 'pages/components/cards.html', context)

@login_required(login_url='/accounts/login/')
def grid(request):
  context = {
    'parent': 'components',
    'segment': 'grid'
  }
  return render(request, 'pages/components/grid.html', context)

@login_required(login_url='/accounts/login/')
def notifications(request):
  context = {
    'parent': 'components',
    'segment': 'notifications'
  }
  return render(request, 'pages/components/notifications.html', context)

@login_required(login_url='/accounts/login/')
def icons(request):
  context = {
    'parent': 'components',
    'segment': 'icons'
  }
  return render(request, 'pages/components/icons.html', context)

@login_required(login_url='/accounts/login/')
def typography(request):
  context = {
    'parent': 'components',
    'segment': 'typography'
  }
  return render(request, 'pages/components/typography.html', context)

@login_required(login_url='/accounts/login/')
def components(request):
  context = {
    'parent': 'components',
    'segment': 'components'
  }
  return render(request, 'pages/components/components.html', context)

# Forms
@login_required(login_url='/accounts/login/')
def form_elements(request):
  context = {
    'parent': 'forms',
    'segment': 'elements'
  }
  return render(request, 'pages/forms/elements.html', context)

@login_required(login_url='/accounts/login/')
def form_components(request):
  context = {
    'parent': 'forms',
    'segment': 'form_components'
  }
  return render(request, 'pages/forms/components.html', context)

@login_required(login_url='/accounts/login/')
def form_validation(request):
  context = {
    'parent': 'forms',
    'segment': 'form_validation'
  }
  return render(request, 'pages/forms/validation.html', context)

# Tables
@login_required(login_url='/accounts/login/')
def tables(request):
  context = {
    'parent': 'tables',
    'segment': 'tables'
  }
  return render(request, 'pages/tables/tables.html', context)

@login_required(login_url='/accounts/login/')
def sortable_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'sortable'
  }
  return render(request, 'pages/tables/sortable.html', context)

@login_required(login_url='/accounts/login/')
def datatables(request):
  context = {
    'parent': 'tables',
    'segment': 'datatables'
  }
  return render(request, 'pages/tables/datatables.html', context)

# Maps
@login_required(login_url='/accounts/login/')
def google_maps(request):
  context = {
    'parent': 'maps',
    'segment': 'google_maps'
  }
  return render(request, 'pages/maps/google.html', context)

@login_required(login_url='/accounts/login/')
def vector_maps(request):
  context = {
    'parent': 'maps',
    'segment': 'vector_maps'
  }
  return render(request, 'pages/maps/vector.html', context)

# Pages
@login_required(login_url='/accounts/login/')
def widgets(request):
  context = {
    'segment': 'widgets'
  }
  return render(request, 'pages/widgets.html', context)

@login_required(login_url='/accounts/login/')
def charts(request):
  context = {
    'segment': 'charts'
  }
  return render(request, 'pages/charts.html', context)

@login_required(login_url='/accounts/login/')
def calendar(request):
  context = {
    'segment': 'calendar'
  }
  return render(request, 'pages/calendar.html', context)

# Examples
@login_required(login_url='/accounts/login/')
def timeline(request):
  context = {
    'parent': 'examples',
    'segment': 'timeline'
  }
  return render(request, 'pages/examples/timeline.html', context)

@login_required(login_url='/accounts/login/')
def profile(request):
  context = {
    'parent': 'examples',
    'segment': 'profile'
  }
  return render(request, 'pages/examples/profile.html', context)

@login_required(login_url='/accounts/login/')
def rtl(request):
  context = {
    'parent': 'examples',
    'segment': 'rtl'
  }
  return render(request, 'pages/examples/rtl-support.html', context)


# Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print("Account created successfully")
      return redirect('/accounts/login/')
    else:
      print("Registration failed")
  else:
    form = RegistrationForm()
  
  context = {
    'form': form
  }
  return render(request, 'accounts/register.html', context)

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password-reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password-reset-confirm.html'
  form_class = UserSetPasswordForm

class UserChangePasswordView(PasswordChangeView):
  template_name = 'accounts/password-change.html'
  form_class = UserPasswordChangeForm

@login_required(login_url='/accounts/login/')
def lock(request):
  return render(request, 'accounts/lock.html')


# Extra
@login_required(login_url='/accounts/login/')
def components_extra(request):
  return render(request, 'pages/components.html')


def handler404(request, exception=None):
  return render(request, 'accounts/error-404.html')

def handler403(request, exception=None):
  return render(request, 'accounts/error-403.html')

def handler500(request, exception=None):
  return render(request, 'accounts/error-500.html')


# i18n
def i18n_view(request):
  context = {
    'parent': 'apps',
    'segment': 'i18n'
  }
  return render(request, 'pages/navigation/i18n.html', context)