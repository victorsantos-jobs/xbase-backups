# RESUMO DO PROJETO - AGENTE MINERADOR

## 🎯 Objetivo Implementado
Sistema automatizado para mineração de dados de empresas brasileiras com execução a cada hora, utilizando tecnologia de agente AGNO para automação web.

## 🏗️ Arquitetura Implementada

### 1. **Agente AGNO** (`agente_agno.py`)
- Automação web inteligente com Selenium
- Busca em múltiplas fontes (Google, Bing, LinkedIn)
- Extração de informações de empresas (telefone, email, redes sociais)
- Download automático de arquivos (PDF, Excel, DOC, HTML, ZIP, CSV)
- Configurações otimizadas para Chrome WebDriver

### 2. **Sistema de Mineração** (`minerador.py`)
- Processamento inteligente de dados
- Validação e filtragem de empresas
- Geração de relatórios em múltiplos formatos
- Sistema de armazenamento organizado por tipo de arquivo

### 3. **Agendador Automático** (`scheduler.py`)
- Execução automática a cada hora (configurável)
- Jobs de limpeza e estatísticas diárias
- Controle de threads e execuções simultâneas
- Logs detalhados de execução

### 4. **Sistema de Armazenamento** (`utils/file_handler.py`)
- Organização automática por tipo de arquivo
- Suporte a múltiplos formatos
- Controle de tamanho e limpeza automática
- Extração e processamento de arquivos

### 5. **Sistema de Logging** (`utils/logger.py`)
- Logs estruturados com timestamps
- Rotação automática de arquivos
- Diferentes níveis de log (INFO, WARNING, ERROR)
- Logs específicos para mineração e downloads

## 📁 Estrutura do Projeto

```
minerador/
├── main.py                 # Arquivo principal com CLI
├── agente_agno.py         # Agente AGNO para automação
├── minerador.py           # Sistema principal de mineração
├── scheduler.py           # Agendador automático
├── monitor.py             # Sistema de monitoramento
├── teste_rapido.py        # Script de teste rápido
├── exemplo_uso.py         # Exemplos de uso programático
├── install.sh             # Script de instalação
├── controle_servico.sh    # Controle do serviço systemd
├── minerador.service      # Configuração do serviço
├── requirements.txt       # Dependências Python
├── env.example            # Exemplo de variáveis de ambiente
├── README.md              # Documentação principal
├── RESUMO_PROJETO.md      # Este arquivo
├── config/                # Configurações do sistema
│   ├── __init__.py
│   ├── settings.py        # Configurações principais
│   └── chrome_config.py   # Configurações do Chrome
├── utils/                 # Utilitários do sistema
│   ├── __init__.py
│   ├── logger.py          # Sistema de logging
│   └── file_handler.py    # Manipulação de arquivos
├── storage/               # Armazenamento de arquivos
│   ├── PDFs/              # Arquivos PDF
│   ├── Excel/             # Arquivos Excel
│   ├── Word/              # Arquivos Word
│   ├── HTML/              # Arquivos HTML
│   ├── ZIP/               # Arquivos ZIP
│   ├── CSV/               # Arquivos CSV
│   └── Outros/            # Outros tipos
└── logs/                  # Arquivos de log
```

## 🚀 Funcionalidades Implementadas

### ✅ **Mineração Automática**
- Execução a cada hora (configurável)
- Busca por porte, estado e nicho
- Extração de dados de empresas brasileiras
- Download automático de arquivos

### ✅ **Múltiplos Formatos de Saída**
- PDF, Excel (.xlsx, .xls)
- Word (.doc, .docx)
- HTML, ZIP, CSV
- Organização automática por tipo

### ✅ **Sistema de Agendamento**
- Execução automática configurável
- Jobs de manutenção diários
- Controle de execuções simultâneas
- Logs detalhados de performance

### ✅ **Monitoramento e Controle**
- Script de monitoramento contínuo
- Controle via serviço systemd
- Estatísticas em tempo real
- Alertas automáticos

