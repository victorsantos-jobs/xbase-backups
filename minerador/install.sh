#!/bin/bash

# Script de Instalação do Agente Minerador
# Sistema de Mineração de Dados de Empresas Brasileiras

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    AGENTE MINERADOR                          ║"
echo "║              Sistema de Mineração de Dados                   ║"
echo "║                Empresas Brasileiras                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verifica se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instalando..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
else
    echo "✅ Python 3 encontrado: $(python3 --version)"
fi

# Verifica se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instalando..."
    sudo apt install -y python3-pip
else
    echo "✅ pip3 encontrado: $(pip3 --version)"
fi

# Cria ambiente virtual
echo "🔧 Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Atualiza pip
echo "📦 Atualizando pip..."
pip install --upgrade pip

# Instala dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Cria diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p storage logs

# Define permissões
echo "🔐 Configurando permissões..."
chmod +x main.py
chmod +x install.sh

# Cria arquivo .env se não existir
if [ ! -f .env ]; then
    echo "⚙️  Criando arquivo de configuração .env..."
    cp env.example .env
    echo "📝 Arquivo .env criado. Edite as configurações conforme necessário."
fi

echo ""
echo "✅ Instalação concluída com sucesso!"
echo ""
echo "📋 Para usar o sistema:"
echo "   1. Ative o ambiente virtual: source venv/bin/activate"
echo "   2. Configure o arquivo .env com suas preferências"
echo "   3. Execute: python main.py"
echo ""
echo "🔧 Modos de execução disponíveis:"
echo "   - Agendado (padrão): python main.py"
echo "   - Manual: python main.py --modo manual --porte Pequena --estado SP --nicho Tecnologia"
echo "   - Teste: python main.py --modo teste"
echo "   - Status: python main.py --modo status"
echo ""
echo "📚 Para mais informações, consulte o README.md"
echo ""
