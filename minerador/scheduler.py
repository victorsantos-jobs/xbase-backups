"""
Sistema de Agendamento para Execução Automática
"""
import schedule
import time
import threading
from datetime import datetime, timedelta
import signal
import sys

from config.settings import Config
from utils.logger import logger
from minerador import Minerador

class AgendadorMinerador:
    """Sistema de agendamento para execução automática do minerador"""
    
    def __init__(self):
        self.minerador = Minerador()
        self.running = False
        self.job_thread = None
        self.current_job = None
        
        # Configura handlers de sinal para graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handler para sinais de interrupção"""
        logger.info(f"Sinal recebido: {signum}. Finalizando agendador...")
        self.parar()
        sys.exit(0)
    
    def iniciar(self):
        """Inicia o sistema de agendamento"""
        logger.info("Iniciando sistema de agendamento...")
        
        try:
            # Configura jobs agendados
            self._configurar_jobs()
            
            # Inicia thread de execução
            self.running = True
            self.job_thread = threading.Thread(target=self._executar_agendador)
            self.job_thread.daemon = True
            self.job_thread.start()
            
            logger.info("Sistema de agendamento iniciado com sucesso")
            logger.info(f"Próxima execução programada para: {self._proxima_execucao()}")
            
            # Execução imediata para teste
            self.executar_mineracao_agendada()
            
        except Exception as e:
            logger.error(f"Erro ao iniciar agendador: {str(e)}")
            raise
    
    def _configurar_jobs(self):
        """Configura os jobs agendados"""
        # Job principal - execução a cada hora
        schedule.every(Config.AGENTE_INTERVALO).seconds.do(
            self.executar_mineracao_agendada
        )
        
        # Job de limpeza diária - remove arquivos antigos
        schedule.every().day.at("02:00").do(
            self.limpar_arquivos_antigos
        )
        
        # Job de estatísticas diárias
        schedule.every().day.at("06:00").do(
            self.gerar_estatisticas_diarias
        )
        
        logger.info("Jobs configurados com sucesso")
    
    def _executar_agendador(self):
        """Loop principal do agendador"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Erro no loop do agendador: {str(e)}")
                time.sleep(5)  # Delay antes de tentar novamente
    
    def executar_mineracao_agendada(self):
        """Executa mineração agendada"""
        try:
            logger.info("Executando mineração agendada...")
            
            # Verifica se já há uma execução em andamento
            if self.current_job and self.current_job.is_alive():
                logger.warning("Mineração anterior ainda em execução. Aguardando...")
                return
            
            # Inicia nova execução em thread separada
            self.current_job = threading.Thread(
                target=self._executar_mineracao_thread
            )
            self.current_job.daemon = True
            self.current_job.start()
            
            logger.info("Mineração agendada iniciada em thread separada")
            
        except Exception as e:
            logger.error(f"Erro ao executar mineração agendada: {str(e)}")
    
    def _executar_mineracao_thread(self):
        """Executa mineração em thread separada"""
        try:
            start_time = datetime.now()
            logger.info(f"Iniciando mineração agendada - {start_time}")
            
            # Executa mineração automática
            resultados = self.minerador.executar_mineracao_automatica()
            
            end_time = datetime.now()
            duracao = end_time - start_time
            
            logger.info(f"Mineração agendada concluída em {duracao.total_seconds():.1f} segundos")
            logger.info(f"Resultados obtidos: {len(resultados)} execuções")
            
            # Log de sucesso
            self._log_execucao_sucesso(start_time, end_time, resultados)
            
        except Exception as e:
            logger.error(f"Erro na execução da mineração agendada: {str(e)}")
            self._log_execucao_erro(str(e))
    
    def _log_execucao_sucesso(self, start_time, end_time, resultados):
        """Registra log de execução bem-sucedida"""
        log_entry = {
            'tipo': 'execucao_agendada',
            'status': 'sucesso',
            'inicio': start_time.isoformat(),
            'fim': end_time.isoformat(),
            'duracao_segundos': (end_time - start_time).total_seconds(),
            'resultados': len(resultados),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Execução agendada registrada: {log_entry}")
    
    def _log_execucao_erro(self, erro):
        """Registra log de execução com erro"""
        log_entry = {
            'tipo': 'execucao_agendada',
            'status': 'erro',
            'erro': erro,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.error(f"Execução agendada com erro: {log_entry}")
    
    def limpar_arquivos_antigos(self):
        """Job de limpeza de arquivos antigos"""
        try:
            logger.info("Iniciando limpeza de arquivos antigos...")
            
            arquivos_removidos = self.minerador.limpar_arquivos_antigos(dias=30)
            
            logger.info(f"Limpeza concluída: {arquivos_removidos} arquivos removidos")
            
        except Exception as e:
            logger.error(f"Erro na limpeza de arquivos: {str(e)}")
    
    def gerar_estatisticas_diarias(self):
        """Job de geração de estatísticas diárias"""
        try:
            logger.info("Gerando estatísticas diárias...")
            
            stats = self.minerador.obter_estatisticas()
            
            # Salva estatísticas
            self._salvar_estatisticas_diarias(stats)
            
            logger.info("Estatísticas diárias geradas com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao gerar estatísticas: {str(e)}")
    
    def _salvar_estatisticas_diarias(self, stats):
        """Salva estatísticas diárias em arquivo"""
        try:
            from utils.file_handler import FileHandler
            file_handler = FileHandler()
            
            timestamp = datetime.now().strftime('%Y%m%d')
            filename = f"estatisticas_diarias_{timestamp}.json"
            
            import json
            json_path = file_handler.storage_path / 'Outros' / filename
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"Estatísticas salvas: {json_path}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar estatísticas: {str(e)}")
    
    def executar_mineracao_manual(self, porte, estado, nicho):
        """Executa mineração manual com parâmetros específicos"""
        try:
            logger.info(f"Executando mineração manual: {porte}, {estado}, {nicho}")
            
            resultado = self.minerador.executar_mineracao(porte, estado, nicho)
            
            logger.info("Mineração manual concluída com sucesso")
            return resultado
            
        except Exception as e:
            logger.error(f"Erro na mineração manual: {str(e)}")
            return None
    
    def obter_status(self):
        """Retorna status atual do agendador"""
        return {
            'running': self.running,
            'proxima_execucao': self._proxima_execucao(),
            'jobs_agendados': len(schedule.get_jobs()),
            'thread_ativa': self.job_thread.is_alive() if self.job_thread else False,
            'mineracao_em_andamento': self.current_job.is_alive() if self.current_job else False,
            'timestamp': datetime.now().isoformat()
        }
    
    def _proxima_execucao(self):
        """Retorna próxima execução programada"""
        try:
            next_run = schedule.next_run()
            if next_run:
                return next_run.isoformat()
            return "Nenhuma execução programada"
        except:
            return "Erro ao obter próxima execução"
    
    def parar(self):
        """Para o sistema de agendamento"""
        logger.info("Parando sistema de agendamento...")
        
        self.running = False
        
        # Aguarda thread principal finalizar
        if self.job_thread and self.job_thread.is_alive():
            self.job_thread.join(timeout=5)
        
        # Aguarda job atual finalizar
        if self.current_job and self.current_job.is_alive():
            self.current_job.join(timeout=10)
        
        # Limpa jobs agendados
        schedule.clear()
        
        logger.info("Sistema de agendamento parado")
    
    def reiniciar(self):
        """Reinicia o sistema de agendamento"""
        logger.info("Reiniciando sistema de agendamento...")
        
        self.parar()
        time.sleep(2)
        self.iniciar()
        
        logger.info("Sistema de agendamento reiniciado")
    
    def aguardar_execucao(self):
        """Aguarda até a próxima execução programada"""
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Interrupção recebida pelo usuário")
            self.parar()
