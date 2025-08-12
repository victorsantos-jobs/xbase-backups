"""
Utilitários para manipulação de arquivos e downloads
"""
import os
import requests
import zipfile
import pandas as pd
from urllib.parse import urlparse, urljoin
from pathlib import Path
from config.settings import Config
from utils.logger import logger

class FileHandler:
    """Classe para manipulação de arquivos e downloads"""
    
    def __init__(self):
        self.storage_path = Path(Config.STORAGE_PATH)
        self.storage_path.mkdir(exist_ok=True)
        
        # Cria subdiretórios por tipo de arquivo
        self.create_storage_dirs()
    
    def create_storage_dirs(self):
        """Cria diretórios de armazenamento organizados por tipo"""
        dirs = {
            'pdfs': 'PDFs',
            'excel': 'Excel',
            'word': 'Word',
            'html': 'HTML',
            'zip': 'ZIP',
            'csv': 'CSV',
            'outros': 'Outros'
        }
        
        for key, dir_name in dirs.items():
            dir_path = self.storage_path / dir_name
            dir_path.mkdir(exist_ok=True)
            logger.debug(f"Diretório criado: {dir_path}")
    
    def get_file_extension(self, url, content_type=None):
        """Determina a extensão do arquivo baseado na URL e content-type"""
        # Tenta extrair da URL
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        
        # Mapeia extensões comuns
        extension_map = {
            '.pdf': 'pdfs',
            '.xlsx': 'excel',
            '.xls': 'excel',
            '.doc': 'word',
            '.docx': 'word',
            '.html': 'html',
            '.htm': 'html',
            '.zip': 'zip',
            '.csv': 'csv'
        }
        
        # Verifica extensão na URL
        for ext, dir_name in extension_map.items():
            if path.endswith(ext):
                return ext, dir_name
        
        # Verifica content-type se disponível
        if content_type:
            content_map = {
                'application/pdf': ('.pdf', 'pdfs'),
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ('.xlsx', 'excel'),
                'application/vnd.ms-excel': ('.xls', 'excel'),
                'application/msword': ('.doc', 'word'),
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ('.docx', 'word'),
                'text/html': ('.html', 'html'),
                'application/zip': ('.zip', 'zip'),
                'text/csv': ('.csv', 'csv')
            }
            
            if content_type in content_map:
                return content_map[content_type]
        
        # Padrão
        return '.txt', 'outros'
    
    def download_file(self, url, filename=None, headers=None):
        """Download de arquivo da web"""
        try:
            if headers is None:
                headers = {'User-Agent': Config.AGENTE_USER_AGENT}
            
            logger.info(f"Iniciando download: {url}")
            
            response = requests.get(url, headers=headers, timeout=Config.AGENTE_TIMEOUT)
            response.raise_for_status()
            
            # Determina extensão e diretório
            ext, dir_name = self.get_file_extension(url, response.headers.get('content-type'))
            
            # Define nome do arquivo
            if filename is None:
                filename = f"download_{len(os.listdir(self.storage_path / dir_name)) + 1}{ext}"
            
            # Caminho completo do arquivo
            file_path = self.storage_path / dir_name / filename
            
            # Salva arquivo
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content)
            logger.log_download(filename, file_size, "SUCESSO")
            
            return str(file_path), file_size
            
        except Exception as e:
            logger.error(f"Erro no download de {url}: {str(e)}")
            return None, 0
    
    def extract_zip(self, zip_path, extract_to=None):
        """Extrai arquivo ZIP"""
        try:
            if extract_to is None:
                extract_to = self.storage_path / 'ZIP' / 'extracted'
            
            extract_to.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            
            logger.info(f"ZIP extraído: {zip_path} -> {extract_to}")
            return str(extract_to)
            
        except Exception as e:
            logger.error(f"Erro ao extrair ZIP {zip_path}: {str(e)}")
            return None
    
    def read_excel(self, file_path):
        """Lê arquivo Excel e retorna dados"""
        try:
            df = pd.read_excel(file_path)
            logger.info(f"Excel lido com sucesso: {file_path} - {len(df)} linhas")
            return df
        except Exception as e:
            logger.error(f"Erro ao ler Excel {file_path}: {str(e)}")
            return None
    
    def read_csv(self, file_path):
        """Lê arquivo CSV e retorna dados"""
        try:
            df = pd.read_csv(file_path)
            logger.info(f"CSV lido com sucesso: {file_path} - {len(df)} linhas")
            return df
        except Exception as e:
            logger.error(f"Erro ao ler CSV {file_path}: {str(e)}")
            return None
    
    def save_dataframe(self, df, filename, format_type='csv'):
        """Salva DataFrame em diferentes formatos"""
        try:
            if format_type.lower() == 'csv':
                file_path = self.storage_path / 'CSV' / filename
                df.to_csv(file_path, index=False)
            elif format_type.lower() == 'excel':
                file_path = self.storage_path / 'Excel' / filename
                df.to_excel(file_path, index=False)
            
            logger.info(f"DataFrame salvo: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Erro ao salvar DataFrame: {str(e)}")
            return None
    
    def get_storage_info(self):
        """Retorna informações sobre o armazenamento"""
        total_size = 0
        file_count = 0
        
        for root, dirs, files in os.walk(self.storage_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(file_path)
                    file_count += 1
                except:
                    pass
        
        return {
            'total_files': file_count,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'storage_path': str(self.storage_path)
        }
    
    def cleanup_old_files(self, days_old=30):
        """Remove arquivos antigos"""
        import time
        current_time = time.time()
        removed_count = 0
        
        for root, dirs, files in os.walk(self.storage_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > (days_old * 24 * 3600):
                        os.remove(file_path)
                        removed_count += 1
                        logger.info(f"Arquivo antigo removido: {file_path}")
                except:
                    pass
        
        logger.info(f"Limpeza concluída: {removed_count} arquivos removidos")
        return removed_count
