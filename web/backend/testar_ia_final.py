"""Teste final da IA API com a chave válida"""
import requests
import json
import time

print("=" * 70)
print("TESTE FINAL DA IA API COM CHAVE VALIDA")
print("=" * 70)
print()

# Aguarda servidor estar pronto
print("Aguardando servidor Flask...")
time.sleep(3)

test_data = {
    "titulo": "Tela azul no computador",
    "descricao": "O computador está dando tela azul quando liga. Aparece um erro na tela azul antes de desligar."
}

print(f"Enviando requisição...")
print(f"Título: {test_data['titulo']}")
print(f"Descrição: {test_data['descricao']}")
print()

try:
    response = requests.post(
        "http://localhost:5000/api/gemini/sugerir-resposta",
        json=test_data,
        headers={"Content-Type": "application/json"},
        timeout=60
    )
    
    print(f"Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        if "sugestao" in data:
            sugestao = data["sugestao"]
            print("=" * 70)
            print("✅ SUCESSO! SUGESTÃO GERADA!")
            print("=" * 70)
            print()
            print(f"Sugestão ({len(sugestao)} caracteres):")
            print("-" * 70)
            print(sugestao)
            print("-" * 70)
            print()
            print("✅ TESTE PASSOU! A IA API ESTÁ FUNCIONANDO!")
        else:
            print("⚠️  Resposta não contém 'sugestao'")
            print(f"Resposta: {data}")
    else:
        data = response.json()
        print("❌ ERRO:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
except requests.exceptions.ConnectionError:
    print("❌ ERRO: Servidor não está respondendo")
    print("   Certifique-se de que o servidor Flask está rodando")
except requests.exceptions.Timeout:
    print("❌ ERRO: Timeout - A requisição demorou muito")
except Exception as e:
    print(f"❌ ERRO INESPERADO: {e}")
    import traceback
    traceback.print_exc()