### ✅ **Interface de Linha de Comando**
- Múltiplos modos de execução
- Parâmetros configuráveis
- Testes automáticos
- Status e estatísticas

## 🔧 Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **Selenium** - Automação web
- **Chrome WebDriver** - Navegação automatizada
- **BeautifulSoup** - Parsing HTML
- **Pandas** - Manipulação de dados
- **Schedule** - Agendamento de tarefas
- **Requests** - Requisições HTTP
- **Systemd** - Serviço do sistema

## 📊 Parâmetros de Entrada

### **Porte da Empresa**
- Micro, Pequena, Média, Grande

### **Estados Brasileiros**
- Todas as 27 UFs (AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO)

### **Nichos de Atuação**
- Tecnologia, Saúde, Educação, Varejo, Serviços, Indústria, Construção, Alimentação, Transporte, Financeiro, Consultoria, Marketing, Turismo

## 📈 Saídas Geradas

### **Arquivos de Dados**
- Relatórios em CSV, Excel e JSON
- Arquivos baixados organizados por tipo
- Logs detalhados de execução
- Estatísticas de performance

### **Informações Extraídas**
- Nome e descrição da empresa
- Telefone e email de contato
- Endereço físico
- Redes sociais (Instagram, WhatsApp, Facebook, LinkedIn)
- URLs dos sites oficiais

## 🚀 Como Usar

### **1. Instalação**
```bash
# Executa script de instalação
./install.sh

# Ou manualmente
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **2. Configuração**
```bash
# Copia arquivo de exemplo
cp env.example .env

# Edita configurações
nano .env
```

### **3. Execução**
```bash
# Modo agendado (padrão)
python main.py

# Modo manual
python main.py --modo manual --porte Pequena --estado SP --nicho Tecnologia

# Modo teste
python main.py --modo teste

# Verificar status
python main.py --modo status
```

### **4. Como Serviço**
```bash
# Instala como serviço
sudo ./controle_servico.sh install

# Inicia serviço
sudo ./controle_servico.sh start

# Verifica status
sudo ./controle_servico.sh status

# Para serviço
sudo ./controle_servico.sh stop
```

## 📋 Scripts Disponíveis

- **`main.py`** - Sistema principal com CLI
- **`teste_rapido.py`** - Teste rápido dos componentes
- **`monitor.py`** - Monitoramento contínuo do sistema
- **`exemplo_uso.py`** - Exemplos de uso programático
- **`install.sh`** - Instalação automática
- **`controle_servico.sh`** - Controle do serviço systemd

## 🔍 Monitoramento

### **Script de Monitoramento**
```bash
# Monitoramento contínuo
python monitor.py

# Verificação única
python monitor.py --uma-vez

# Intervalo personalizado
python monitor.py --intervalo 300  # 5 minutos
```

### **Logs do Sistema**
- Logs detalhados em `logs/minerador.log`
- Relatórios de execução em `storage/Outros/`
- Estatísticas de monitoramento
- Alertas automáticos de problemas

## 🎉 Status do Projeto

✅ **COMPLETAMENTE IMPLEMENTADO**

- ✅ Agente AGNO para automação web
- ✅ Sistema de mineração de dados
- ✅ Agendador automático (a cada hora)
- ✅ Múltiplos formatos de saída
- ✅ Sistema de armazenamento organizado
- ✅ Monitoramento e controle
- ✅ Interface de linha de comando
- ✅ Serviço systemd
- ✅ Scripts de instalação e controle
- ✅ Sistema de logging completo
- ✅ Testes automatizados
- ✅ Documentação completa

## 🚀 Próximos Passos Sugeridos

1. **Configurar variáveis de ambiente** no arquivo `.env`
2. **Executar teste rápido** com `python teste_rapido.py`
3. **Testar mineração manual** com parâmetros específicos
4. **Configurar como serviço** para execução automática
5. **Monitorar execuções** e ajustar configurações conforme necessário

---

**🎯 O sistema está pronto para uso em produção!**
