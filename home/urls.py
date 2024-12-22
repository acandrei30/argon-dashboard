from django.urls import path
from home import views
from django.contrib.auth import views as auth_views


urlpatterns = [
  
  # Pages
  path('pages/pricing/', views.pricing, name='pricing'),
  path('pages/widgets/', views.widgets, name='widgets'),
  path('pages/charts/', views.charts, name='charts'),
  path('pages/calendar/', views.calendar, name='calendar'),

  # Dashboard
  path('', views.dashboard, name='dashboard'),
  path('dashboard/alternative/', views.alternative, name='alternative'),

  # Components
  path('components/buttons/', views.buttons, name='buttons'),
  path('components/cards/', views.cards, name='cards'),
  path('components/grid/', views.grid, name='grid'),
  path('components/notifications/', views.notifications, name='notifications'),
  path('components/icons/', views.icons, name='icons'),
  path('components/typography/', views.typography, name='typography'),
  path('components/components/', views.components, name='components'),

  # Forms
  path('forms/elements/', views.form_elements, name="form_elements"),
  path('forms/components/', views.form_components, name="form_components"),
  path('forms/validation/', views.form_validation, name="form_validation"),

  # Tables
  path('tables/', views.tables, name="tables"),
  path('tables/sortable', views.sortable_tables, name="sortable_tables"),
  path('tables/datatables', views.datatables, name="datatables"),

  # Maps
  path('maps/google/', views.google_maps, name="google_maps"),
  path('maps/vector/', views.vector_maps, name="vector_maps"),

  # Authentication
  path('accounts/login/', views.UserLoginView.as_view(), name="login"),
  path('accounts/register/', views.register, name="register"),
  path('accounts/logout/', views.logout_view, name="logout"),

  path('accounts/change-password/', views.UserChangePasswordView.as_view(), name="change_password"),
  path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
    template_name="accounts/password-change-done.html"
  ), name="password_change_done"),

  path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
  path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
      template_name='accounts/password-reset-done.html'
  ), name='password_reset_done'),
  path('accounts/password-reset-confirm/<uidb64>/<token>/', 
      views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
      template_name='accounts/password-reset-complete.html'
  ), name='password_reset_complete'),
  path('accounts/lock/', views.lock, name="lock"),

  # Examples
  path('examples/timeline/', views.timeline, name="timeline"),
  path('examples/profile/', views.profile, name="profile"),
  path('examples/rtl/', views.rtl, name="rtl"),

  # Extra
  path('components/', views.components_extra, name="components"),
]
