#!/usr/bin/env python3
"""
Script de inicialização do MiteScan Flask API
"""

import os
import sys
from app import create_app

def main():
    """Função principal para inicializar a aplicação"""
    
    # Verificar se o arquivo .env existe
    if not os.path.exists('.env'):
        print("⚠️ Arquivo .env não encontrado!")
        print("📋 Crie um arquivo .env baseado no .env.example")
        print("💡 Exemplo: cp .env.example .env")
        return
    
    # Criar a aplicação Flask
    app = create_app()
    
    # Configurações do servidor
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 8000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🚀 Iniciando MiteScan Flask API...")
    print(f"🌐 Servidor: http://{host}:{port}")
    print(f"🔧 Debug: {debug}")
    print("📚 Documentação: Acesse os endpoints via Postman ou curl")
    print("🛑 Para parar: Ctrl+C")
    print("-" * 50)
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()