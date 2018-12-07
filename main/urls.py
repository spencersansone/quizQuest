from . import views
from django.conf.urls import url

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^landing/$', views.landing, name='landing'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^leaderboard/(?P<pk>[0-9]+)/$', views.leaderboard, name='leaderboard'),
    url(r'^profile_detail/(?P<code>[0-9]+)/$', views.profile_detail, name='profile_detail'),
    url(r'^class_detail/(?P<code>[0-9]+)/$', views.class_detail, name='class_detail'),
    url(r'^quiz/(?P<pk>[0-9]+)/$', views.quiz, name='quiz'),
    url(r'^create_quiz/$', views.create_quiz, name='create_quiz'),
    url(r'^quiz_results/(?P<pk>[0-9]+)/$', views.quiz_results , name='quiz_results'),
    # url(r'^api/getClassesForStudent/(?P<up_id>[0-9]+)/$', views.getClassesForStudent, name="getClassesForStudent"),
    url(r'^api/verify_login_API/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<password>.*)/$', views.verify_login_API, name="verify_login_API"),
    url(r'^api/get_user_info_API/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.get_user_info_API, name="get_user_info_API"),
    url(r'^api/get_class_quiz_ids_API/(?P<class_code>[0-9]+)/$', views.get_class_quiz_ids_API, name="get_class_quiz_ids_API"),
    
    # (?P<consultant_id>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})
    # IGNORE ME
    # url(r'^add_step/(?P<pk>[0-9]+)/$', views.add_step, name='add_step'),
    
    # {% url 'main:add_step' pk=certain_task.pk %}
    
    
    
    
    url(r'^add_class/$', views.add_class, name='add_class'),
]