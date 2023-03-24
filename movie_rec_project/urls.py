from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users import views as users_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('movie.urls')),
    path('admin/', admin.site.urls),
    path('registration/', users_views.registration_user, name="registration"),
    path('profile/', users_views.profile, name="profile"),
    path('signin/', auth_views.LoginView.as_view(template_name='users/signin.html'), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('genre/', include('genre.urls')),
    path('delete_user/', users_views.delete_user, name='delete_user'),
    # path('delete_user/', users_views.DeleteUser.as_view(), name='delete_user')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
