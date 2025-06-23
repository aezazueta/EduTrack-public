"""
Utilidades para la carga y manejo de configuraciones del proyecto
"""
import yaml
import os
from typing import Dict, Any
from pydantic import BaseModel, FilePath
from pathlib import Path

class PreprocessConfig(BaseModel):
    """Configuración para el preprocesamiento de datos.
    
    Attributes:
        input_path: Directorio que contiene los archivos de entrada
        output_path: Directorio donde se guardarán los archivos procesados
        files: Configuración de los archivos de entrada
    """
    input_path: str
    output_path: str
    version: str
    files: Dict[str, str]

def load_config(config_path: str) -> Dict[str, Any]:
    """Carga la configuración desde un archivo YAML.
    
    Args:
        config_path: Ruta al archivo de configuración YAML
        
    Returns:
        Dict[str, Any]: Diccionario con la configuración
        
    Raises:
        FileNotFoundError: Si el archivo de configuración no existe
        yaml.YAMLError: Si hay errores en el formato YAML
    """
    from src.utils.logging_utils import config_logging
    logger = config_logging()
    
    logger.info(f"📂 Cargando configuración desde: {config_path}")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = yaml.safe_load(f)
            
        #logger.debug(f"🔍 Configuración cargada: {config_dict}")
        logger.info("✅ Configuración cargada exitosamente")
        
        return config_dict
        
    except FileNotFoundError:
        logger.error(f"❌ Archivo de configuración no encontrado: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"❌ Error en formato YAML: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"❌ Error inesperado al cargar configuración: {str(e)}")
        raise