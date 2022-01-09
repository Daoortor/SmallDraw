from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('host/', views.host, name='host'),
    path('start/', views.start, name='start'),
    path('start?alert_type=<alert_type>&alert=<alert>', views.start),
    path('play/<int:game_id>/<player>/choose_cat/alert=<alert>', views.choose_cat, name='choose_cat'),
    path('play/<int:game_id>/<player>/choose_cat', views.choose_cat, name='choose_cat'),
    path('play/<int:game_id>/<player>/choose_word/cat=<category_id>', views.choose_word, name='choose_word'),
    path('play/<int:game_id>/<player>/draw', views.draw, name='draw'),
    path('play/<int:game_id>/<player>/guess', views.guess, name='guess'),
    path('play/<int:game_id>/<player>/draw_wait', views.draw_wait, name='draw_wait'),
    path('play/<int:game_id>/<player>/guess_wait', views.guess_wait, name='guess_wait'),
    path('play/<int:game_id>/<player>/check', views.check_status, name='check'),
]
