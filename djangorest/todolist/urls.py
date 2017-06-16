from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TasklistCreateView, TasklistDetailsView, TaskCreateView, TaskDetailsView, UserViewSet, Logout, TagCreateView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = {
    url(r'^todolists/$', TasklistCreateView.as_view(), name="lists"),
    url(r'^todolists/(?P<pk>[0-9]+)/$', TasklistDetailsView.as_view(), name="list-detail"),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/$', TaskCreateView.as_view(), name="tasks"),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', TaskDetailsView.as_view(), name="task-detail"),
    url(r'^newtag/$', TagCreateView.as_view(), name="new-tag"),
    url(r'^newuser/$', UserViewSet.as_view(), name="user"),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^logout/', Logout.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)