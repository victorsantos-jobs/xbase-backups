# 📋 INSTRUÇÕES DE INSTALAÇÃO - AGENTE MINERADOR

## 🎯 Visão Geral
Este documento contém instruções detalhadas para instalar e configurar o Agente Minerador em seu sistema Linux.

## 🔧 Pré-requisitos

### **Sistema Operacional**
- ✅ Linux (Ubuntu 18.04+, Debian 10+, CentOS 7+)
- ❌ Windows (não testado)
- ❌ macOS (não testado)

### **Software Necessário**
- Python 3.8 ou superior
- pip3 (gerenciador de pacotes Python)
- Chrome ou Chromium (para WebDriver)
- Git (opcional, para clonar repositório)

## 🚀 Instalação Rápida (Recomendado)

### **1. Executar Script de Instalação Automática**
```bash
# Torne o script executável
chmod +x install.sh

# Execute a instalação
./install.sh
```

O script irá:
- ✅ Verificar e instalar Python 3
- ✅ Criar ambiente virtual
- ✅ Instalar todas as dependências
- ✅ Configurar diretórios
- ✅ Criar arquivo de configuração

### **2. Ativar Ambiente Virtual**
```bash
source venv/bin/activate
```

### **3. Testar Instalação**
```bash
python teste_rapido.py
```

## 🔧 Instalação Manual (Passo a Passo)

### **Passo 1: Verificar Python**
```bash
# Verifica versão do Python
python3 --version

# Se não estiver instalado
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### **Passo 2: Criar Ambiente Virtual**
```bash
# Cria ambiente virtual
python3 -m venv venv

# Ativa ambiente virtual
source venv/bin/activate

# Verifica se está ativo (deve mostrar caminho do venv)
which python
```

### **Passo 3: Instalar Dependências**
```bash
# Atualiza pip
pip install --upgrade pip

# Instala dependências
pip install -r requirements.txt
```

### **Passo 4: Configurar Diretórios**
```bash
# Cria diretórios necessários
mkdir -p storage logs

# Define permissões
chmod +x *.py *.sh
```

### **Passo 5: Configurar Variáveis de Ambiente**
```bash
# Copia arquivo de exemplo
cp env.example .env

# Edita configurações (opcional)
nano .env
```

## 🧪 Testando a Instalação

### **Teste Rápido**
```bash
# Executa teste completo
python teste_rapido.py
```

**Resultado Esperado:**
```
🎉 TODOS OS TESTES PASSARAM!
✅ O sistema está pronto para uso!
```

### **Teste de Componentes Individuais**
```bash
# Testa configurações
python -c "from config.settings import Config; print('Config OK')"

# Testa logger
python -c "from utils.logger import logger; logger.info('Teste')"

# Testa file handler
python -c "from utils.file_handler import FileHandler; fh = FileHandler(); print('FileHandler OK')"
```

## 🚀 Primeira Execução

### **1. Modo Teste (Recomendado para início)**
```bash
python main.py --modo teste
```

### **2. Modo Manual (Teste específico)**
```bash
python main.py --modo manual --porte Pequena --estado SP --nicho Tecnologia
```

### **3. Modo Agendado (Produção)**
```bash
python main.py --modo agendado
```

## 🔧 Configuração Avançada

### **Arquivo .env**
```bash
# Copia arquivo de exemplo
cp env.example .env

# Edita configurações
nano .env
```

**Configurações Importantes:**
```env
# Intervalo de execução (em segundos)
AGENTE_INTERVALO=3600  # 1 hora

# Timeout para operações web
AGENTE_TIMEOUT=300     # 5 minutos

# Limite de armazenamento
STORAGE_MAX_SIZE_MB=1024  # 1GB

# Nível de log
LOG_LEVEL=INFO
```

### **Configurações do Chrome**
```bash
# Edita configurações do Chrome
nano config/chrome_config.py
```

## 🐛 Solução de Problemas

### **Erro: "No module named 'selenium'"**
```bash
# Solução: Instalar dependências
pip install -r requirements.txt

# Ou instalar individualmente
pip install selenium webdriver-manager
```

### **Erro: "Chrome not found"**
```bash
# Instala Chrome
sudo apt update
sudo apt install -y google-chrome-stable

# Ou Chromium
sudo apt install -y chromium-browser
```

### **Erro: "Permission denied"**
```bash
# Corrige permissões
chmod +x *.py *.sh
chmod 755 storage logs
```

### **Erro: "Port already in use"**
```bash
# Verifica processos
ps aux | grep python

# Mata processo se necessário
kill -9 <PID>
```

## 📊 Verificação de Status

### **Status do Sistema**
```bash
python main.py --modo status
```

### **Monitoramento em Tempo Real**
```bash
python monitor.py
```

### **Logs do Sistema**
```bash
# Últimas linhas
tail -f logs/minerador.log

# Busca por erro
grep ERROR logs/minerador.log
```

## 🔄 Atualizações

### **Atualizar Dependências**
```bash
# Ativa ambiente virtual
source venv/bin/activate

# Atualiza dependências
pip install --upgrade -r requirements.txt
```

### **Atualizar Código**
```bash
# Se usando Git
git pull origin main

# Reinicia serviço se necessário
sudo ./controle_servico.sh restart
```

## 🚀 Configuração como Serviço (Opcional)

### **Instalar como Serviço Systemd**
```bash
# Instala serviço
sudo ./controle_servico.sh install

# Inicia serviço
sudo ./controle_servico.sh start

# Verifica status
sudo ./controle_servico.sh status
```

### **Comandos do Serviço**
```bash
# Iniciar
sudo ./controle_servico.sh start

# Parar
sudo ./controle_servico.sh stop

# Reiniciar
sudo ./controle_servico.sh restart

# Status
sudo ./controle_servico.sh status

# Logs
sudo ./controle_servico.sh logs
```

## 📋 Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Diretórios criados (`storage/`, `logs/`)
- [ ] Arquivo `.env` configurado
- [ ] Teste rápido executado com sucesso
- [ ] Primeira execução testada
- [ ] Serviço configurado (opcional)

## 🆘 Suporte

### **Logs de Erro**
- Verifique `logs/minerador.log`
- Execute `python teste_rapido.py`
- Use `python main.py --modo status`

### **Problemas Comuns**
1. **Dependências não instaladas** → Execute `pip install -r requirements.txt`
2. **Chrome não encontrado** → Instale Google Chrome ou Chromium
3. **Permissões negadas** → Execute `chmod +x *.py *.sh`
4. **Porta em uso** → Verifique processos com `ps aux | grep python`

### **Comandos de Diagnóstico**
```bash
# Verifica Python
python3 --version

# Verifica pip
pip --version

# Verifica ambiente virtual
echo $VIRTUAL_ENV

# Verifica dependências
pip list

# Verifica estrutura
ls -la
tree -L 2
```

---

## 🎉 Instalação Concluída!

Após seguir todas as etapas acima, seu Agente Minerador estará funcionando e executando mineração automática a cada hora!

**Próximo passo:** Configure o arquivo `.env` com suas preferências e execute `python main.py --modo agendado` para iniciar a mineração automática.
