from django.urls import path

from blog.views import (CommentList, LikeList, BlogDetail, BlogList,
                        BlogViewList)

urlpatterns = [
    path('', BlogList.as_view(), name='blog-list'),
    path('<int:id>/', BlogDetail.as_view(), name='blog-detail'),
    path('<int:id>/comment/', CommentList.as_view()),
    path('<int:id>/like/', LikeList.as_view()),
    path('<int:id>/view/', BlogViewList.as_view()),
]
