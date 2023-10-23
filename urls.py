from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name="login"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('admin_home', views.admin_home, name='admin_home'),
    path('user_home', views.user_home, name='user_home'),

    path('register_team',views.register_team, name='register_team'),
    path('add_team',views.add_team, name='add_team'),
    path('view_team',views.view_team, name='view_team'),
    path('edit_team/<int:id>', views.edit_team, name='edit_team'),
    path('update_team/<int:id>', views.update_team, name='update_team'),
    path('delete_team/<int:id>', views.delete_team, name='delete_team'),

    path('register_match', views.register_match, name='register_match'),
    path('add_match', views.add_match, name='add_match'),
    path('view_match', views.view_match, name='view_match'),
    path('edit_match/<int:id>', views.edit_match, name='edit_match'),
    path('update_match/<int:id>', views.update_match, name='update_match'),
    path('delete_match/<int:id>', views.delete_match, name='delete_match'),

    path('tickets',views.tickets, name='tickets'),
    path('rating',views.rating, name='rating'),
    path('feedbacks',views.feedbacks, name='feedbacks'),

    path('book_ticket', views.book_ticket, name='book_ticket'),
    path('book/<int:id>', views.book, name='book'),
    path('card_verify', views.card_verify, name='card_verify'),

    path('booked_tickets',views.booked_tickets,name='booked_tickets'),

    path('user_team_view/<int:id>', views.user_team_view, name='user_team_view'),
    path('rate/<int:id>', views.rate, name='rate'),

    path('feedback', views.feedback, name='feedback'),
    path('sendfb', views.sendfb, name='sendfb'),
    path('view_fb', views.view_fb, name='view_fb'),

    path('user_view_match/<int:id>', views.user_view_match, name='user_view_match'),
    path('profile', views.profile, name='profile'),
    path('update_profile', views.update_profile, name='update_profile'),

    ]
