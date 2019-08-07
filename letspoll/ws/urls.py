from django.urls import path

from ws.views.poll_views import get_poll_by_name, create_poll
from ws.views.poll_views import PollByIDView
from ws.views.question_views import QuestionView
from ws.views.option_views import OptionView


urlpatterns = [
    # Polls
    path('polls/<str:poll_id>/', PollByIDView.as_view()),
    path('polls/', create_poll),
    path('polls/name/<str:poll_name>/', get_poll_by_name),
    # Questions
    path('polls/<str:poll_id>/questions/', QuestionView.as_view()),
    path('polls/<str:poll_id>/questions/<str:question_id>/', QuestionView.as_view()),
    # Options
    path('polls/<str:poll_id>/questions/<str:question_id>/options/', OptionView.as_view()),
    path('polls/<str:poll_id>/questions/<str:question_id>/options/<str:option_id>/', OptionView.as_view()),
]
