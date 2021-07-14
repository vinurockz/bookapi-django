from django.urls import path
from .views import book_list,book_details,AllBooks,BookDetails,BookList,BookDetailMixin,LoginPage
from django.views.generic import TemplateView
urlpatterns=[
    path('books',book_list,name='bookss'),
    path('books/<int:id>',book_details,name='detailss'),
    path('mybook',TemplateView.as_view(template_name="index.html"),name="mybooks"),
    path('cbook',AllBooks.as_view(),name='cbooks'),
    path('cbook/<int:pk>',BookDetails.as_view(),name='cdetails'),
    path('lbooks',BookList.as_view(),name='lists'),
path('lbooks/<int:pk>',BookDetailMixin.as_view(),name='lists'),

    path('logs',LoginPage.as_view(),name='loged')



]