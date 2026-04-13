"""
Logging estructurado con JSON para producción.
"""
import logging
import json
import sys
from datetime import datetime
from typing import Any, Optional


class JSONFormatter(logging.Formatter):
    """
    Formatter que serializa logs en JSON con contexto.
    Útil para Cloud logging (Railway, Datadog, CloudWatch, etc.)
    """
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Agregar contexto extra (user_id, ip, duration_ms, etc)
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "ip"):
            log_data["ip"] = record.ip
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, "error_code"):
            log_data["error_code"] = record.error_code
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        # Stack trace si hay excepción
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, default=str)


def _create_logger(name: str) -> logging.Logger:
    """Crea logger con handler JSON a stdout."""
    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(logging.INFO)
    
    # Handler stdout (para Railway, Vercel, Docker, etc)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    # Formatter JSON
    formatter = JSONFormatter()
    handler.setFormatter(formatter)
    
    logger_instance.addHandler(handler)
    logger_instance.propagate = False
    
    return logger_instance


# Logger global para la app
logger = _create_logger("jwt_api")
