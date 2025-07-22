from rest_framework import serializers
from .models import ChatSession, ChatMessage, UserFile

class UserFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = UserFile
        fields = ['id', 'filename', 'uploaded_at', 'url']
    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url

class ChatMessageSerializer(serializers.ModelSerializer):
    file = UserFileSerializer(read_only=True)
    file_id = serializers.PrimaryKeyRelatedField(queryset=UserFile.objects.all(), source='file', write_only=True, required=False)
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'created_at', 'file', 'file_id']

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'created_at', 'updated_at', 'messages'] 