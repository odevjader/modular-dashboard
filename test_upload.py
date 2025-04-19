# test_upload.py
import requests
import os

# --- Configuração ---
# Certifique-se que este arquivo existe na mesma pasta que o script
file_to_upload = "1.pdf" # ou "1.pdf" se preferir testar com ele
api_url = "http://localhost:8000/api/gerador_quesitos/v1/gerar"
payload = {
    "beneficio": "Auxílio por Incapacidade Temporária (Auxílio-Doença)",
    "profissao": "Pedreiro",
    "modelo_nome": "<Modelo Padrão>"
}
# --- Fim Configuração ---

print(f"Tentando enviar o arquivo: {file_to_upload}")
print(f"Para a URL: {api_url}")
print(f"Com os dados: {payload}")

if not os.path.exists(file_to_upload):
    print(f"\nERRO: Arquivo '{file_to_upload}' não encontrado no diretório atual!")
else:
    try:
        # Abre o arquivo em modo binário ('rb')
        with open(file_to_upload, 'rb') as f:
            # Define o dicionário 'files' para a requisição
            # A tupla contém: nome do campo no form ('files'), tupla (nome do arquivo, file object, content_type)
            files_data = {'files': (os.path.basename(file_to_upload), f, 'application/pdf')}

            # Faz a requisição POST multipart
            response = requests.post(api_url, data=payload, files=files_data)

            # Imprime o status e a resposta
            print(f"\nStatus Code: {response.status_code}")
            print("Resposta:")
            try:
                # Tenta imprimir como JSON se possível
                print(response.json())
            except requests.exceptions.JSONDecodeError:
                # Imprime como texto se não for JSON
                print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"\nERRO na requisição: {e}")
    except Exception as e:
        print(f"\nERRO inesperado: {e}")
      