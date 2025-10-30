"""
Script final para testar a IA API
"""
import sys
import os
import requests
import time

# Adiciona o diretório raiz ao path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

BASE_URL = "http://localhost:5000"

def test_gemini_api():
    """Testa o endpoint da IA API"""
    
    print("=" * 70)
    print("TESTE FINAL DA IA API (GEMINI)")
    print("=" * 70)
    
    # Aguarda o servidor estar pronto
    print("\n[INFO] Aguardando servidor...")
    max_attempts = 10
    for i in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/", timeout=2)
            print(f"[INFO] Servidor respondendo na tentativa {i+1}")
            break
        except requests.exceptions.ConnectionError:
            if i < max_attempts - 1:
                time.sleep(1)
            else:
                print("❌ ERRO: Servidor não está respondendo")
                print("   Por favor, inicie o servidor com: python app.py")
                return
        except Exception as e:
            print(f"⚠️  Erro: {e}")
    
    # Teste 1: Validação - sem descrição
    print("\n" + "-" * 70)
    print("[TESTE 1] Validação - Requisição sem descrição")
    print("-" * 70)
    try:
        response = requests.post(
            f"{BASE_URL}/api/gemini/sugerir-resposta",
            json={"titulo": "Teste"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"✅ Validação OK: {data.get('erro', 'Erro não especificado')}")
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
            print(f"Resposta: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 2: Geração de sugestão completa
    print("\n" + "-" * 70)
    print("[TESTE 2] Geração de Sugestão pela IA")
    print("-" * 70)
    
    test_data = {
        "titulo": "Problema com impressora",
        "descricao": "A impressora não está imprimindo documentos. Quando tento imprimir, aparece uma mensagem de erro dizendo que há um problema de comunicação."
    }
    
    print(f"\n📤 Enviando dados:")
    print(f"   Título: {test_data['titulo']}")
    print(f"   Descrição: {test_data['descricao'][:80]}...")
    print(f"\n⏳ Gerando sugestão... (pode levar alguns segundos)\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/gemini/sugerir-resposta",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # Timeout maior para IA
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "sugestao" in data:
                sugestao = data["sugestao"]
                print("\n" + "=" * 70)
                print("✅ SUCESSO! SUGESTÃO GERADA PELA IA")
                print("=" * 70)
                print(f"\n📝 Sugestão ({len(sugestao)} caracteres):")
                print("-" * 70)
                print(sugestao)
                print("-" * 70)
                print("\n✅ TESTE COMPLETO - IA API ESTÁ FUNCIONANDO!")
            else:
                print("⚠️  Resposta não contém 'sugestao'")
                print(f"Resposta completa: {data}")
        elif response.status_code == 400:
            data = response.json()
            erro = data.get('erro', 'Erro desconhecido')
            print(f"\n❌ ERRO DE VALIDAÇÃO/CONFIGURAÇÃO: {erro}")
            if 'GEMINI_API_KEY' in erro:
                print("\n💡 DICA: Configure a variável GEMINI_API_KEY no arquivo .env")
                print("   Exemplo: GEMINI_API_KEY=sua_chave_aqui")
        elif response.status_code == 500:
            data = response.json()
            erro = data.get('erro', 'Erro interno do servidor')
            print(f"\n❌ ERRO INTERNO: {erro}")
        else:
            print(f"\n⚠️  Status não esperado: {response.status_code}")
            try:
                print(f"Resposta: {response.json()}")
            except:
                print(f"Resposta: {response.text[:500]}")
                
    except requests.exceptions.Timeout:
        print("\n❌ ERRO: Timeout - A requisição demorou muito")
        print("   Isso pode indicar que a API do Gemini está demorando para responder")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar ao servidor")
        print("   Certifique-se de que o servidor Flask está rodando")
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("TESTE FINALIZADO")
    print("=" * 70)

if __name__ == "__main__":
    test_gemini_api()

