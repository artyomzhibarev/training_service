from django.urls import path, re_path
from training import views

app_name = 'training'

urlpatterns = [
    path('topics/', views.TopicList.as_view(), name='topic-list'),
    path('topics/<int:pk>/', views.TopicDetail.as_view(), name='topic-detail'),
    path('my-tests/', views.PersonalCustomerTests.as_view()),
    path('tests/', views.TrainingTestList.as_view(), name='trainingtest-list'),
    re_path(r'^tests/(?P<slug>[\w\-]+)/$', views.TrainingTestDetail.as_view(), name='trainingtest-detail'),
    re_path(r'^tests/(?P<slug>[\w\-]+)/submit/$', views.SubmitTest.as_view()),
    re_path(r'^tests/(?P<slug>[\w\-]+)/save-answer/$', views.SaveCustomerAnswers.as_view()),
]
