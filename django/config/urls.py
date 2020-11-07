"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ..apiv1 import views

router = routers.SimpleRouter()
router.register('books', views.BookViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    # # 全てのアクション（一覧・詳細・登録・更新・一部更新・削除）をまとめて削除
    # path('api/', include(router.urls)),

    # # 本モデルの取得（一覧）・登録
    # path('api/books/', views.BookListAPIView.as_view()),
    # # 本モデルの取得（詳細）・更新・一部更新・削除
    # path('api/books/<pk>', views.BookRetrieveUpdateDestroyAPIView.as_view()),

    path('api/v1/', include('apiv1.urls')),
    path('api/v2/', include('apiv2.urls')),

    path('api-auth/', include('rest_framework.urls')),  # 追加
]
