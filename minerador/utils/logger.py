"""
Sistema de logging para o Agente Minerador
"""
import logging
import os
from datetime import datetime
from config.settings import Config

class Logger:
    """Classe para gerenciar logs do sistema"""
    
    def __init__(self, name='minerador'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Cria diretório de logs se não existir
        os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
        
        # Handler para arquivo
        file_handler = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
        file_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Adiciona handlers
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log de informação"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log de aviso"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log de erro"""
        self.logger.error(message)
    
    def debug(self, message):
        """Log de debug"""
        self.logger.debug(message)
    
    def critical(self, message):
        """Log crítico"""
        self.logger.critical(message)
    
    def log_mineracao(self, acao, detalhes):
        """Log específico para ações de mineração"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"[MINERAÇÃO] {acao} - {detalhes} - {timestamp}"
        self.info(message)
    
    def log_download(self, arquivo, tamanho, status):
        """Log específico para downloads"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"[DOWNLOAD] {arquivo} - {tamanho} bytes - {status} - {timestamp}"
        self.info(message)

# Instância global do logger
logger = Logger()
