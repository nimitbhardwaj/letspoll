from django.urls import path, include, re_path

from authentication.views.user_views import UserView

urlpatterns = [
    path('create_user/', UserView.as_view({'post': 'create_user'})),
    path('make_admin/', UserView.as_view({'post': 'make_admin'})),
    path('login/', UserView.as_view({'post': 'login_user'})),
]
