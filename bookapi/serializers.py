from rest_framework import serializers
from .models import Books
from rest_framework.serializers import ModelSerializer

class BookSerialize(serializers.Serializer):
    book_name=serializers.CharField()
    author=serializers.CharField()
    pages=serializers.CharField()
    prize=serializers.CharField()

    def create(self, validated_data):
        return Books.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.book_name=validated_data.get("book_name",instance.book_name)
        instance.author=validated_data.get("author",instance.author)
        instance.pages=validated_data.get("pages",instance.pages)
        instance.prize=validated_data.get("prize",instance.prize)
        instance.save()
        return instance

class BookModelSeril(ModelSerializer):
    class Meta:
        model=Books
        fields=["id","book_name","author","pages","prize"]

class LoginSeril(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()


