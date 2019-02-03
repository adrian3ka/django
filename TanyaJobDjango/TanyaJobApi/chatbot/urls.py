from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'user_answers', views.UserAnswerViewSet)
router.register(r'bot_questions', views.BotQuestionViewSet)
router.register(r'master_degrees', views.MasterDegreesViewSet)
router.register(r'master_facilities', views.MasterFacilitiesViewSet)
router.register(r'master_fields', views.MasterFieldsViewSet)
router.register(r'master_industries', views.MasterIndustriesViewSet)
router.register(r'master_job_levels', views.MasterJobLevelsViewSet)
router.register(r'master_locations', views.MasterLocationsViewSet)
router.register(r'master_majors', views.MasterMajorsViewSet)
