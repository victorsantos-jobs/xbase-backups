"""
Agente AGNO - Sistema de Automação Web Inteligente
"""
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import re

from config.settings import Config
from utils.logger import logger
from utils.file_handler import FileHandler

class AgenteAGNO:
    """Agente AGNO para automação web e mineração de dados"""
    
    def __init__(self):
        self.driver = None
        self.file_handler = FileHandler()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': Config.AGENTE_USER_AGENT})
        
        # Configura proxy se necessário
        if Config.USE_PROXY:
            self.setup_proxy()
    
    def setup_proxy(self):
        """Configura proxy para as requisições"""
        if Config.PROXY_HOST and Config.PROXY_PORT:
            proxy_url = f"http://{Config.PROXY_HOST}:{Config.PROXY_PORT}"
            if Config.PROXY_USERNAME and Config.PROXY_PASSWORD:
                proxy_url = f"http://{Config.PROXY_USERNAME}:{Config.PROXY_PASSWORD}@{Config.PROXY_HOST}:{Config.PROXY_PORT}"
            
            self.session.proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            logger.info(f"Proxy configurado: {Config.PROXY_HOST}:{Config.PROXY_PORT}")
    
    def init_driver(self):
        """Inicializa o driver do Chrome priorizando Selenium Manager e fallback para webdriver-manager"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(f'--user-agent={Config.AGENTE_USER_AGENT}')
            chrome_options.add_argument('--window-size=1920,1080')
            prefs = {
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.notifications": 2
            }
            chrome_options.add_experimental_option("prefs", prefs)

            # 1) Tenta via Selenium Manager (recomendado pelo Selenium 4.6+)
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                logger.info("Driver Chrome inicializado (Selenium Manager)")
                return True
            except Exception as inner_e:
                logger.warning(f"Falha no Selenium Manager: {inner_e}. Tentando webdriver-manager...")
                
                # 2) Fallback via webdriver-manager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("Driver Chrome inicializado (webdriver-manager)")
                return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar driver: {str(e)}")
            return False
    
    def close_driver(self):
        """Fecha o driver do Chrome"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Driver Chrome fechado")
    
    def search_google(self, query, max_results=10):
        """Realiza busca no Google"""
        try:
            if not self.driver:
                if not self.init_driver():
                    return []
            
            search_url = f"https://www.google.com/search?q={query}"
            self.driver.get(search_url)
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.g"))
            )
            
            results = []
            elements = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            
            for element in elements[:max_results]:
                try:
                    title_element = element.find_element(By.CSS_SELECTOR, "h3")
                    link_element = element.find_element(By.CSS_SELECTOR, "a")
                    
                    title = title_element.text
                    url = link_element.get_attribute("href")
                    
                    if title and url:
                        results.append({
                            'title': title,
                            'url': url,
                            'source': 'Google'
                        })
                except:
                    continue
            
            logger.info(f"Busca Google concluída: {len(results)} resultados")
            return results
            
        except Exception as e:
            logger.error(f"Erro na busca Google: {str(e)}")
            return []
    
    def search_bing(self, query, max_results=10):
        """Realiza busca no Bing"""
        try:
            if not self.driver:
                if not self.init_driver():
                    return []
            
            search_url = f"https://www.bing.com/search?q={query}"
            self.driver.get(search_url)
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.b_algo"))
            )
            
            results = []
            elements = self.driver.find_elements(By.CSS_SELECTOR, "li.b_algo")
            
            for element in elements[:max_results]:
                try:
                    title_element = element.find_element(By.CSS_SELECTOR, "h2 a")
                    title = title_element.text
                    url = title_element.get_attribute("href")
                    
                    if title and url:
                        results.append({
                            'title': title,
                            'url': url,
                            'source': 'Bing'
                        })
                except:
                    continue
            
            logger.info(f"Busca Bing concluída: {len(results)} resultados")
            return results
            
        except Exception as e:
            logger.error(f"Erro na busca Bing: {str(e)}")
            return []
    
    def search_linkedin(self, query, max_results=10):
        """Realiza busca no LinkedIn"""
        try:
            if not self.driver:
                if not self.init_driver():
                    return []
            
            search_url = f"https://www.linkedin.com/search/results/companies/?keywords={query}"
            self.driver.get(search_url)
            
            time.sleep(5)
            
            results = []
            elements = self.driver.find_elements(By.CSS_SELECTOR, "div.search-result__info")
            
            for element in elements[:max_results]:
                try:
                    title_element = element.find_element(By.CSS_SELECTOR, "h3 a")
                    title = title_element.text
                    url = title_element.get_attribute("href")
                    
                    if title and url:
                        results.append({
                            'title': title,
                            'url': url,
                            'source': 'LinkedIn'
                        })
                except:
                    continue
            
            logger.info(f"Busca LinkedIn concluída: {len(results)} resultados")
            return results
            
        except Exception as e:
            logger.error(f"Erro na busca LinkedIn: {str(e)}")
            return []
    
    def extract_company_info(self, url):
        """Extrai informações de empresa de uma página web"""
        try:
            response = self.session.get(url, timeout=Config.AGENTE_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            company_info = {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'description': '',
                'phone': '',
                'email': '',
                'address': '',
                'social_media': {}
            }
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                company_info['description'] = meta_desc.get('content', '')
            
            phone_pattern = r'\(?\d{2,3}\)?\s*\d{4,5}-?\d{4}'
            phone_matches = re.findall(phone_pattern, response.text)
            if phone_matches:
                company_info['phone'] = phone_matches[0]
            
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email_matches = re.findall(email_pattern, response.text)
            if email_matches:
                company_info['email'] = email_matches[0]
            
            address_pattern = r'Rua\s+[^,]+,\s*\d+[^,]*,[^,]*,[^,]*'
            address_matches = re.findall(address_pattern, response.text)
            if address_matches:
                company_info['address'] = address_matches[0]
            
            social_links = soup.find_all('a', href=True)
            for link in social_links:
                href = link.get('href', '').lower()
                if 'instagram.com' in href:
                    company_info['social_media']['instagram'] = href
                elif 'facebook.com' in href:
                    company_info['social_media']['facebook'] = href
                elif 'linkedin.com' in href:
                    company_info['social_media']['linkedin'] = href
                elif 'whatsapp' in href or 'wa.me' in href:
                    company_info['social_media']['whatsapp'] = href
            
            logger.info(f"Informações extraídas de: {url}")
            return company_info
            
        except Exception as e:
            logger.error(f"Erro ao extrair informações de {url}: {str(e)}")
            return None
    
    def find_downloadable_files(self, url):
        """Encontra arquivos para download em uma página web"""
        try:
            response = self.session.get(url, timeout=Config.AGENTE_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            downloadable_files = []
            
            for link in soup.find_all('a', href=True):
                href = link.get('href', '').lower()
                for ext in Config.EXTENSOES_SUPORTADAS:
                    if href.endswith(ext):
                        file_url = urljoin(url, href)
                        downloadable_files.append({
                            'url': file_url,
                            'filename': link.text.strip() or href.split('/')[-1],
                            'extension': ext
                        })
            
            logger.info(f"Arquivos encontrados em {url}: {len(downloadable_files)}")
            return downloadable_files
            
        except Exception as e:
            logger.error(f"Erro ao buscar arquivos em {url}: {str(e)}")
            return []
    
    def download_all_files(self, url):
        """Baixa todos os arquivos encontrados em uma página"""
        files = self.find_downloadable_files(url)
        downloaded_files = []
        
        for file_info in files:
            try:
                file_path, file_size = self.file_handler.download_file(
                    file_info['url'], 
                    file_info['filename']
                )
                
                if file_path:
                    downloaded_files.append({
                        'original_url': file_info['url'],
                        'local_path': file_path,
                        'size': file_size,
                        'filename': file_info['filename']
                    })
                
                time.sleep(Config.BUSCA_DELAY_ENTRE_REQUESTS)
                
            except Exception as e:
                logger.error(f"Erro ao baixar {file_info['url']}: {str(e)}")
        
        logger.info(f"Download concluído: {len(downloaded_files)} arquivos baixados")
        return downloaded_files
    
    def smart_search(self, porte, estado, nicho):
        """Busca inteligente combinando múltiplas fontes"""
        logger.log_mineracao("INICIADA", f"Porte: {porte}, Estado: {estado}, Nicho: {nicho}")
        
        queries = [
            f'"{porte}" empresa "{nicho}" "{estado}" site instagram whatsapp',
            f'empresa "{nicho}" "{estado}" "{porte}" contato',
            f'"{nicho}" "{estado}" empresa "{porte}" telefone email'
        ]
        
        all_results = []
        
        for query in queries:
            logger.info(f"Executando busca: {query}")
            
            google_results = self.search_google(query, Config.BUSCA_MAX_RESULTADOS // 3)
            all_results.extend(google_results)
            
            bing_results = self.search_bing(query, Config.BUSCA_MAX_RESULTADOS // 3)
            all_results.extend(bing_results)
            
            linkedin_results = self.search_linkedin(query, Config.BUSCA_MAX_RESULTADOS // 3)
            all_results.extend(linkedin_results)
            
            time.sleep(Config.BUSCA_DELAY_ENTRE_REQUESTS)
        
        unique_results = []
        seen_urls = set()
        
        for result in all_results:
            if result['url'] not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result['url'])
        
        logger.info(f"Busca inteligente concluída: {len(unique_results)} resultados únicos")
        return unique_results
    
    def process_search_results(self, search_results):
        """Processa resultados de busca e extrai dados"""
        processed_data = []
        
        for result in search_results:
            try:
                logger.info(f"Processando: {result['url']}")
                
                company_info = self.extract_company_info(result['url'])
                if company_info:
                    company_info['search_result'] = result
                    processed_data.append(company_info)
                
                downloaded_files = self.download_all_files(result['url'])
                if downloaded_files:
                    company_info['downloaded_files'] = downloaded_files
                
                time.sleep(Config.BUSCA_DELAY_ENTRE_REQUESTS)
                
            except Exception as e:
                logger.error(f"Erro ao processar {result['url']}: {str(e)}")
        
        logger.info(f"Processamento concluído: {len(processed_data)} empresas processadas")
        return processed_data
    
    def cleanup(self):
        """Limpeza e finalização"""
        self.close_driver()
        self.session.close()
        logger.info("Agente AGNO finalizado")
