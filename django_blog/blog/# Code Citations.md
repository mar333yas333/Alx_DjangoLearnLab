# Code Citations

## License: Apache-2.0
https://github.com/yanjl/blog_auth/blob/00ea53eefca37fe34970c0dc661859ecec16e3a5/blog/urls.py

```
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'
```


## License: unknown
https://github.com/mukheshinturi/ase_project/blob/99d4dedd9cba9492abfbb17fb28fffc2c841c656/users/urls.py

```
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'
```


## License: unknown
https://github.com/cristomathew/django_trials/blob/6eb0b429a5bca589bbf1ee3cf9922cdf6466a5c1/users/urls.py

```
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'
```


## License: unknown
https://github.com/lokeshsharma596/Django_Projects/blob/25823b03a21bcf147bac05712cb17f0746b37981/lokesh_blog/blog/urls.py

```
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'
```


## License: unknown
https://github.com/100sarthak100/devblog/blob/64aa8469ed66babe6fb5e1610d5f99e29a20129e/djangoProj/urls.py

```
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'
```

