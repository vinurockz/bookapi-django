
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import Books
from .serializers import BookSerialize,BookModelSeril,LoginSeril
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from rest_framework import authentication
from rest_framework import permissions
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token




@csrf_exempt
def book_list(request):
    if request.method == "GET":
        book=Books.objects.all()
        serializer=BookSerialize(book,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method =="POST":
        data=JSONParser().parse(request)
        serializer=BookSerialize(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

@csrf_exempt
def book_details(request,*args,**kwargs):
    try:
        book=Books.objects.get(id=kwargs.get("id"))
    except:
        msg="not exisist"
        return JsonResponse(data=msg,status=400,safe=False)

    if request.method =="GET":
        seril=BookSerialize(book)
        return JsonResponse(seril.data,status=200)
    elif request.method =="PUT":
        data = JSONParser().parse(request)
        seril=BookSerialize(instance=book,data=data)
        if seril.is_valid():
            seril.save()
            return JsonResponse(seril.data,status=200)
        else:
            return JsonResponse(seril.errors,status=400)
    elif request.method == "DELETE":
        book.delete()
        msg="deleted"
        return JsonResponse(data=msg,status=200,safe=False)




class AllBooks(APIView):
    def get(self,request):
        books=Books.objects.all()
        seril=BookModelSeril(books,many=True)
        return Response(seril.data,status=200)
    def post(self,request):
        seril=BookModelSeril(data=request.data)
        if seril.is_valid():
            seril.save()
            return Response(seril.data,status=200)
        else:
            return Response(seril.errors,status=status.HTTP_400_BAD_REQUEST)

class BookDetails(APIView):
    def get_object(self,pk):
        try:
            return Books.objects.get(id=pk)
        except:
            raise Http404

    def get(self,request,*args,**kwargs):
        book=self.get_object(kwargs.get("pk"))
        seril=BookModelSeril(book)
        return Response(seril.data,status=status.HTTP_200_OK)
    def put(self,request,*args,**kwargs):
        book=self.get_object(kwargs.get("pk"))
        seril=BookModelSeril(instance=book,data=request.data)
        if seril.is_valid():
            seril.save()
            return Response(seril.data,status=status.HTTP_200_OK)
        else:
            return Response(seril.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,**kwargs):
        book = self.get_object(kwargs.get("pk"))
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookList(generics.GenericAPIView,
               mixins.ListModelMixin,
               mixins.CreateModelMixin,):

    queryset = Books.objects.all()
    serializer_class = BookModelSeril
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
class BookDetailMixin(generics.GenericAPIView,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    authentication_classes = [authentication.TokenAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Books.objects.all()
    serializer_class = BookModelSeril

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(self,request,*args,**kwargs)

class LoginPage(APIView):
    def post(self,request):
        seril=LoginSeril(data=request.data)
        if seril.is_valid():
            username=seril.validated_data.get("username")
            password=seril.validated_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                token,created=Token.objects.get_or_create(user=user)
            return Response({"token":token.key},status=status.HTTP_201_CREATED)









