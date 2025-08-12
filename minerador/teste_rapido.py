#!/usr/bin/env python3
"""
Teste Rápido do Agente Minerador
Verifica se todos os componentes estão funcionando
"""

import sys
import os

# Adiciona o diretório atual ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def testar_imports():
    """Testa se todos os módulos podem ser importados"""
    print("🔍 Testando imports...")
    
    try:
        from config.settings import Config
        print("  ✅ config.settings.Config")
        
        from utils.logger import logger
        print("  ✅ utils.logger.logger")
        
        from utils.file_handler import FileHandler
        print("  ✅ utils.file_handler.FileHandler")
        
        from agente_agno import AgenteAGNO
        print("  ✅ agente_agno.AgenteAGNO")
        
        from minerador import Minerador
        print("  ✅ minerador.Minerador")
        
        from scheduler import AgendadorMinerador
        print("  ✅ scheduler.AgendadorMinerador")
        
        print("✅ Todos os imports funcionando!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def testar_configuracoes():
    """Testa se as configurações estão carregando"""
    print("\n⚙️  Testando configurações...")
    
    try:
        from config.settings import Config
        
        print(f"  Intervalo: {Config.AGENTE_INTERVALO}s")
        print(f"  Timeout: {Config.AGENTE_TIMEOUT}s")
        print(f"  Max Resultados: {Config.BUSCA_MAX_RESULTADOS}")
        print(f"  Storage Path: {Config.STORAGE_PATH}")
        print(f"  Estados: {len(Config.ESTADOS_BRASIL)}")
        print(f"  Portes: {len(Config.PORTES_EMPRESA)}")
        print(f"  Nichos: {len(Config.NICHOS_COMUNS)}")
        
        print("✅ Configurações carregadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro nas configurações: {e}")
        return False

def testar_logger():
    """Testa se o sistema de logging está funcionando"""
    print("\n📝 Testando logger...")
    
    try:
        from utils.logger import logger
        
        logger.info("Teste de log INFO")
        logger.warning("Teste de log WARNING")
        logger.error("Teste de log ERROR")
        
        print("✅ Logger funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no logger: {e}")
        return False

def testar_file_handler():
    """Testa se o file handler está funcionando"""
    print("\n📁 Testando file handler...")
    
    try:
        from utils.file_handler import FileHandler
        
        file_handler = FileHandler()
        storage_info = file_handler.get_storage_info()
        
        print(f"  Storage Path: {storage_info['storage_path']}")
        print(f"  Total Files: {storage_info['total_files']}")
        print(f"  Total Size: {storage_info['total_size_mb']}MB")
        
        print("✅ File handler funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no file handler: {e}")
        return False

def testar_estrutura_diretorios():
    """Testa se a estrutura de diretórios está correta"""
    print("\n📂 Testando estrutura de diretórios...")
    
    diretorios_necessarios = [
        'config',
        'utils', 
        'storage',
        'logs'
    ]
    
    arquivos_necessarios = [
        'main.py',
        'agente_agno.py',
        'minerador.py',
        'scheduler.py',
        'requirements.txt',
        'README.md'
    ]
    
    # Verifica diretórios
    for dir_name in diretorios_necessarios:
        if os.path.isdir(dir_name):
            print(f"  ✅ Diretório: {dir_name}/")
        else:
            print(f"  ❌ Diretório faltando: {dir_name}/")
            return False
    
    # Verifica arquivos
    for file_name in arquivos_necessarios:
        if os.path.isfile(file_name):
            print(f"  ✅ Arquivo: {file_name}")
        else:
            print(f"  ❌ Arquivo faltando: {file_name}")
            return False
    
    print("✅ Estrutura de diretórios correta!")
    return True

def testar_ambiente_python():
    """Testa se o ambiente Python está configurado"""
    print("\n🐍 Testando ambiente Python...")
    
    try:
        import selenium
        print(f"  ✅ Selenium: {selenium.__version__}")
        
        import pandas
        print(f"  ✅ Pandas: {pandas.__version__}")
        
        import requests
        print(f"  ✅ Requests: {requests.__version__}")
        
        import schedule
        print(f"  ✅ Schedule: {schedule.__version__}")
        
        print("✅ Dependências Python instaladas!")
        return True
        
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    """Função principal do teste"""
    print("🚀 TESTE RÁPIDO DO AGENTE MINERADOR")
    print("=" * 50)
    
    testes = [
        testar_imports,
        testar_configuracoes,
        testar_logger,
        testar_file_handler,
        testar_estrutura_diretorios,
        testar_ambiente_python
    ]
    
    resultados = []
    
    for teste in testes:
        try:
            resultado = teste()
            resultados.append(resultado)
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
            resultados.append(False)
    
    # Resumo final
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    total_testes = len(resultados)
    testes_aprovados = sum(resultados)
    
    print(f"Total de testes: {total_testes}")
    print(f"Testes aprovados: {testes_aprovados}")
    print(f"Testes reprovados: {total_testes - testes_aprovados}")
    
    if todos_aprovados := (testes_aprovados == total_testes):
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O sistema está pronto para uso!")
        print("\n💡 Para executar:")
        print("   python main.py --modo teste")
        print("   python main.py --modo agendado")
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM!")
        print("❌ Verifique os erros acima antes de usar o sistema")
    
    return todos_aprovados

if __name__ == "__main__":
    try:
        sucesso = main()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro fatal no teste: {e}")
        sys.exit(1)
