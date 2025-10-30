"""
Script para ajudar a configurar a chave de API do Gemini
"""
import os

def configurar_chave_api():
    """Configura a chave de API no arquivo .env"""
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    print("=" * 70)
    print("CONFIGURACAO DA CHAVE DE API DO GEMINI")
    print("=" * 70)
    print()
    
    # Verifica se o arquivo .env existe
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Verifica se já tem a chave
        if 'GEMINI_API_KEY=' in content:
            print("✅ Arquivo .env encontrado!")
            print()
            
            # Extrai a chave atual
            lines = content.split('\n')
            for line in lines:
                if line.startswith('GEMINI_API_KEY='):
                    chave_atual = line.replace('GEMINI_API_KEY=', '').strip()
                    if chave_atual and chave_atual != 'sua_chave_api_aqui':
                        print(f"Chave atual configurada: {chave_atual[:10]}...")
                        print()
                        resposta = input("Deseja alterar a chave? (s/n): ").lower()
                        if resposta != 's':
                            print("✅ Mantendo chave atual.")
                            return
                    break
    else:
        print("⚠️  Arquivo .env não encontrado. Será criado agora.")
        print()
    
    print("Como obter sua chave de API:")
    print("1. Acesse: https://makersuite.google.com/app/apikey")
    print("2. Faça login com sua conta Google")
    print("3. Clique em 'Create API Key' (Criar Chave de API)")
    print("4. Copie a chave gerada")
    print()
    
    chave = input("Cole sua chave de API do Gemini aqui: ").strip()
    
    if not chave:
        print("❌ Nenhuma chave foi fornecida. Configuração cancelada.")
        return
    
    # Remove espaços e caracteres especiais que possam ter sido copiados
    chave = chave.replace(' ', '').replace('"', '').replace("'", '')
    
    # Escreve no arquivo .env
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(f"# Configuração da API do Google Gemini\n")
        f.write(f"# Obtenha sua chave em: https://makersuite.google.com/app/apikey\n")
        f.write(f"GEMINI_API_KEY={chave}\n")
    
    print()
    print("=" * 70)
    print("✅ CHAVE DE API CONFIGURADA COM SUCESSO!")
    print("=" * 70)
    print()
    print("📝 Arquivo salvo em:", env_path)
    print()
    print("⚠️  IMPORTANTE: Reinicie o servidor Flask para que as mudanças tenham efeito!")
    print("    Pressione Ctrl+C no terminal do Flask e execute novamente:")
    print("    python app.py")
    print()

if __name__ == "__main__":
    try:
        configurar_chave_api()
    except KeyboardInterrupt:
        print("\n\nConfiguração cancelada.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

