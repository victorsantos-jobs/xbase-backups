#!/usr/bin/env python3
"""
Script de Monitoramento do Agente Minerador
Monitora o sistema e gera relatórios de status
"""

import time
import psutil
import os
import json
from datetime import datetime, timedelta
import sys

# Adiciona o diretório atual ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from utils.logger import logger
from utils.file_handler import FileHandler

class MonitorSistema:
    """Monitor do sistema de mineração"""
    
    def __init__(self):
        self.file_handler = FileHandler()
        self.start_time = datetime.now()
        self.metrics = []
        
    def coletar_metricas_sistema(self):
        """Coleta métricas do sistema"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memória
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_gb = memory.used / (1024**3)
            memory_total_gb = memory.total / (1024**3)
            
            # Disco
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free_gb = disk.free / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            
            # Rede
            network = psutil.net_io_counters()
            bytes_sent = network.bytes_sent
            bytes_recv = network.bytes_recv
            
            # Processos Python
            python_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if 'python' in proc.info['name'].lower():
                        python_processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            metricas = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count
                },
                'memory': {
                    'percent': memory_percent,
                    'used_gb': round(memory_used_gb, 2),
                    'total_gb': round(memory_total_gb, 2)
                },
                'disk': {
                    'percent': disk_percent,
                    'free_gb': round(disk_free_gb, 2),
                    'total_gb': round(disk_total_gb, 2)
                },
                'network': {
                    'bytes_sent': bytes_sent,
                    'bytes_recv': bytes_recv
                },
                'python_processes': len(python_processes),
                'uptime': (datetime.now() - self.start_time).total_seconds()
            }
            
            self.metrics.append(metricas)
            
            # Mantém apenas as últimas 1000 métricas
            if len(self.metrics) > 1000:
                self.metrics = self.metrics[-1000:]
            
            return metricas
            
        except Exception as e:
            logger.error(f"Erro ao coletar métricas: {str(e)}")
            return None
    
    def verificar_armazenamento(self):
        """Verifica status do armazenamento"""
        try:
            storage_info = self.file_handler.get_storage_info()
            
            # Verifica se está próximo do limite
            if storage_info['total_size_mb'] > Config.STORAGE_MAX_SIZE_MB * 0.8:
                logger.warning(f"Armazenamento próximo do limite: {storage_info['total_size_mb']}MB / {Config.STORAGE_MAX_SIZE_MB}MB")
            
            return storage_info
            
        except Exception as e:
            logger.error(f"Erro ao verificar armazenamento: {str(e)}")
            return None
    
    def verificar_logs(self):
        """Verifica status dos logs"""
        try:
            log_file = Config.LOG_FILE
            if os.path.exists(log_file):
                log_size = os.path.getsize(log_file) / (1024 * 1024)  # MB
                log_age = time.time() - os.path.getmtime(log_file)
                
                log_info = {
                    'size_mb': round(log_size, 2),
                    'age_hours': round(log_age / 3600, 2),
                    'exists': True
                }
                
                # Verifica se o log está muito grande
                if log_size > 100:  # Mais de 100MB
                    logger.warning(f"Log muito grande: {log_size}MB")
                
                return log_info
            else:
                return {'exists': False}
                
        except Exception as e:
            logger.error(f"Erro ao verificar logs: {str(e)}")
            return None
    
    def verificar_processos_minerador(self):
        """Verifica se há processos do minerador rodando"""
        try:
            minerador_processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'main.py' in cmdline or 'minerador' in cmdline.lower():
                        minerador_processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cmdline': cmdline,
                            'cpu_percent': proc.cpu_percent(),
                            'memory_percent': proc.memory_percent()
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return minerador_processes
            
        except Exception as e:
            logger.error(f"Erro ao verificar processos: {str(e)}")
            return []
    
    def gerar_relatorio_status(self):
        """Gera relatório completo de status"""
        try:
            # Coleta todas as métricas
            metricas_sistema = self.coletar_metricas_sistema()
            armazenamento = self.verificar_armazenamento()
            logs = self.verificar_logs()
            processos = self.verificar_processos_minerador()
            
            relatorio = {
                'timestamp': datetime.now().isoformat(),
                'sistema': metricas_sistema,
                'armazenamento': armazenamento,
                'logs': logs,
                'processos_minerador': processos,
                'status_geral': self._avaliar_status_geral(metricas_sistema, armazenamento, logs)
            }
            
            return relatorio
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {str(e)}")
            return None
    
    def _avaliar_status_geral(self, metricas, armazenamento, logs):
        """Avalia status geral do sistema"""
        status = 'OK'
        alertas = []
        
        try:
            # Verifica CPU
            if metricas and metricas['cpu']['percent'] > 80:
                status = 'ATENÇÃO'
                alertas.append('CPU alta (>80%)')
            
            # Verifica memória
            if metricas and metricas['memory']['percent'] > 85:
                status = 'ATENÇÃO'
                alertas.append('Memória alta (>85%)')
            
            # Verifica disco
            if metricas and metricas['disk']['percent'] > 90:
                status = 'CRÍTICO'
                alertas.append('Disco quase cheio (>90%)')
            
            # Verifica armazenamento
            if armazenamento and armazenamento['total_size_mb'] > Config.STORAGE_MAX_SIZE_MB * 0.9:
                status = 'CRÍTICO'
                alertas.append('Armazenamento quase cheio (>90%)')
            
            # Verifica logs
            if logs and logs.get('size_mb', 0) > 100:
                alertas.append('Log muito grande (>100MB)')
            
            return {
                'status': status,
                'alertas': alertas,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'ERRO',
                'alertas': [f'Erro na avaliação: {str(e)}'],
                'timestamp': datetime.now().isoformat()
            }
    
    def salvar_relatorio(self, relatorio):
        """Salva relatório de monitoramento"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"relatorio_monitoramento_{timestamp}.json"
            
            relatorio_path = self.file_handler.storage_path / 'Outros' / filename
            
            with open(relatorio_path, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"Relatório de monitoramento salvo: {relatorio_path}")
            return str(relatorio_path)
            
        except Exception as e:
            logger.error(f"Erro ao salvar relatório: {str(e)}")
            return None
    
    def monitorar_continuamente(self, intervalo=60):
        """Monitora o sistema continuamente"""
        logger.info(f"Iniciando monitoramento contínuo (intervalo: {intervalo}s)")
        
        try:
            while True:
                # Gera e salva relatório
                relatorio = self.gerar_relatorio_status()
                if relatorio:
                    self.salvar_relatorio(relatorio)
                    
                    # Mostra status no console
                    self._mostrar_status_console(relatorio)
                
                # Aguarda próximo ciclo
                time.sleep(intervalo)
                
        except KeyboardInterrupt:
            logger.info("Monitoramento interrompido pelo usuário")
        except Exception as e:
            logger.error(f"Erro no monitoramento: {str(e)}")
    
    def _mostrar_status_console(self, relatorio):
        """Mostra status no console"""
        try:
            status = relatorio.get('status_geral', {})
            sistema = relatorio.get('sistema', {})
            armazenamento = relatorio.get('armazenamento', {})
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] STATUS: {status.get('status', 'N/A')}")
            
            if sistema:
                print(f"  CPU: {sistema.get('cpu', {}).get('percent', 'N/A')}% | "
                      f"Mem: {sistema.get('memory', {}).get('percent', 'N/A')}% | "
                      f"Disco: {sistema.get('disk', {}).get('percent', 'N/A')}%")
            
            if armazenamento:
                print(f"  Arquivos: {armazenamento.get('total_files', 'N/A')} | "
                      f"Tamanho: {armazenamento.get('total_size_mb', 'N/A')}MB")
            
            if status.get('alertas'):
                print(f"  ⚠️  Alertas: {', '.join(status['alertas'])}")
                
        except Exception as e:
            print(f"Erro ao mostrar status: {str(e)}")

def main():
    """Função principal do monitor"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor do Sistema de Mineração')
    parser.add_argument('--intervalo', type=int, default=60, help='Intervalo de monitoramento em segundos')
    parser.add_argument('--uma-vez', action='store_true', help='Executa apenas uma vez')
    
    args = parser.parse_args()
    
    monitor = MonitorSistema()
    
    if args.uma_vez:
        # Executa apenas uma vez
        relatorio = monitor.gerar_relatorio_status()
        if relatorio:
            monitor.salvar_relatorio(relatorio)
            monitor._mostrar_status_console(relatorio)
    else:
        # Monitoramento contínuo
        monitor.monitorar_continuamente(args.intervalo)

if __name__ == "__main__":
    main()
