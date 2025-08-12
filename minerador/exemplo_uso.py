#!/usr/bin/env python3
"""
Exemplo de Uso do Agente Minerador
Demonstra como usar o sistema programaticamente
"""

import sys
import os
from datetime import datetime

# Adiciona o diretório atual ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from minerador import Minerador
from scheduler import AgendadorMinerador
from utils.logger import logger

def exemplo_mineracao_manual():
    """Exemplo de mineração manual"""
    print("=== EXEMPLO: MINERAÇÃO MANUAL ===")
    
    minerador = Minerador()
    
    try:
        # Executa mineração com parâmetros específicos
        resultado = minerador.executar_mineracao(
            porte="Pequena",
            estado="SP",
            nicho="Tecnologia"
        )
        
        if resultado and resultado.get('status') == 'sucesso':
            print(f"✅ Mineração concluída: {resultado.get('resumo')}")
            print(f"📊 Empresas encontradas: {resultado.get('resultados', {}).get('total_empresas', 0)}")
            print(f"📁 Arquivos gerados: {len(resultado.get('arquivos_gerados', []))}")
        else:
            print(f"❌ Mineração falhou: {resultado.get('mensagem', 'Erro desconhecido')}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    finally:
        minerador.agente.cleanup()

def exemplo_mineracao_automatica():
    """Exemplo de mineração automática"""
    print("\n=== EXEMPLO: MINERAÇÃO AUTOMÁTICA ===")
    
    minerador = Minerador()
    
    try:
        # Executa mineração automática com parâmetros padrão
        resultados = minerador.executar_mineracao_automatica()
        
        print(f"✅ Mineração automática concluída: {len(resultados)} execuções")
        
        for i, resultado in enumerate(resultados, 1):
            if resultado and resultado.get('status') == 'sucesso':
                print(f"  Execução {i}: {resultado.get('resumo')}")
            else:
                print(f"  Execução {i}: Falhou - {resultado.get('mensagem', 'Erro desconhecido')}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    finally:
        minerador.agente.cleanup()

def exemplo_agendador():
    """Exemplo de uso do agendador"""
    print("\n=== EXEMPLO: AGENDADOR ===")
    
    agendador = AgendadorMinerador()
    
    try:
        # Inicia agendador
        agendador.iniciar()
        
        # Mostra status
        status = agendador.obter_status()
        print("Status do Agendador:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        # Executa mineração manual através do agendador
        resultado = agendador.executar_mineracao_manual(
            porte="Média",
            estado="RJ",
            nicho="Saúde"
        )
        
        if resultado:
            print(f"✅ Mineração manual executada: {resultado.get('resumo', 'N/A')}")
        
        # Para agendador
        agendador.parar()
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        agendador.parar()

def exemplo_estatisticas():
    """Exemplo de obtenção de estatísticas"""
    print("\n=== EXEMPLO: ESTATÍSTICAS ===")
    
    minerador = Minerador()
    
    try:
        # Obtém estatísticas do sistema
        stats = minerador.obter_estatisticas()
        
        print("Estatísticas do Sistema:")
        for key, value in stats.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for sub_key, sub_value in value.items():
                    print(f"    {sub_key}: {sub_value}")
            else:
                print(f"  {key}: {value}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    finally:
        minerador.agente.cleanup()

def exemplo_limpeza():
    """Exemplo de limpeza de arquivos"""
    print("\n=== EXEMPLO: LIMPEZA DE ARQUIVOS ===")
    
    minerador = Minerador()
    
    try:
        # Limpa arquivos antigos (mais de 30 dias)
        arquivos_removidos = minerador.limpar_arquivos_antigos(dias=30)
        
        print(f"✅ Limpeza concluída: {arquivos_removidos} arquivos removidos")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    finally:
        minerador.agente.cleanup()

def main():
    """Função principal dos exemplos"""
    print("🚀 EXEMPLOS DE USO DO AGENTE MINERADOR")
    print("=" * 50)
    
    try:
        # Executa exemplos
        exemplo_mineracao_manual()
        exemplo_mineracao_automatica()
        exemplo_agendador()
        exemplo_estatisticas()
        exemplo_limpeza()
        
        print("\n✅ Todos os exemplos executados com sucesso!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro na execução dos exemplos: {str(e)}")

if __name__ == "__main__":
    main()
