from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import OptimizationProcess
from .serializers import OptimizationProcessSerializer
from llm_integration.services import LLMService


class OptimizationProcessAPIView(APIView):
    # Configura para que seja necessario estar logado
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        """Cria um novo processo de otimização e chama o LLMService"""
        serializer = OptimizationProcessSerializer(data=request.data)

        if serializer.is_valid():
            optimization_process = serializer.save(user=request.user)

            llm_service = LLMService("openai")
            response_data = llm_service.get_response(optimization_process.input_data)

            optimization_process.result_data = response_data
            optimization_process.status = 'completed'
            optimization_process.save()

            return Response({'id': optimization_process.id}, status=status.HTTP_201_CREATED)

        return Response({"error": "Erro na validação", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
    

    def get(self, request, process_id=None):
        """Obtém um processo específico ou lista todos os processos do usuário com paginação"""
        
        # Se o id for especificado retorna somente as infos dele
        if process_id:  
            optimization_process = get_object_or_404(OptimizationProcess, id=process_id, user=request.user)
            serializer = OptimizationProcessSerializer(optimization_process)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Retorna todos os processos do usuário com paginação
        processes = OptimizationProcess.objects.filter(user=request.user).order_by('-created_at')
        paginator = PageNumberPagination()
        paginated_processes = paginator.paginate_queryset(processes, request)
        serializer = OptimizationProcessSerializer(paginated_processes, many=True)

        return paginator.get_paginated_response(serializer.data)

