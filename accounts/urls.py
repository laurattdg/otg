
from django.conf.urls import url, include
from accounts import views

urlpatterns = [
    url(r'^send_login_email', views.send_email_view, name="send_email"),
    url(r'^login', views.login_view, name="account_login")
]