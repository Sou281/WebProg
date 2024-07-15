from django.urls import path
from will import views, views_api
from will.views import updateStudent

app_name = 'will'

urlpatterns =[
 # URLs untuk Student
path('', views.home, name='home'),
path('read/', views.readStudent, name='read-data-student'),
path('create/', views.createStudent, name='create-data-student'),
path('update/<str:id>', views.updateStudent, name='update-data-student'),
path('delete/<str:id>', views.deleteStudent, name='delete-data-student'),

#urls untuk Course
path('read/course', views.readCourse, name='read-data-course'),
path('create/course', views.createCourse, name='create-data-course'),
path('update/course/<str:id>', views.updateCourse, name='update-data-course'),
path('delete/course/<str:id>', views.deleteCourse, name='delete-data-course'),
#urls untuk API Course
path('api/course', views_api.apiCourse, name='api-view-data-course'),
#urls untuk Consume API
path('api/consume/course', views_api.consumeApiGet, name='api-consume-get-data'),]
path('api/course/', views_api.apiCourse, name='api-view-data-course'),