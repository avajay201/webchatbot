from django.urls import path
from .views import set_tab_session


urlpatterns = [
    path("set-tab-session/", set_tab_session, name="set_tab_session"),
]
