from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import ClientListCreateView, ClientDetailView, ProjectCreateView, UserProjectsView, UserCreateView, CustomAuthToken,UserListView

urlpatterns = [
    path('clients/', ClientListCreateView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/<int:pk>/projects/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/', UserProjectsView.as_view(), name='user-projects'),
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('projects/', UserProjectsView.as_view(), name='user-projects'),
    path('nimapDjangoProject-token-auth/', obtain_auth_token),
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('nimapDjangoProject-token-auth/', CustomAuthToken.as_view(), name='nimapDjangoProject-token-auth'),
    path('users/list/', UserListView.as_view(), name='user-list'),
]

