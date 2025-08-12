"""
Configurações específicas para o Chrome WebDriver
"""
from selenium.webdriver.chrome.options import Options

def get_chrome_options():
    """Retorna opções otimizadas para o Chrome"""
    options = Options()
    
    # Configurações de performance
    options.add_argument('--headless')  # Execução sem interface gráfica
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    options.add_argument('--disable-javascript')  # Para melhor performance
    options.add_argument('--disable-logging')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    
    # Configurações de memória
    options.add_argument('--memory-pressure-off')
    options.add_argument('--max_old_space_size=4096')
    
    # Configurações de rede
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    
    # Configurações de user agent
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Configurações de janela
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    
    # Configurações de privacidade
    options.add_argument('--incognito')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Configurações de performance
    prefs = {
        "profile.managed_default_content_settings.images": 2,  # Desabilita imagens
        "profile.default_content_setting_values.notifications": 2,  # Desabilita notificações
        "profile.managed_default_content_settings.stylesheets": 2,  # Desabilita CSS
        "profile.managed_default_content_settings.cookies": 1,  # Habilita cookies
        "profile.managed_default_content_settings.javascript": 1,  # Habilita JavaScript
        "profile.managed_default_content_settings.plugins": 1,  # Habilita plugins
        "profile.managed_default_content_settings.popups": 2,  # Desabilita popups
        "profile.managed_default_content_settings.geolocation": 2,  # Desabilita geolocalização
        "profile.managed_default_content_settings.media_stream": 2,  # Desabilita mídia
    }
    options.add_experimental_option("prefs", prefs)
    
    # Configurações experimentais
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    return options

def get_chrome_options_debug():
    """Retorna opções do Chrome para debug (com interface gráfica)"""
    options = get_chrome_options()
    
    # Remove headless para debug
    options.arguments = [arg for arg in options.arguments if arg != '--headless']
    
    # Habilita logs detalhados
    options.add_argument('--enable-logging')
    options.add_argument('--v=1')
    
    return options

def get_chrome_options_mobile():
    """Retorna opções do Chrome para simulação mobile"""
    options = get_chrome_options()
    
    # Configurações mobile
    mobile_emulation = {
        "deviceMetrics": {
            "width": 375,
            "height": 667,
            "pixelRatio": 2.0
        },
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    }
    
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    return options
