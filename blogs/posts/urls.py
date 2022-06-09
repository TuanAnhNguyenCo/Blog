from django.urls import path
from . import views
app_name = 'post'
urlpatterns = [
    path('home/',views.PTlist.as_view(),name = 'home'),
    
    path('PT/<int:pk>/',views.PTDeatil.as_view(),name = 'PT-detail'),

    # Dường dẫn tới question
    path('question/create',views.CreateQuestion,name = 'question-create'),
    path('question/search',views.SearchQuestion,name = 'question-search'),
    path('question/<int:pk>/',views.question_detail,name = 'question-detail'),
    path('question/<int:pk>/update',views.QuestionUpdateView,name = 'question-update'),
    path('question/<int:pk>/delete',views.DeleteQuestion,name = 'question-delete'),


    # Dường dẫn tới answer
    path('question/answer/<int:pk>/update',views.AnswerUpdateView,name = 'answer-update'),
    path('question/answer/<int:pk>/save',views.save_answer,name = 'answer-create'),
    path('question/answer/<int:pk>/delete',views.DeleteAnswer,name = 'answer-delete'),
]