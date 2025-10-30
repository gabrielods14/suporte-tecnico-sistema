"""
Script para testar o servidor Flask e a IA API
"""
import sys
import os
import time
import threading
import requests

# Adiciona o diretório raiz ao path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Importa o app Flask
from app import app

def run_server():
    """Inicia o servidor Flask"""
    print("[INFO] Iniciando servidor Flask na porta 5000...")
    app.run(debug=False, port=5000, use_reloader=False)

def test_server():
    """Testa o servidor após aguardar inicialização"""
    time.sleep(3)  # Aguarda o servidor iniciar
    
    base_url = "http://localhost:5000"
    
    print("\n" + "=" * 60)
    print("TESTE DO SERVIDOR FLASK E IA API")
    print("=" * 60)
    
    # Teste 1: Verificar se o servidor está rodando
    print("\n[TESTE 1] Verificando se o servidor está respondendo...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ Servidor respondendo (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está respondendo")
        return
    except Exception as e:
        print(f"⚠️  Erro ao conectar: {e}")
    
    # Teste 2: Testar validação do endpoint IA
    print("\n[TESTE 2] Testando validação do endpoint /api/gemini/sugerir-resposta...")
    try:
        response = requests.post(
            f"{base_url}/api/gemini/sugerir-resposta",
            json={"titulo": "Teste"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 400:
            print("✅ Validação funcionando (descrição obrigatória)")
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro no teste de validação: {e}")
    
    # Teste 3: Testar endpoint IA com dados completos
    print("\n[TESTE 3] Testando geração de sugestão pela IA...")
    test_data = {
        "titulo": "Problema com impressora",
        "descricao": "A impressora não está imprimindo documentos. Quando tento imprimir, aparece uma mensagem de erro."
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/gemini/sugerir-resposta",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "sugestao" in data:
                sugestao = data["sugestao"]
                print(f"✅ SUGESTÃO GERADA COM SUCESSO!")
                print(f"\n📝 Sugestão ({len(sugestao)} caracteres):")
                print("-" * 60)
                print(sugestao[:300] + ("..." if len(sugestao) > 300 else ""))
                print("-" * 60)
            else:
                print("⚠️  Resposta não contém 'sugestao'")
                print(f"Resposta: {data}")
        elif response.status_code == 400:
            data = response.json()
            print(f"⚠️  Erro de validação: {data.get('erro', 'Erro desconhecido')}")
            print("   (Verifique se GEMINI_API_KEY está configurada)")
        else:
            print(f"❌ Erro: Status {response.status_code}")
            try:
                print(f"Resposta: {response.json()}")
            except:
                print(f"Resposta: {response.text}")
    except requests.exceptions.Timeout:
        print("❌ Timeout - O servidor pode estar demorando muito")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS")
    print("=" * 60)
    print("\n💡 Dica: Para manter o servidor rodando, execute: python app.py")
    print("\nPressione Ctrl+C para parar o servidor...")

if __name__ == "__main__":
    # Inicia o servidor em uma thread separada
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Executa os testes
    test_server()
    
    # Mantém o script rodando
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[INFO] Encerrando servidor...")
        sys.exit(0)

