from django.conf.urls import url
from django.urls import path,re_path
from Quiz import views

Quiz_url_patterns = [

    path('', views.Categories_list_view, name = 'quiz_category_list_all'),
    path('progress/',views.user_progress,name = 'quiz_progress'),
    re_path(r'^(?P<category_name>[\w|W-]+)/$', views.View_Quizlist_by_Category.as_view(),name = 'Quiz_category_list_matching'),
    re_path(r'^quiz/(?P<slug>[\w-]+)/$', views.Quiz_Detail_View.as_view(), name = 'quiz_detail'),
    re_path(r'^quiz/(?P<quiz_name>[\w-]+)/take/$', views.QuizAttempt.as_view(), name = 'Quiz_attempt'),
]
