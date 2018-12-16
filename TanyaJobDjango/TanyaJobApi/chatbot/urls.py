from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'user_answers', views.UserAnswerViewSet)
router.register(r'bot_questions', views.BotQuestionViewSet)
