from .models import TaskModel, BoardModel
from rest_framework.serializers import ModelSerializer

class TaskSerializer(ModelSerializer):
    class Meta:
        model = TaskModel
        fields = '__all__'
        read_only_fields = ['board']
    
    def create(self, validated_data):
        board_id = self.context.get('request').data.get('board')
        board = BoardModel.objects.get(id =board_id)
        return TaskModel.objects.create(board = board,**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.status = validated_data.get('status',instance.status)
        instance.description = validated_data.get('description',instance.description)
        instance.save()
        return instance

class BoardSerializer(ModelSerializer):
    class Meta:
        model = BoardModel
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context.get('request').user
        return BoardModel.objects.create(user = user,**validated_data)