from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    # post views
    # path('login/', views.user_login, name='login'),
    # logins & default dashboard
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),

    # change password urls
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # reset password urls
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView,
         name='password_reset_complete'),

    path('grantmaker/',
         views.grantmaker_view,
         name='grantmaker'),
    path('grantmakers/',
         views.grantmaker_list,
         name='grantmaker_list'),

    path('grant/',
         views.grant_view,
         name='grant'),
    path('grants/',
         views.grant_list,
         name='grant_list'),

    path('status/',
         views.status,
         name='status'),
    path('statuses/',
         views.status_list,
         name='status_list'),

    path('obligations/',
         views.obligations_list,
         name='obligations_list'),
    path('obligation/',
         views.obligation,
         name='obligation')

    # # Grantmaker URLs
    # # Get all grantmakers.
    # path('grantmakers/',
    #      views.all_grantmakers,
    #      name='grantmakers'),
    # # Delete (POST) a post by ID
    # path('grantmaker/<int:gm_id>/delete/',
    #      views.delete_grantmaker,
    #      name="delete_grantmaker"),
    # # View (GET) or edit (POST) a single grantmaker
    # path('grantmaker/',
    #      views.grantmaker,
    #      name='grantmaker')
]

