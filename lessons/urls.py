from django.urls import path
from lessons.apps import LessonsConfig
from lessons.views import LessonListAPIView, LessonRetrieveAPIView, \
    LessonCreateAPIView, LessonUpdateAPIView, LessonDestroyAPIView

app_name = LessonsConfig.name

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/destroy/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson-delete'),

]
