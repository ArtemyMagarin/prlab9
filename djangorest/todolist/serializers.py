from rest_framework import serializers
from .models import Task, Tasklist, Tag, User


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name',)
        read_only_fields = ('id',)

class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many = True, slug_field = "id", queryset = Tag.objects.all())
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'completed', 'date_created', 'date_modified', 'due_date', 'priority', 'tags')
        read_only_fields = ('id', 'date_created', 'date_modified')




class TasklistSerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = Tasklist
        fields = ('id', 'name', 'tasks', 'owner' )
        read_only_fields = ('owner',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

