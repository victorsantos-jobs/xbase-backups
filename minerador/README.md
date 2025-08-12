# Agente Minerador - Empresas Brasileiras

Sistema automatizado para mineração de dados de empresas brasileiras com execução a cada hora.

## Funcionalidades

- **Agente AGNO**: Automação web inteligente
- **Minerador de Dados**: Busca empresas por porte, estado e nicho
- **Execução Automática**: Roda a cada 1 hora
- **Múltiplos Formatos**: Suporta PDF, Excel, DOC, HTML, ZIP, CSV
- **Armazenamento**: Salva arquivos na pasta `storage/`

## Configuração

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. Execute o agente:
```bash
python main.py
```

## Estrutura do Projeto

```
minerador/
├── main.py                 # Arquivo principal
├── agente_agno.py         # Agente AGNO para automação
├── minerador.py           # Lógica de mineração
├── scheduler.py           # Agendador de tarefas
├── storage/               # Pasta para arquivos baixados
├── config/                # Configurações
└── utils/                 # Utilitários
```

## Parâmetros de Entrada

- **Porte**: Micro, Pequena, Média, Grande
- **Estado**: UF brasileira (SP, RJ, MG, etc.)
- **Nicho**: Setor de atuação (Tecnologia, Saúde, etc.)

## Saída

Arquivos salvos na pasta `storage/` nos formatos:
- PDF
- Excel (.xlsx, .xls)
- Word (.doc, .docx)
- HTML
- ZIP
- CSV
