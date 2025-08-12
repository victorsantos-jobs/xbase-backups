#!/usr/bin/env python3
"""
Agente Minerador - Sistema Principal
Executa mineração automática de dados de empresas brasileiras a cada hora
"""

import argparse
import sys
import os
from datetime import datetime

# Adiciona o diretório atual ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from utils.logger import logger
from scheduler import AgendadorMinerador
from minerador import Minerador

def main():
    """Função principal do sistema"""
    parser = argparse.ArgumentParser(
        description='Agente Minerador - Sistema de Mineração de Dados de Empresas Brasileiras'
    )
    
    parser.add_argument(
        '--modo',
        choices=['agendado', 'manual', 'teste', 'status'],
        default='agendado',
        help='Modo de execução (padrão: agendado)'
    )
    
    parser.add_argument(
        '--porte',
        choices=Config.PORTES_EMPRESA,
        help='Porte da empresa para busca manual'
    )
    
    parser.add_argument(
        '--estado',
        choices=Config.ESTADOS_BRASIL,
        help='Estado (UF) para busca manual'
    )
    
    parser.add_argument(
        '--nicho',
        help='Nichos de atuação para busca manual'
    )
    
    parser.add_argument(
        '--intervalo',
        type=int,
        default=Config.AGENTE_INTERVALO,
        help=f'Intervalo de execução em segundos (padrão: {Config.AGENTE_INTERVALO})'
    )
    
    parser.add_argument(
        '--limpar',
        action='store_true',
        help='Limpar arquivos antigos antes de executar'
    )
    
    parser.add_argument(
        '--estatisticas',
        action='store_true',
        help='Mostrar estatísticas do sistema'
    )
    
    args = parser.parse_args()
    
    try:
        # Configura intervalo personalizado se especificado
        if args.intervalo != Config.AGENTE_INTERVALO:
            Config.AGENTE_INTERVALO = args.intervalo
            logger.info(f"Intervalo configurado para {args.intervalo} segundos")
        
        # Executa modo selecionado
        if args.modo == 'agendado':
            executar_modo_agendado(args)
        elif args.modo == 'manual':
            executar_modo_manual(args)
        elif args.modo == 'teste':
            executar_modo_teste()
        elif args.modo == 'status':
            mostrar_status()
        
    except KeyboardInterrupt:
        logger.info("Interrupção recebida pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro na execução principal: {str(e)}")
        sys.exit(1)

def executar_modo_agendado(args):
    """Executa o sistema em modo agendado"""
    logger.info("=== INICIANDO MODO AGENDADO ===")
    
    # Limpa arquivos antigos se solicitado
    if args.limpar:
        limpar_arquivos_antigos()
    
    # Mostra estatísticas se solicitado
    if args.estatisticas:
        mostrar_estatisticas()
    
    # Inicia agendador
    agendador = AgendadorMinerador()
    
    try:
        agendador.iniciar()
        logger.info("Sistema agendado iniciado. Pressione Ctrl+C para parar.")
        
        # Aguarda execuções
        agendador.aguardar_execucao()
        
    except KeyboardInterrupt:
        logger.info("Interrupção recebida. Finalizando...")
    finally:
        agendador.parar()
        logger.info("Sistema agendado finalizado")

def executar_modo_manual(args):
    """Executa o sistema em modo manual"""
    logger.info("=== INICIANDO MODO MANUAL ===")
    
    # Valida parâmetros obrigatórios
    if not all([args.porte, args.estado, args.nicho]):
        logger.error("Modo manual requer --porte, --estado e --nicho")
        sys.exit(1)
    
    logger.info(f"Executando mineração manual: {args.porte}, {args.estado}, {args.nicho}")
    
    # Executa mineração
    minerador = Minerador()
    
    try:
        resultado = minerador.executar_mineracao(args.porte, args.estado, args.nicho)
        
        if resultado and resultado.get('status') == 'sucesso':
            logger.info("Mineração manual concluída com sucesso!")
            logger.info(f"Resultado: {resultado.get('resumo', 'N/A')}")
        else:
            logger.error("Mineração manual falhou")
            if resultado:
                logger.error(f"Erro: {resultado.get('mensagem', 'Erro desconhecido')}")
            
    except Exception as e:
        logger.error(f"Erro na mineração manual: {str(e)}")
    finally:
        minerador.agente.cleanup()

