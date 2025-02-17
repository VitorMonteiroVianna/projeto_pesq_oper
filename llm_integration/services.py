# llm_integration/services.py
from .models import LLMInteraction
# import openai
# import anthropic


class LLMService:
    def __init__(self, model_type: str, api_key: str):
        self.model_type = model_type
        self.api_key = api_key
        
        # if model_type == 'openai':
        #     openai.api_key = api_key
        # elif model_type == 'anthropic':
        #     self.client = anthropic.Client(api_key)
        # else:
        #     raise ValueError(f"Modelo {model_type} não suportado")

    def get_openai_response(self, prompt: str):
        """Usa a API OpenAI para obter uma resposta e retorna também o número de tokens usados."""
        # response = openai.Completion.create(
        #     engine="text-davinci-003",
        #     prompt=prompt,
        #     max_tokens=150
        # )
        # tokens_input = response['usage']['prompt_tokens']
        # tokens_output = response['usage']['completion_tokens']
        # return response.choices[0].text.strip(), tokens_input, tokens_output
        return "Aqui vem o uso do GPT"

    def get_anthropic_response(self, prompt: str):
        """Usa a API Anthropic para obter uma resposta e retorna também o número de tokens usados."""
        # response = self.client.completion(
        #     prompt=prompt,
        #     model="claude-1",
        #     max_tokens=150
        # )
        # tokens_input = len(prompt.split())  # Considera o número de palavras como tokens de entrada
        # tokens_output = len(response.completion.split())  # Considera o número de palavras como tokens de saída
        # return response.completion.strip(), tokens_input, tokens_output
        return "Aqui vem o uso da anthroptic"
        
    def log_interaction(self, prompt: str, response: str, tokens_input: int, tokens_output: int, status: str = 'success'):
        """Salva a interação com o LLM no banco de dados."""
        LLMInteraction.objects.create(
            model_type=self.model_type,
            prompt=prompt,
            response=response,
            status=status,
            tokens_input=tokens_input,
            tokens_output=tokens_output
        )

    def get_response(self, prompt: str):
        """Método genérico para pegar a resposta do modelo adequado."""
        try:
            if self.model_type == 'openai':
                response, tokens_input, tokens_output = self.get_openai_response(prompt)
            elif self.model_type == 'anthropic':
                response, tokens_input, tokens_output = self.get_anthropic_response(prompt)
            else:
                raise ValueError("Modelo não suportado.")
            
            # Registrar a interação no banco de dados
            self.log_interaction(prompt, response, tokens_input, tokens_output)
            return response
        except Exception as e:
            # Em caso de erro, registrar como erro no banco
            self.log_interaction(prompt, str(e), 0, 0, status='error')
            raise e
