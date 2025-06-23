from ast import Call
#from curses import wrapper
import logging
import os
from datetime import datetime
from typing import Optional, Callable
from functools import wraps

from numpy.lib.scimath import log
from pyarrow import timestamp

def config_logging(
    log_dir: str = 'logs',
    log_level: int = logging.INFO,
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    include_console: bool = True
) -> logging.Logger:
    """
    Configura el sistema de logging del proyecto.

    Args:
        log_dir (str): Directorio donde se guardarán los logs.
        log_level (int): Nivel de logging (default: logging.INFO).
        log_format (str): Formato de los mensajes de log.

    Returns:
        logging.Logger: Logger configurado.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Formato de nombres de archivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'edutrack_{timestamp}.log')

    # Configuracion logger
    logger = logging.getLogger('EduTrack')
    
    # Evitar duplicación de handlers
    if logger.handlers:
        return logger
        
    logger.setLevel(log_level)
    
    # Configuracion de formato
    formatter = logging.Formatter(log_format)

    # Configuracion del handler para los archivos log
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if (include_console):
        # configuracion del handler para la consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    #retorno del obj logger ya bien configuradito
    return logger

def log_function(logger: Optional[logging.Logger] = None) -> Callable:
    """
    Decorador para registrar la ejecución de funciones.

    Args:
        logger (Optional[logging.Logger]): Logger a utilizar. Si es None, se crea uno nuevo.

    Returns:
        Callable: Decorador que registra la ejecución de la función.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Usar el logger existente
            log = logger or logging.getLogger('EduTrack')

            # Registro del inicio de la función
            log.info(f'Iniciando ejecución de {func.__name__}')

            try:
                result = func(*args, **kwargs)
                log.info(f'✅ Función {func.__name__} ejecutandose exitosamente')
                return result
            except Exception as e:
                log.error(f'❌ Ocurrió un error en {func.__name__}: {str(e)}')
                raise
        return wrapper
    return decorator