def executar_modo_teste():
    """Executa o sistema em modo de teste"""
    logger.info("=== INICIANDO MODO TESTE ===")
    
    # Testa componentes básicos
    testar_componentes()
    
    # Executa mineração de teste
    minerador = Minerador()
    
    try:
        logger.info("Executando mineração de teste...")
        resultado = minerador.executar_mineracao_automatica()
        
        logger.info(f"Teste concluído: {len(resultado)} execuções")
        
        # Mostra estatísticas
        stats = minerador.obter_estatisticas()
        logger.info(f"Estatísticas: {stats}")
        
    except Exception as e:
        logger.error(f"Erro no teste: {str(e)}")
    finally:
        minerador.agente.cleanup()

def testar_componentes():
    """Testa componentes básicos do sistema"""
    logger.info("Testando componentes do sistema...")
    
    try:
        # Testa configurações
        logger.info(f"Configurações carregadas: {Config.AGENTE_INTERVALO}s")
        
        # Testa logger
        logger.info("Logger funcionando")
        
        # Testa file handler
        from utils.file_handler import FileHandler
        file_handler = FileHandler()
        storage_info = file_handler.get_storage_info()
        logger.info(f"File handler funcionando: {storage_info}")
        
        logger.info("Todos os componentes funcionando corretamente")
        
    except Exception as e:
        logger.error(f"Erro no teste de componentes: {str(e)}")
        raise

def mostrar_status():
    """Mostra status do sistema"""
    logger.info("=== STATUS DO SISTEMA ===")
    
    try:
        # Status do agendador
        agendador = AgendadorMinerador()
        status = agendador.obter_status()
        
        logger.info("Status do Agendador:")
        for key, value in status.items():
            logger.info(f"  {key}: {value}")
        
        # Estatísticas de armazenamento
        from utils.file_handler import FileHandler
        file_handler = FileHandler()
        storage_info = file_handler.get_storage_info()
        
        logger.info("Informações de Armazenamento:")
        for key, value in storage_info.items():
            logger.info(f"  {key}: {value}")
        
        # Configurações atuais
        logger.info("Configurações Atuais:")
        logger.info(f"  Intervalo: {Config.AGENTE_INTERVALO}s")
        logger.info(f"  Timeout: {Config.AGENTE_TIMEOUT}s")
        logger.info(f"  Max Resultados: {Config.BUSCA_MAX_RESULTADOS}")
        
    except Exception as e:
        logger.error(f"Erro ao obter status: {str(e)}")

def mostrar_estatisticas():
    """Mostra estatísticas do sistema"""
    logger.info("=== ESTATÍSTICAS DO SISTEMA ===")
    
    try:
        minerador = Minerador()
        stats = minerador.obter_estatisticas()
        
        for key, value in stats.items():
            if isinstance(value, dict):
                logger.info(f"{key}:")
                for sub_key, sub_value in value.items():
                    logger.info(f"  {sub_key}: {sub_value}")
            else:
                logger.info(f"{key}: {value}")
                
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {str(e)}")

def limpar_arquivos_antigos():
    """Limpa arquivos antigos do sistema"""
    logger.info("=== LIMPANDO ARQUIVOS ANTIGOS ===")
    
    try:
        from utils.file_handler import FileHandler
        file_handler = FileHandler()
        
        arquivos_removidos = file_handler.cleanup_old_files(dias=30)
        logger.info(f"Limpeza concluída: {arquivos_removidos} arquivos removidos")
        
    except Exception as e:
        logger.error(f"Erro na limpeza: {str(e)}")

def mostrar_banner():
    """Mostra banner do sistema"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    AGENTE MINERADOR                          ║
║              Sistema de Mineração de Dados                   ║
║                Empresas Brasileiras                          ║
║                                                              ║
║  Tecnologia: Agente AGNO                                    ║
║  Execução: A cada 1 hora                                    ║
║  Saída: PDF, Excel, DOC, HTML, ZIP, CSV                    ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

if __name__ == "__main__":
    mostrar_banner()
    main()
