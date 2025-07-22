import os
import uuid
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import tempfile
from .model_tools import call_bert_model, call_rule_tool, call_gen_model
from rest_framework import generics, permissions
from .models import ChatSession, ChatMessage, UserFile
from .serializers import ChatSessionSerializer, ChatMessageSerializer
import time
from .temp_path import TEMP_BASE_PATH
from django.core.files.base import ContentFile

def save_temp_file(file, model_type, ext='pcap'):
    temp_dir = os.path.join(TEMP_BASE_PATH, model_type)
    os.makedirs(temp_dir, exist_ok=True)
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return file_path

def clean_temp_files(days=7):
    base_temp = TEMP_BASE_PATH
    now = time.time()
    expire = days * 86400
    for model_type in ['bert', 'rule', 'gen']:
        temp_dir = os.path.join(base_temp, model_type)
        if not os.path.exists(temp_dir):
            continue
        for fname in os.listdir(temp_dir):
            fpath = os.path.join(temp_dir, fname)
            if os.path.isfile(fpath):
                if now - os.path.getmtime(fpath) > expire:
                    try:
                        os.remove(fpath)
                    except Exception:
                        pass

class ModelAnalyzeView(APIView):
    """
    多模型推理接口：
    type=bert（pcap->研判结果）、type=rule（pcap->规则）、type=gen（指令->pcap文件）
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        clean_temp_files()  # 每次推理前自动清理过期文件
        tool_type = request.data.get('type')
        if tool_type in ['bert', 'rule']:
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return Response({"error": "缺少pcap文件"}, status=400)
            # 保存到temp/<model_type>/
            temp_path = save_temp_file(uploaded_file, tool_type)
            if tool_type == 'bert':
                result = call_bert_model(temp_path)
            else:
                result = call_rule_tool(temp_path)
            return Response(result, status=200)
        elif tool_type == 'gen':
            text = request.data.get('text')
            if not text:
                return Response({"error": "缺少指令文本"}, status=400)
            temp_dir = os.path.join(TEMP_BASE_PATH, 'gen')
            os.makedirs(temp_dir, exist_ok=True)
            filename = f"{uuid.uuid4()}.pcap"
            file_path = os.path.join(temp_dir, filename)
            pcap_content = call_gen_model(text)
            with open(file_path, 'wb') as f:
                f.write(pcap_content)
            # 保存到UserFile
            user_file = UserFile.objects.create(
                user=request.user,
                file=ContentFile(pcap_content, name=filename),
                filename=filename
            )
            # 创建AI消息并关联文件
            ai_msg = ChatMessage.objects.create(
                session=ChatSession.objects.filter(user=request.user).order_by('-updated_at').first(),
                role='ai',
                content='',
                file=user_file
            )
            with open(file_path, 'rb') as f:
                response = Response(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="result.pcap"'
                return response
        else:
            return Response({"error": "type参数错误"}, status=400)

class ChatSessionListView(generics.ListCreateAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).order_by('-updated_at')
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChatSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

class ChatMessageCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, session_id):
        session = ChatSession.objects.filter(id=session_id, user=request.user).first()
        if not session:
            return Response({'detail': '会话不存在'}, status=404)
        file_obj = request.FILES.get('file')
        file_instance = None
        if file_obj:
            file_instance = UserFile.objects.create(
                user=request.user,
                file=file_obj,
                filename=file_obj.name
            )
        data = request.data.copy()
        if file_instance:
            data['file'] = file_instance.id
        serializer = ChatMessageSerializer(data=data)
        if serializer.is_valid():
            msg = serializer.save(session=session, file=file_instance if file_instance else None)
            session.updated_at = serializer.data['created_at']
            session.save()
            return Response(ChatMessageSerializer(msg, context={'request': request}).data, status=201)
        return Response(serializer.errors, status=400)

