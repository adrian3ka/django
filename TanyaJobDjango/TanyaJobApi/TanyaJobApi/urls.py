"""TanyaJobApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from rest_framework import routers
#from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from chatbot import views as chatbotViews
from job import views as jobViews
from chatbot.urls import router as routerChatbot
from job.urls import router as routerJob


class DefaultRouter(routers.DefaultRouter):
    """
    Extends `DefaultRouter` class to add a method for extending url routes from another router.
    """

    def extend(self, router):
        """
        Extend the routes with url routes of the passed in router.

        Args:
             router: SimpleRouter instance containing route definitions.
        """
        self.registry.extend(router.registry)


router = DefaultRouter()
router.extend(routerChatbot)
router.extend(routerJob)

urlpatterns = [
    url(r'^api/v1/job/reccomendation/$', jobViews.GetJobRecommendation),
    url(r'^api/v1/extract/information/$', chatbotViews.ExtractInformation),
    url(r'^api/v2/extract/information/$', chatbotViews.ExtractInformationV2),
    url(r'^api/v1/ask/question/$', chatbotViews.AskQuestion),
    url(r'^api/v1/fresh_graduate/extract/$',
        chatbotViews.FreshGraduateExtraction),
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    url(r'^api/', include(router.urls)),
]
