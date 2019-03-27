from django.urls import path
from . import views

#Note: views.index is a  function in the views module
app_name = 'polls' #Useful for namespacing in the templates!
urlpatterns = [
    #ex /polls/
    path('', views.IndexView.as_view(), name='index'),
    #ex /polls/4/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #ex /polls/4/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name = 'results'),
    #ex /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('<int:comment_id>/upvote_me/', views.upvote_me, name='upvote_me'),

    path('user_submit_question/', views.user_submit_question, name='user_submit_question')


]
 