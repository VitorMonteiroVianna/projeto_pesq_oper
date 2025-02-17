from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import OptimizationProcess
from .serializers import OptimizationProcessSerializer
from llm_integration.services import LLMService


class OptimizationProcessAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # Autenticação por JWT
    permission_classes = [IsAuthenticated]  #

    def post(self, request):
        """Cria um novo processo de otimização e chama o LLMService"""
        serializer = OptimizationProcessSerializer(data=request.data)

        if serializer.is_valid():
            # Cria o objeto mas ainda não salva
            optimization_process = serializer.save(user=request.user)

            # Morreu aq TODO: corrigir
            llm_service = LLMService()
            response_data = llm_service.get_response(optimization_process.input_data)

            # Atualiza o processo com os resultados
            optimization_process.result_data = response_data
            optimization_process.status = 'completed'
            optimization_process.save()

            return Response({'id': optimization_process.id}, status=status.HTTP_201_CREATED)

        return Response({"error": "Erro na validação", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
    

    def get(self, request, process_id):
        """Obtém detalhes de um processo específico"""
        optimization_process = get_object_or_404(OptimizationProcess, id=process_id, user=request.user)
        serializer = OptimizationProcessSerializer(optimization_process)
        return Response(serializer.data, status=status.HTTP_200_OK)
