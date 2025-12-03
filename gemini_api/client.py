import google.generativeai as genai


import os
from dotenv import load_dotenv

load_dotenv()


def get_car_ai_bio(model, brand, year):
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=gemini_api_key)

    prompt = f"""
    Gere uma biografia curta, criativa e voltada para vendas para um carro.
    Carro: {brand} {model} {year}.
    Regras:
    1. A biografia deve ter no máximo 250 caracteres.
    2. Fale sobre características específicas do modelo.
    3. **Comece a resposta DIRETAMENTE com a descrição criativa.** NÃO inclua NUNCA o nome do carro, ano ou qualquer valor monetário (R$) e nem apenas o simbolo R$ como um prefixo.
    4. **NÃO mostre a contagem de caracteres.**

    Exemplo de como **NÃO** fazer:
    R$ Kombi 1980: A lenda das estradas! Motor 1.6 refrigerado a ar...

    Exemplo de como **FAZER**:
    A lenda das estradas! Motor 1.6 refrigerado a ar, pioneira da aventura. Espaço de sobra para sua tribo e estilo retrô imbatível. Viva o clássico!
    """

    model_ai = genai.GenerativeModel('models/gemini-flash-lite-latest')

    generation_config = genai.GenerationConfig(max_output_tokens=1000)
    response = model_ai.generate_content(prompt, generation_config=generation_config)

    return response.text
