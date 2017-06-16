from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import TaskSerializer, TasklistSerializer, TagSerializer, UserSerializer
from .models import Task, Tasklist, Tag, User


class TagCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()



class TasklistCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TasklistSerializer
    queryset = Tasklist.objects.all()


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

        


class TasklistDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Tasklist.objects.all()
    serializer_class = TasklistSerializer

    def put(self, request, pk):
        try:
            tasklist = Tasklist.objects.get(pk=pk)
        except Tasklist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TasklistSerializer(tasklist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            tasklist = Tasklist.objects.get(pk=pk)
        except Tasklist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        tasklist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None:

            try:
                tasklist = Tasklist.objects.get(owner=self.request.user)
            except Tasklist.DoesNotExist:
                raise PermissionDenied()

            queryset = queryset.filter(tasklist_id = list_id)
        return queryset

    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id', None)
        try:
            tasklist = Tasklist.objects.get(pk=list_id)
        except Tasklist.DoesNotExist:
            raise PermissionDenied()
        serializer.save(tasklist=tasklist)


class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        list_id = self.kwargs.get('list_id', None)
        if list_id is not None:
            queryset = queryset.filter(tasklist_id = list_id)
        return queryset

    def put(self, request, pk, list_id):
        try:
            task = Task.objects.get(pk=pk, tasklist_id=list_id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, list_id):
        try:
            task = Task.objects.get(pk=pk, tasklist_id=list_id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserViewSet(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()



class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)




