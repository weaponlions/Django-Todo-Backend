from rest_framework import serializers
from .models import Notes
from django.contrib.auth.models import User

class SerializerNote(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="SerializerNote.user")
    class Meta:
        model = Notes
        fields = ['title', 'description', 'tag', 'created_time', 'modify_time', 'slug', 'id', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(SerializerNote, self).create(validated_data)


class SignUpSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField()
    last_name =  serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    password =  serializers.CharField()

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password')

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
