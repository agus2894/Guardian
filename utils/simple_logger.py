import logging
import os
import json
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, Optional

class SimpleGuardianLogger:

    def __init__(self):
        self.log_dir = "logs"
        self.ensure_log_directory()
        self.setup_logger()

    def ensure_log_directory(self):
        """Crear directorio de logs si no existe"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def setup_logger(self):
        """Configurar un solo logger unificado"""
        self.logger = logging.getLogger('guardian')
        self.logger.setLevel(logging.INFO)

        if self.logger.handlers:
            return

        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'guardian.log'),
            maxBytes=5*1024*1024,  # 5MB (más pequeño)
            backupCount=3  # Solo 3 backups (menos archivos)
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _log(self, level: str, category: str, message: str, **kwargs):
        """Método interno unificado para logging"""
        log_data = {
            "category": category,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }

        log_message = json.dumps(log_data, ensure_ascii=False, default=str)

        if level == "INFO":
            self.logger.info(log_message)
        elif level == "WARNING":
            self.logger.warning(log_message)
        elif level == "ERROR":
            self.logger.error(log_message)
        elif level == "CRITICAL":
            self.logger.critical(log_message)

    def info(self, message: str, **kwargs):
        self._log("INFO", "APP", message, **kwargs)

    def warning(self, message: str, **kwargs):
        self._log("WARNING", "APP", message, **kwargs)

    def error(self, message: str, **kwargs):
        self._log("ERROR", "APP", message, **kwargs)

    def security(self, message: str, severity: str = "warning", **kwargs):
        level = "CRITICAL" if severity == "critical" else "ERROR" if severity == "high" else "WARNING"
        self._log(level, "SECURITY", message, severity=severity, **kwargs)

    def network(self, message: str, **kwargs):
        self._log("INFO", "NETWORK", message, **kwargs)

    def auth(self, message: str, success: bool = True, **kwargs):
        level = "INFO" if success else "WARNING"
        self._log(level, "AUTH", message, success=success, **kwargs)

class SimpleMetricsCollector:
    def __init__(self):
        self.logger = SimpleGuardianLogger()

    def record(self, metric_type: str, action: str, value: Any = 1, **metadata):
        self.logger.info(
            f"Metric recorded: {metric_type}.{action}",
            metric_type=metric_type,
            action=action,
            value=value,
            **metadata
        )

simple_logger = SimpleGuardianLogger()
simple_metrics = SimpleMetricsCollector()
