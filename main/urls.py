from . import views
from django.conf.urls import url

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^landing/$', views.landing, name='landing'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^leaderboard/campaign/(?P<pk>[0-9]+)/$', views.leaderboard_campaign, name='leaderboard_campaign'),
    url(r'^leaderboard/competitive/(?P<pk>[0-9]+)/$', views.leaderboard_competitive, name='leaderboard_competitive'),
    url(r'^profile_detail/(?P<code>[0-9]+)/$', views.profile_detail, name='profile_detail'),
    url(r'^class_detail/(?P<code>[0-9]+)/$', views.class_detail, name='class_detail'),
    url(r'^class_grade_book/(?P<code>[0-9]+)/$', views.class_grade_book, name='class_grade_book'),
    url(r'^quiz/(?P<pk>[0-9]+)/$', views.quiz, name='quiz'),
    url(r'^accept_comp_quiz/(?P<code>[0-9]+)/(?P<pk>[0-9]+)/$', views.accept_comp_quiz, name='accept_comp_quiz'),
    url(r'^decline_comp_quiz/(?P<code>[0-9]+)/(?P<pk>[0-9]+)/$', views.decline_comp_quiz, name='decline_comp_quiz'),
    url(r'^convert_declined_comp_quiz/(?P<code>[0-9]+)/(?P<pk>[0-9]+)/$', views.convert_declined_comp_quiz, name='convert_declined_comp_quiz'),
    url(r'^discard_declined_comp_quiz/(?P<code>[0-9]+)/(?P<pk>[0-9]+)/$', views.discard_declined_comp_quiz, name='discard_declined_comp_quiz'),
    url(r'^publish_quiz/(?P<code>[0-9]+)/(?P<pk>[0-9]+)/$', views.publish_quiz, name='publish_quiz'),
    url(r'^unpublish_quiz/(?P<code>[0-9]+)/(?P<pk>[0-9]+)/$', views.unpublish_quiz, name='unpublish_quiz'),
    url(r'^comp_quiz/(?P<pk>[0-9]+)/$', views.comp_quiz, name='comp_quiz'),
    url(r'^create_quiz/$', views.create_quiz, name='create_quiz'),
    url(r'^quiz_results/(?P<pk>[0-9]+)/$', views.quiz_results , name='quiz_results'),
    url(r'^comp_quiz_results/(?P<pk>[0-9]+)/$', views.comp_quiz_results , name='comp_quiz_results'),
    url(r'^api/verify_login_API/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<password>.*)/$', views.verify_login_API, name="verify_login_API"),
    url(r'^api/get_user_info_API/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.get_user_info_API, name="get_user_info_API"),
    url(r'^api/get_student_classes_API/(?P<username>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.get_student_classes_API, name="get_student_classes_API"),
    url(r'^api/get_class_quiz_ids_API/(?P<class_code>[0-9]+)/$', views.get_class_quiz_ids_API, name="get_class_quiz_ids_API"),
    url(r'^add_class/$', views.add_class, name='add_class'),
]