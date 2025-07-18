from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import tempfile
from .model_tools import call_bert_model, call_rule_tool, call_gen_model
from rest_framework import generics, permissions
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer

class ModelAnalyzeView(APIView):
    """
    多模型推理接口：
    type=bert（pcap->研判结果）、type=rule（pcap->规则）、type=gen（指令->pcap文件）
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        tool_type = request.data.get('type')
        if tool_type in ['bert', 'rule']:
            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return Response({"error": "缺少pcap文件"}, status=400)
            with tempfile.NamedTemporaryFile(delete=True) as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp.flush()
                if tool_type == 'bert':
                    result = call_bert_model(tmp.name)
                else:
                    result = call_rule_tool(tmp.name)
            return Response(result, status=200)
        elif tool_type == 'gen':
            text = request.data.get('text')
            if not text:
                return Response({"error": "缺少指令文本"}, status=400)
            pcap_content = call_gen_model(text)
            response = Response(pcap_content, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="result.pcap"'
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

class ChatSessionDetailView(generics.RetrieveUpdateAPIView):
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
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(session=session)
            session.updated_at = serializer.data['created_at']
            session.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

