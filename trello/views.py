from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from .models import TaskModel,BoardModel
from .serializers import TaskSerializer,BoardSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from django.contrib.auth.models import User
from django.http import Http404
# Create your views here.

# Define reusable security scheme for Bearer token
bearer_token_scheme = [{"Bearer": []}]

class TaskModelView (APIView):
    @swagger_auto_schema(
        operation_description="Get all tasks for the current authenticated user.",
        responses={200: "List of tasks"},
        security=bearer_token_scheme,
        request_body=None
    )
    # Gets all tasks associated with a user
    def get(self,request):
        """
        Get all tasks for the current authenticated user.
        {
        Body is empty. 
        Ensure token is passed in bearers. 
        }
        """
        user = request.user
        tasks = TaskModel.objects.filter(board__user=user)
        serializer = TaskSerializer(tasks,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        security=bearer_token_scheme,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'description', 'status', 'board'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Task title'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Task description'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Task status'),
                'board': openapi.Schema(type=openapi.TYPE_INTEGER, description='Board ID'),
            },
            example={
                "title": "Clean room3",
                "description": "Need to clean room",
                "status": "Todo",
                "board": 3
            }
        )
    )
    # Creates tasks associated with a board. Board id is passed in request body
    def post (self,request):
        """
        Create a new task. You must include a valid `board` ID in the request body.
        {
        "title": "Clean room3",
        "description": "Need to clean room",
        "status": "Todo",
        "board": 3
        }
        """

        serializer = TaskSerializer(data = request.data, context = {"request": request} )
        if serializer.is_valid():
            serializer.save()
            return Response('Request received successfully', status=status.HTTP_201_CREATED)
        else:
            return Response(f'{serializer.errors}',status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        security=bearer_token_scheme,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Task ID'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Task title', default=None),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Task description', default=None),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Task status', default=None),
                'board': openapi.Schema(type=openapi.TYPE_INTEGER, description='Board ID', default=None),
            },
            example={
                "id": 3,
                "title": "Clean room3",
                "description": "Need to clean room",
                "status": "Todo",
                "board": 3
            }
        )
    )
    # Edits specific task. Id is sent in request body. 
    def put(self,request):
        """
        Update a task. Provide the `id` of the task and the fields to update.
        {
        "id": 3,
        "title": "Clean room3",
        "description": "Need to clean room",
        "status": "Todo",
        "board": 3
        },
        """
        try:
            id = request.data.get('id')
            task = TaskModel.objects.get(id = id)
        except TaskModel.DoesNotExist:
            raise Http404("Does not Exist")
        serializer = TaskSerializer(task,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Updated Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response(f"${serializer.errors}", status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        security=bearer_token_scheme,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Task ID'),
            },
            example={
                "id": 3
            }
        )
    )
    def delete(self,request):
        """
        Delete a task. Provide the `id` of the task to delete in the request body.
        {
        "id": 3,
        },

        """
        try:
            id = request.data.get('id')
            task = TaskModel.objects.get(id = id)
        except TaskModel.DoesNotExist:
            raise Http404("Does not Exist")
        task.delete()
        return Response({"message": "Deleted succesfully"},status=status.HTTP_204_NO_CONTENT)

class BoardView(APIView):
    """
        Retrieve all boards belonging to the authenticated user.
        Request body is empty ensure logged in and token passed in bearer section
    """

    @swagger_auto_schema(
        operation_description="Retrieve all boards belonging to the authenticated user.",
        responses={200: "List of boards"},
        security=bearer_token_scheme,
        request_body=None
    )
    # Returns All Boards associated with a User
    def get(self,request):
        user = request.user
        boards = user.boards.all()
        serializer = BoardSerializer(boards,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        security=bearer_token_scheme,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'description'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Board title'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Board description'),
            },
            example={
                "title": "Board3",
                "description": "Need to clean room2"
            }
        )
    )
    # Creates a Board. User is passed through Request
    def post(self,request):
        """
        Create a new board. The board is automatically associated with the authenticated user.
        Example JSON
        {
        "title": "Board3",
        "description": "Need to clean room2"
        }
        """
        
        serializer = BoardSerializer(data= request.data,context = {"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response("Board created successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        security=bearer_token_scheme,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Board ID'),
            },
            example={
                "id": 3
            }
        )
    )
    # Deletes a specific board. Id is passed in request body
    def delete(self,request):
        """
        Delete a board. Provide the `id` of the board in the request body.
          {
        "id": 3,
        },

        """
        
        try:
            id = request.data.get('id')
            Board = BoardModel.objects.get(id = id)
        except BoardModel.DoesNotExist:
            raise Http404("Does not Exist")
        Board.delete()
        return Response({"message": "Deleted succesfully"},status=status.HTTP_204_NO_CONTENT)

class SpecificBoardView(APIView):
    """
        Retrieve all tasks linked to a specific board.
        Id is passed in url
    """
    @swagger_auto_schema(
        operation_description="Retrieve all tasks linked to a specific board.",
        responses={200: "List of tasks"},
        security=bearer_token_scheme,
        request_body=None
    )
    # Returns Tasks Associated with specific boards. 
    def get(self,request,id):
        try:
            board = BoardModel.objects.get(id = id)
        except BoardModel.DoesNotExist:
            raise Http404("Does not Exist")
        tasks = board.tasks.all()
        serializer = TaskSerializer(tasks,many = True)
        return Response (serializer.data,status=status.HTTP_200_OK)











