"""
Configurações do Agente Minerador
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Configurações do sistema"""
    
    # Configurações do Agente
    AGENTE_INTERVALO = int(os.getenv('AGENTE_INTERVALO', 3600))  # 1 hora
    AGENTE_TIMEOUT = int(os.getenv('AGENTE_TIMEOUT', 300))
    AGENTE_USER_AGENT = os.getenv('AGENTE_USER_AGENT', 
                                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    # Configurações de Busca
    BUSCA_MAX_RESULTADOS = int(os.getenv('BUSCA_MAX_RESULTADOS', 100))
    BUSCA_DELAY_ENTRE_REQUESTS = int(os.getenv('BUSCA_DELAY_ENTRE_REQUESTS', 2))
    
    # Configurações de Armazenamento
    STORAGE_PATH = os.getenv('STORAGE_PATH', './storage')
    STORAGE_MAX_SIZE_MB = int(os.getenv('STORAGE_MAX_SIZE_MB', 1024))
    
    # Configurações de Log
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/minerador.log')
    
    # Configurações de Proxy
    USE_PROXY = os.getenv('USE_PROXY', 'false').lower() == 'true'
    PROXY_HOST = os.getenv('PROXY_HOST', '')
    PROXY_PORT = os.getenv('PROXY_PORT', '')
    PROXY_USERNAME = os.getenv('PROXY_USERNAME', '')
    PROXY_PASSWORD = os.getenv('PROXY_PASSWORD', '')
    
    # Fontes de dados para busca
    FONTES_BUSCA = [
        'https://www.google.com/search',
        'https://www.bing.com/search',
        'https://www.linkedin.com/search/results/companies',
        'https://www.empresascnpj.com',
        'https://www.receita.fazenda.gov.br'
    ]
    
    # Extensões de arquivo suportadas
    EXTENSOES_SUPORTADAS = [
        '.pdf', '.xlsx', '.xls', '.doc', '.docx', 
        '.html', '.htm', '.zip', '.csv', '.txt'
    ]
    
    # Estados brasileiros
    ESTADOS_BRASIL = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    
    # Portes de empresa
    PORTES_EMPRESA = ['Micro', 'Pequena', 'Média', 'Grande']
    
    # Nichos comuns
    NICHOS_COMUNS = [
        'Tecnologia', 'Saúde', 'Educação', 'Varejo', 'Serviços',
        'Indústria', 'Construção', 'Alimentação', 'Transporte',
        'Financeiro', 'Consultoria', 'Marketing', 'Turismo'
    ]
