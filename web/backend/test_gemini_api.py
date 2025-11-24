"""
Script de teste para verificar se a IA API (Gemini) está funcionando corretamente.
Execute este script após iniciar o servidor Flask para testar o endpoint.
"""
import requests
import json

# URL base do servidor Flask
BASE_URL = "http://localhost:5000"

def test_gemini_endpoint():
    """Testa o endpoint /api/gemini/sugerir-resposta"""
    
    endpoint = f"{BASE_URL}/api/gemini/sugerir-resposta"
    
    # Dados de teste
    test_data = {
        "titulo": "Problema com impressora",
        "descricao": "A impressora não está imprimindo documentos. Quando tento imprimir, aparece uma mensagem de erro."
    }
    
    print("=" * 60)
    print("TESTE DA IA API (GEMINI)")s
    print("=" * 60)
    print(f"\n📡 Endpoint: {endpoint}")
    print(f"📤 Dados enviados:")
    print(json.dumps(test_data, indent=2, ensure_ascii=False))
    print("\n⏳ Enviando requisição...\n")
    
    try:
        response = requests.post(
            endpoint,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        print(f"\n📥 Response Body:")
        
        try:
            response_data = response.json()
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            
            if response.status_code == 200:
                print("\n✅ TESTE PASSOU! O endpoint está funcionando corretamente.")
                if "sugestao" in response_data:
                    print(f"\n💡 Sugestão gerada ({len(response_data['sugestao'])} caracteres)")
            else:
                print(f"\n❌ TESTE FALHOU! Status code: {response.status_code}")
                if "erro" in response_data:
                    print(f"Erro: {response_data['erro']}")
                    
        except json.JSONDecodeError:
            print(f"Resposta não é JSON válido:")
            print(response.text)
            print("\n❌ TESTE FALHOU! Resposta não é JSON válido.")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Não foi possível conectar ao servidor Flask.")
        print("   Certifique-se de que o servidor está rodando em http://localhost:5000")
        print("   Execute: python app.py")
    except requests.exceptions.Timeout:
        print("❌ ERRO: Timeout na requisição. O servidor pode estar demorando muito para responder.")
    except Exception as e:
        print(f"❌ ERRO INESPERADO: {str(e)}")

def test_endpoint_validation():
    """Testa a validação do endpoint"""
    
    endpoint = f"{BASE_URL}/api/gemini/sugerir-resposta"
    
    print("\n" + "=" * 60)
    print("TESTE DE VALIDAÇÃO")
    print("=" * 60)
    
    # Teste 1: Sem descrição
    print("\n🧪 Teste 1: Requisição sem descrição")
    try:
        response = requests.post(
            endpoint,
            json={"titulo": "Teste"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 400:
            print("✅ Validação funcionando: descrição obrigatória")
        else:
            print("❌ Validação não funcionou como esperado")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    
    # Teste 2: Sem JSON
    print("\n🧪 Teste 2: Requisição sem Content-Type JSON")
    try:
        response = requests.post(
            endpoint,
            data="not json",
            timeout=10
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        if response.status_code == 400:
            print("✅ Validação funcionando: Content-Type obrigatório")
        else:
            print("❌ Validação não funcionou como esperado")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    print("\n🚀 Iniciando testes da IA API (Gemini)...\n")
    
    # Primeiro testa a validação
    test_endpoint_validation()
    
    # Depois testa o endpoint principal
    test_gemini_endpoint()
    
    print("\n" + "=" * 60)
    print("FIM DOS TESTES")
    print("=" * 60)

