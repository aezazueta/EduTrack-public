import logging
import pandas as pd
import os
from typing import Union, Optional
from src.utils import config_logging

logger = logging.getLogger(__name__)

class dataRaw2DF:
    """
    Clase auxiliar utilizada para manejar las conversiones de archivos en hojas de calculo
    a DataFrames. Soporta archivos CSV, XLS y XLSX.
    """

    @staticmethod
    def to_dataframe(
        file: Any,
        sheet_name: Optional[Union[str, int]] = 0,
        encoding: str = 'utf-8',
        **kwargs
    ) -> Tuple[bool, pd.DataFrame]:
        """
            Convierte un archivo de hoja de cálculo a DataFrame.
            
            Args:
                file_name (str): Nombre del archivo a convertir
                file_ext (str): Extensión del archivo a convertir
                sheet_name (Union[str, int], optional): Nombre o índice de la hoja a leer. Por defecto 0
                encoding (str, optional): Codificación del archivo. Por defecto 'utf-8'
                **kwargs: Argumentos adicionales para pd.read_csv o pd.read_excel
                
            Returns:
                pd.DataFrame: DataFrame con los datos del archivo
                
            Raises:
                FileNotFoundError: Si el archivo no existe
                ValueError: Si el formato del archivo no es soportado
        """
        file_name = file.name
        file_ext = file_name.split(".")[-1].lower()
        try:
            if file_ext == '.csv':
                logger.info(f'🔍 Leyendo archivo CSV: {file_path}')
                return True, pd.read_csv(file_path, encoding=encoding, **kwargs)
            
            elif file_ext in ['xls', 'xlsx']:
                logger.info(f'🔍 Leyendo archivo EXCEL: {file_path}')
                return True, pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
            else:
                raise ValueError('Formato de archivo no soportado.')
                return False, None
        except Exception as e:
            logger.error(f"❌ Error al convertir el archivo {file_path}: {str(e)}")
            raise
            return False, None
