"""
Sistema Principal de Mineração de Dados
"""
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time

from config.settings import Config
from utils.logger import logger
from utils.file_handler import FileHandler
from agente_agno import AgenteAGNO

class Minerador:
    """Sistema principal de mineração de dados de empresas brasileiras"""
    
    def __init__(self):
        self.agente = AgenteAGNO()
        self.file_handler = FileHandler()
        self.session_data = {}
        
    def executar_mineracao(self, porte: str, estado: str, nicho: str) -> Dict[str, Any]:
        """
        Executa processo completo de mineração
        
        Args:
            porte: Porte da empresa (Micro, Pequena, Média, Grande)
            estado: UF brasileira
            nicho: Setor de atuação
            
        Returns:
            Dicionário com resultados da mineração
        """
        start_time = datetime.now()
        logger.log_mineracao("INICIADA", f"Porte: {porte}, Estado: {estado}, Nicho: {nicho}")
        
        try:
            # Valida parâmetros
            self._validar_parametros(porte, estado, nicho)
            
            # Inicia processo de mineração
            resultados = self._processar_mineracao(porte, estado, nicho)
            
            # Salva resultados
            arquivos_gerados = self._salvar_resultados(resultados, porte, estado, nicho)
            
            # Gera relatório
            relatorio = self._gerar_relatorio(resultados, arquivos_gerados, start_time)
            
            logger.log_mineracao("CONCLUÍDA", f"Resultados: {len(resultados)} empresas, Arquivos: {len(arquivos_gerados)}")
            
            return relatorio
            
        except Exception as e:
            logger.error(f"Erro na execução da mineração: {str(e)}")
            return {
                'status': 'erro',
                'mensagem': str(e),
                'timestamp': datetime.now().isoformat()
            }
        finally:
            # Limpeza
            self.agente.cleanup()
    
    def _validar_parametros(self, porte: str, estado: str, nicho: str):
        """Valida parâmetros de entrada"""
        if porte not in Config.PORTES_EMPRESA:
            raise ValueError(f"Porte inválido. Valores aceitos: {Config.PORTES_EMPRESA}")
        
        if estado not in Config.ESTADOS_BRASIL:
            raise ValueError(f"Estado inválido. Valores aceitos: {Config.ESTADOS_BRASIL}")
        
        if not nicho or len(nicho.strip()) < 3:
            raise ValueError("Nicho deve ter pelo menos 3 caracteres")
        
        logger.info(f"Parâmetros validados: {porte}, {estado}, {nicho}")
    
    def _processar_mineracao(self, porte: str, estado: str, nicho: str) -> List[Dict[str, Any]]:
        """Processa a mineração de dados"""
        logger.info("Iniciando processo de mineração...")
        
        # Executa busca inteligente
        search_results = self.agente.smart_search(porte, estado, nicho)
        
        if not search_results:
            logger.warning("Nenhum resultado encontrado na busca")
            return []
        
        # Processa resultados
        processed_data = self.agente.process_search_results(search_results)
        
        # Filtra e valida dados
        filtered_data = self._filtrar_dados_empresas(processed_data)
        
        logger.info(f"Mineração processada: {len(filtered_data)} empresas válidas")
        return filtered_data
    
    def _filtrar_dados_empresas(self, dados: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filtra e valida dados das empresas"""
        empresas_validas = []
        
        for empresa in dados:
            # Verifica se tem informações mínimas
            if self._validar_empresa(empresa):
                empresas_validas.append(empresa)
        
        logger.info(f"Empresas validadas: {len(empresas_validas)} de {len(dados)}")
        return empresas_validas
    
    def _validar_empresa(self, empresa: Dict[str, Any]) -> bool:
        """Valida se empresa tem informações mínimas"""
        # Deve ter pelo menos uma das seguintes informações
        campos_obrigatorios = ['phone', 'email', 'address']
        campos_sociais = ['instagram', 'whatsapp', 'facebook', 'linkedin']
        
        # Verifica campos obrigatórios
        tem_campo_obrigatorio = any(empresa.get(campo) for campo in campos_obrigatorios)
        
        # Verifica redes sociais
        tem_rede_social = any(
            empresa.get('social_media', {}).get(rede) 
            for rede in campos_sociais
        )
        
        # Deve ter pelo menos um dos dois
        return tem_campo_obrigatorio or tem_rede_social
    
    def _salvar_resultados(self, resultados: List[Dict[str, Any]], 
                          porte: str, estado: str, nicho: str) -> List[str]:
        """Salva resultados em diferentes formatos"""
        arquivos_gerados = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if not resultados:
            logger.warning("Nenhum resultado para salvar")
            return []
        
        # Converte para DataFrame
        df = self._converter_para_dataframe(resultados)
        
        # Nome base dos arquivos
        base_filename = f"empresas_{porte}_{estado}_{nicho}_{timestamp}"
        
        try:
            # Salva como CSV
            csv_path = self.file_handler.save_dataframe(
                df, f"{base_filename}.csv", 'csv'
            )
            if csv_path:
                arquivos_gerados.append(csv_path)
            
            # Salva como Excel
            excel_path = self.file_handler.save_dataframe(
                df, f"{base_filename}.xlsx", 'excel'
            )
            if excel_path:
                arquivos_gerados.append(excel_path)
            
            # Salva como JSON
            json_path = self._salvar_json(resultados, f"{base_filename}.json")
            if json_path:
                arquivos_gerados.append(json_path)
            
            logger.info(f"Resultados salvos em {len(arquivos_gerados)} arquivos")
            
        except Exception as e:
            logger.error(f"Erro ao salvar resultados: {str(e)}")
        
        return arquivos_gerados
    
    def _converter_para_dataframe(self, resultados: List[Dict[str, Any]]) -> pd.DataFrame:
        """Converte resultados para DataFrame pandas"""
        dados_limpos = []
        
        for empresa in resultados:
            # Extrai dados básicos
            dados_empresa = {
                'nome': empresa.get('title', ''),
                'url': empresa.get('url', ''),
                'descricao': empresa.get('description', ''),
                'telefone': empresa.get('phone', ''),
                'email': empresa.get('email', ''),
                'endereco': empresa.get('address', ''),
                'fonte_busca': empresa.get('search_result', {}).get('source', ''),
                'instagram': empresa.get('social_media', {}).get('instagram', ''),
                'whatsapp': empresa.get('social_media', {}).get('whatsapp', ''),
                'facebook': empresa.get('social_media', {}).get('facebook', ''),
                'linkedin': empresa.get('social_media', {}).get('linkedin', ''),
                'arquivos_baixados': len(empresa.get('downloaded_files', [])),
                'timestamp_processamento': datetime.now().isoformat()
            }
            
            dados_limpos.append(dados_empresa)
        
        return pd.DataFrame(dados_limpos)
    
    def _salvar_json(self, dados: List[Dict[str, Any]], filename: str) -> str:
        """Salva dados em formato JSON"""
        try:
            json_path = self.file_handler.storage_path / 'Outros' / filename
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"JSON salvo: {json_path}")
            return str(json_path)
            
        except Exception as e:
            logger.error(f"Erro ao salvar JSON: {str(e)}")
            return None
    
    def _gerar_relatorio(self, resultados: List[Dict[str, Any]], 
                         arquivos: List[str], start_time: datetime) -> Dict[str, Any]:
        """Gera relatório da mineração"""
        end_time = datetime.now()
        duracao = end_time - start_time
        
        # Estatísticas dos resultados
        total_empresas = len(resultados)
        empresas_com_telefone = sum(1 for e in resultados if e.get('phone'))
        empresas_com_email = sum(1 for e in resultados if e.get('email'))
        empresas_com_instagram = sum(1 for e in resultados if e.get('social_media', {}).get('instagram'))
        empresas_com_whatsapp = sum(1 for e in resultados if e.get('social_media', {}).get('whatsapp'))
        
        # Informações de armazenamento
        storage_info = self.file_handler.get_storage_info()
        
        relatorio = {
            'status': 'sucesso',
            'timestamp_inicio': start_time.isoformat(),
            'timestamp_fim': end_time.isoformat(),
            'duracao_segundos': duracao.total_seconds(),
            'parametros_busca': {
                'porte': 'porte',
                'estado': 'estado',
                'nicho': 'nicho'
            },
            'resultados': {
                'total_empresas': total_empresas,
                'empresas_com_telefone': empresas_com_telefone,
                'empresas_com_email': empresas_com_email,
                'empresas_com_instagram': empresas_com_instagram,
                'empresas_com_whatsapp': empresas_com_whatsapp
            },
            'arquivos_gerados': arquivos,
            'armazenamento': storage_info,
            'resumo': f"Mineração concluída com {total_empresas} empresas encontradas em {duracao.total_seconds():.1f} segundos"
        }
        
        # Salva relatório
        self._salvar_relatorio(relatorio)
        
        return relatorio
    
    def _salvar_relatorio(self, relatorio: Dict[str, Any]):
        """Salva relatório da mineração"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"relatorio_mineracao_{timestamp}.json"
            
            relatorio_path = self.file_handler.storage_path / 'Outros' / filename
            
            with open(relatorio_path, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"Relatório salvo: {relatorio_path}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar relatório: {str(e)}")
    
    def executar_mineracao_automatica(self):
        """Executa mineração automática com parâmetros padrão"""
        logger.info("Iniciando mineração automática...")
        
        # Parâmetros padrão para teste
        parametros_padrao = [
            ('Pequena', 'SP', 'Tecnologia'),
            ('Média', 'RJ', 'Saúde'),
            ('Micro', 'MG', 'Serviços')
        ]
        
        resultados_totais = []
        
        for porte, estado, nicho in parametros_padrao:
            try:
                logger.info(f"Executando mineração para: {porte}, {estado}, {nicho}")
                
                resultado = self.executar_mineracao(porte, estado, nicho)
                resultados_totais.append(resultado)
                
                # Delay entre execuções
                time.sleep(Config.BUSCA_DELAY_ENTRE_REQUESTS * 2)
                
            except Exception as e:
                logger.error(f"Erro na mineração automática para {porte}, {estado}, {nicho}: {str(e)}")
        
        logger.info(f"Mineração automática concluída: {len(resultados_totais)} execuções")
        return resultados_totais
    
    def limpar_arquivos_antigos(self, dias: int = 30):
        """Remove arquivos antigos do armazenamento"""
        return self.file_handler.cleanup_old_files(dias)
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema"""
        storage_info = self.file_handler.get_storage_info()
        
        return {
            'armazenamento': storage_info,
            'configuracoes': {
                'intervalo_execucao': Config.AGENTE_INTERVALO,
                'timeout': Config.AGENTE_TIMEOUT,
                'max_resultados': Config.BUSCA_MAX_RESULTADOS
            },
            'timestamp': datetime.now().isoformat()
        }
