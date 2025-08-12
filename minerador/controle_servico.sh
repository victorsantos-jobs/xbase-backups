#!/bin/bash

# Script de Controle do Serviço Agente Minerador
# Gerencia o serviço systemd do sistema de mineração

SERVICE_NAME="minerador"
SERVICE_FILE="/etc/systemd/system/minerador.service"
PROJECT_DIR="/home/gosh/Desktop/minerador"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para mostrar mensagens coloridas
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                    AGENTE MINERADOR                          ║${NC}"
    echo -e "${BLUE}║              Controle de Serviço Systemd                     ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Função para verificar se o usuário é root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "Este script deve ser executado como root (sudo)"
        exit 1
    fi
}

# Função para instalar o serviço
install_service() {
    print_message "Instalando serviço $SERVICE_NAME..."
    
    # Copia arquivo de serviço
    if [ -f "$PROJECT_DIR/minerador.service" ]; then
        cp "$PROJECT_DIR/minerador.service" "$SERVICE_FILE"
        print_message "Arquivo de serviço copiado para $SERVICE_FILE"
    else
        print_error "Arquivo minerador.service não encontrado em $PROJECT_DIR"
        exit 1
    fi
    
    # Recarrega systemd
    systemctl daemon-reload
    print_message "Systemd recarregado"
    
    # Habilita serviço para iniciar com o sistema
    systemctl enable "$SERVICE_NAME"
    print_message "Serviço habilitado para iniciar automaticamente"
    
    print_message "Serviço instalado com sucesso!"
    print_message "Use: sudo $0 start|stop|restart|status"
}

# Função para remover o serviço
uninstall_service() {
    print_message "Removendo serviço $SERVICE_NAME..."
    
    # Para o serviço se estiver rodando
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        systemctl stop "$SERVICE_NAME"
        print_message "Serviço parado"
    fi
    
    # Desabilita serviço
    systemctl disable "$SERVICE_NAME"
    print_message "Serviço desabilitado"
    
    # Remove arquivo de serviço
    if [ -f "$SERVICE_FILE" ]; then
        rm "$SERVICE_FILE"
        print_message "Arquivo de serviço removido"
    fi
    
    # Recarrega systemd
    systemctl daemon-reload
    print_message "Systemd recarregado"
    
    print_message "Serviço removido com sucesso!"
}

# Função para iniciar o serviço
start_service() {
    print_message "Iniciando serviço $SERVICE_NAME..."
    
    if systemctl start "$SERVICE_NAME"; then
        print_message "Serviço iniciado com sucesso!"
    else
        print_error "Falha ao iniciar serviço"
        systemctl status "$SERVICE_NAME"
        exit 1
    fi
}

# Função para parar o serviço
stop_service() {
    print_message "Parando serviço $SERVICE_NAME..."
    
    if systemctl stop "$SERVICE_NAME"; then
        print_message "Serviço parado com sucesso!"
    else
        print_error "Falha ao parar serviço"
        exit 1
    fi
}

# Função para reiniciar o serviço
restart_service() {
    print_message "Reiniciando serviço $SERVICE_NAME..."
    
    if systemctl restart "$SERVICE_NAME"; then
        print_message "Serviço reiniciado com sucesso!"
    else
        print_error "Falha ao reiniciar serviço"
        exit 1
    fi
}

# Função para mostrar status do serviço
show_status() {
    print_message "Status do serviço $SERVICE_NAME:"
    echo ""
    systemctl status "$SERVICE_NAME" --no-pager -l
}

# Função para mostrar logs do serviço
show_logs() {
    print_message "Logs do serviço $SERVICE_NAME:"
    echo ""
    journalctl -u "$SERVICE_NAME" -f --no-pager
}

# Função para mostrar logs das últimas N linhas
show_logs_tail() {
    local lines=${1:-50}
    print_message "Últimas $lines linhas dos logs do serviço $SERVICE_NAME:"
    echo ""
    journalctl -u "$SERVICE_NAME" -n "$lines" --no-pager
}

# Função para verificar se o serviço está instalado
is_service_installed() {
    systemctl list-unit-files | grep -q "^$SERVICE_NAME.service"
}

# Função para verificar se o serviço está rodando
is_service_running() {
    systemctl is-active --quiet "$SERVICE_NAME"
}

# Função para mostrar informações do sistema
show_system_info() {
    print_message "Informações do sistema:"
    echo ""
    echo "Diretório do projeto: $PROJECT_DIR"
    echo "Arquivo de serviço: $SERVICE_FILE"
    echo "Serviço instalado: $(is_service_installed && echo "Sim" || echo "Não")"
    echo "Serviço rodando: $(is_service_running && echo "Sim" || echo "Não")"
    echo ""
    
    if is_service_installed; then
        systemctl is-enabled "$SERVICE_NAME" >/dev/null 2>&1 && echo "Serviço habilitado: Sim" || echo "Serviço habilitado: Não"
    fi
}

# Função para mostrar ajuda
show_help() {
    print_header
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  install     - Instala o serviço systemd"
    echo "  uninstall   - Remove o serviço systemd"
    echo "  start       - Inicia o serviço"
    echo "  stop        - Para o serviço"
    echo "  restart     - Reinicia o serviço"
    echo "  status      - Mostra status do serviço"
    echo "  logs        - Mostra logs em tempo real"
    echo "  logs-tail   - Mostra últimas linhas dos logs"
    echo "  info        - Mostra informações do sistema"
    echo "  help        - Mostra esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  sudo $0 install    # Instala o serviço"
    echo "  sudo $0 start      # Inicia o serviço"
    echo "  sudo $0 status     # Mostra status"
    echo "  sudo $0 logs       # Mostra logs em tempo real"
    echo ""
}

# Função principal
main() {
    case "$1" in
        install)
            check_root
            install_service
            ;;
        uninstall)
            check_root
            uninstall_service
            ;;
        start)
            check_root
            start_service
            ;;
        stop)
            check_root
            stop_service
            ;;
        restart)
            check_root
            restart_service
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        logs-tail)
            show_logs_tail "$2"
            ;;
        info)
            show_system_info
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Comando inválido: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Executa função principal
main "$@"
