from loguru import logger
from pathlib import Path
import sys

def setup_logger(log_dir: str = "logs") -> None:
    """
    Configure le logger global loguru avec toutes les options professionnelles.
    """
    # Vider les anciens fichiers (pour overwrite)
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    open(f"{log_dir}/app.log", "w").close()
    open(f"{log_dir}/error.log", "w").close()
    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # Paramètres communs (console et fichier)
    base_params = {
        "format": log_format,
        "enqueue": True,
        "backtrace": True,
        "diagnose": True,
    }

    # Console
    logger.add(
        sink=sys.stdout,
        level="DEBUG",
        colorize=True,
        **base_params,
    )

    # Paramètres fichiers
    file_params = {
        **base_params,
        "rotation": "10 MB",
        "retention": "7 days",
        "compression": "zip",
        "encoding": "utf-8",
        "colorize": False,
    }

    # Fichier général
    logger.add(
        sink=f"{log_dir}/app.log",
        level="DEBUG",
        **file_params,
    )

    # Fichier uniquement erreurs
    logger.add(
        sink=f"{log_dir}/error.log",
        level="ERROR",
        **file_params,
    )

    # Attraper toutes les exceptions non gérées globalement
    def log_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.opt(exception=(exc_type, exc_value, exc_traceback)).critical("Exception non gérée")

    sys.excepthook = log_exception

# Setup automatique
setup_logger()

__all__ = ["logger"]