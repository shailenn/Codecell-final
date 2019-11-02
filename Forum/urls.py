from django.conf.urls import url
from django.urls import path,re_path
from Forum import views

Forum_url_patterns = [

    path('', views.forum_home, name = "forum_home"),
    path('Ask/',views.Ask_question.as_view(), name = "ask_question"),
    path('<int:pk>/', views.Add_answer.as_view(), name="answer_list"),
    #path('<int:pk>/answer/', views.Add_answer.as_view(), name="add_answer"),
]
