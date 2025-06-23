import pandas as pd
import numpy as np
import math
import os
from src.utils import load_config
from src.utils.logging_utils import config_logging
from src.utils.config_utils import PreprocessConfig
import logging

main_path = os.path.dirname(os.path.abspath(__file__))
logger = config_logging()

def load_data(path_dalumn, path_dcalum, path_dkarde):
    """Carga los archivos de datos iniciales y valida que contengan las columnas necesarias.
    
    Args:
        path_dalumn: Ruta al archivo CSV con datos de alumnos
        path_dcalum: Ruta al archivo CSV con datos académicos
        path_dkarde: Ruta al archivo CSV con datos de calificaciones
        
    Returns:
        tuple: (df_cal, df_alumn, df_dcalumn) DataFrames con los datos cargados y validados
        
    Raises:
        ValueError: Si algún archivo no contiene las columnas requeridas
    """
    logger.info("🔄 Iniciando carga de archivos de datos")
    # Definir columnas requeridas para cada DataFrame
    cols_dkarde = ['aluctr', 'matcve', 'karcal', 'tcacve']
    cols_dalumn = ['aluctr', 'aluapp', 'aluapm', 'alunom', 'alurfc', 'alucur', 'aluseg',
                   'alunac', 'alusex', 'alulna', 'alumun', 'aluesc', 'aluegr', 'aluescp',
                   'alucpo', 'alusme', 'alueci', 'aluare', 'alupadv', 'alumadv', 'alutcp',
                   'alutra', 'alulexp', 'alutecpo', 'alupexani', 'discve', 'alucen']
    cols_dcalum = ['aluctr', 'carcve', 'placve', 'espcve', 'caling', 'calter', 'calsit',
                   'calnpe', 'calgpo', 'calcac', 'calnpec', 'calobs', 'caltcala', 'caltcalr',
                   'calmata', 'calmat', 'calmatac', 'calpri', 'calnpep', 'calingt', 'calingi']
    # Definir tipos de datos para dkarde que pandas podría mal interpretar
    dtypes_dict = {
        'aluctr': 'object', 
        'mat_cve': object,
        'karcal': 'Int64',
        'tcacve': 'Int64',
        'pdocve1': 'Int64',
        'karnpe1': object
    }
    logger.info("📂 Cargando archivo de calificaciones...")
    try:
        df_cal = pd.read_csv(path_dkarde, dtype=dtypes_dict)
        logger.info(f"✅ Archivo de calificaciones cargado exitosamente - {len(df_cal)} registros")
    except Exception as e:
        logger.error(f"❌ Error al cargar archivo de calificaciones: {str(e)}")
        raise
    logger.info("📂 Cargando archivo de datos personales...")
    try:
        df_alumn = pd.read_csv(path_dalumn, encoding='latin1')
        logger.info(f"✅ Archivo de datos personales cargado exitosamente - {len(df_alumn)} registros")
    except Exception as e:
        logger.error(f"❌ Error al cargar archivo de datos personales: {str(e)}")
        raise
    logger.info("📂 Cargando archivo de datos académicos...")
    try:
        df_dcalumn = pd.read_csv(path_dcalum, encoding='latin1')
        logger.info(f"✅ Archivo de datos académicos cargado exitosamente - {len(df_dcalumn)} registros")
    except Exception as e:
        logger.error(f"❌ Error al cargar archivo de datos académicos: {str(e)}")
        raise
    # Validar columnas en df_cal
    logger.info("🔍 Validando columnas requeridas en archivo de calificaciones...")
    missing_cols_cal = set(cols_dkarde) - set(df_cal.columns)
    if missing_cols_cal:
        error_msg = f"Faltan las siguientes columnas en el archivo de calificaciones: {missing_cols_cal}"
        logger.error(f"❌ {error_msg}")
        raise ValueError(error_msg)
    logger.info("✅ Todas las columnas requeridas presentes en archivo de calificaciones")
    # Validar columnas en df_alumn
    logger.info("🔍 Validando columnas requeridas en archivo de datos personales...")
    missing_cols_alumn = set(cols_dalumn) - set(df_alumn.columns)
    if missing_cols_alumn:
        error_msg = f"Faltan las siguientes columnas en el archivo de datos personales: {missing_cols_alumn}"
        logger.error(f"❌ {error_msg}")
        raise ValueError(error_msg)
    logger.info("✅ Todas las columnas requeridas presentes en archivo de datos personales")
    # Validar columnas en df_dcalumn
    logger.info("🔍 Validando columnas requeridas en archivo de datos académicos...")
    missing_cols_dcalumn = set(cols_dcalum) - set(df_dcalumn.columns)
    if missing_cols_dcalumn:
        error_msg = f"Faltan las siguientes columnas en el archivo de datos académicos: {missing_cols_dcalumn}"
        logger.error(f"❌ {error_msg}")
        raise ValueError(error_msg)
    logger.info("✅ Todas las columnas requeridas presentes en archivo de datos académicos")
    logger.info("✨ Carga y validación de archivos completada exitosamente")
    return df_cal, df_alumn, df_dcalumn

def process_grades(df_cal):
    """Procesa las calificaciones y materias del dataframe.
    
    Args:
        df_cal (pd.DataFrame): DataFrame con las calificaciones de los alumnos.
        
    Returns:
        pd.DataFrame: DataFrame con las calificaciones procesadas y estandarizadas.
        
    Note:
        - Estandariza las claves de materias eliminando espacios
        - Filtra solo materias de tronco común
        - Mapea los códigos de materias a nombres más descriptivos
        - Elimina registros duplicados manteniendo el último
    """
    logger.info("🔄 Iniciando procesado de calificaciones")
    # estandarización de las claves de las materias
    df_cal['matcve'] = df_cal['matcve'].str.replace(" ", "")
    materias_tronco_comun = ['ACC-0906', 'ACA-0907', 'ACF-0901', 'ACF-0902', 'ACF-0903', 'AEC-1053',
                         'AEC-1081', 'AEF-1052', 'ASF-1010', 'GED-0921', 'INC-1025', 'GEF-0910',
                         'AEF-1056', 'AEC-1058', 'ALF-1021', 'GEF-0929', 'GEF-0914', 'ALF-1022', 'ALC-1020']
    # filtrado de materias de tronco común necesarias para el modelo
    df_cal = df_cal[df_cal['matcve'].isin(materias_tronco_comun)] 
    # Mapeo directo de materias (más eficiente)
    materia_mapping = {
        'AEC-1053': 'Estad', 'AEC-1081': 'Estad', 'AEF-1052': 'Estad', 'ASF-1010': 'Estad', 'GED-0921': 'Estad', 'GEF-0929': 'Estad', 
        'ALC-1020': 'Estad', 'INC-1025': 'Quim', 'GEF-0910': 'Quim', 'AEF-1056': 'Quim', 'AEC-1058': 'Quim', 'ALF-1021': 'Quim', 
        'GEF-0914': 'Quim', 'ALF-1022': 'Quim', 'ACF-0903': 'Algb_Lin', 'ACF-0902': 'Calc_Int', 'ACF-0901': 'Calc_Dif',
        'ACA-0907': 'Etica', 'ACC-0906': 'Fund_Inv'
    }
    df_cal['matcve'] = df_cal['matcve'].map(materia_mapping)
    # Eliminar duplicados manteniendo el último registro
    df_cal = df_cal.drop_duplicates(subset=['aluctr', 'matcve'], keep='last')
    logger.info("✅  Procesado de calificaciones completado!")
    return df_cal

def merge_dataframes(df_cal, df_alumn, df_dcalumn):
    """Combina los dataframes de calificaciones y datos de alumnos.
    
    Args:
        df_cal (pd.DataFrame): DataFrame con calificaciones
        df_alumn (pd.DataFrame): DataFrame con datos personales de alumnos
        df_dcalumn (pd.DataFrame): DataFrame con datos académicos
        
    Returns:
        pd.DataFrame: DataFrame combinado con todos los datos fusionados
        
    Note:
        - Elimina columnas no necesarias
        - Pivotea las calificaciones por materia
        - Pivotea los tipos de calificación por materia
        - Fusiona los dataframes usando el ID del alumno
    """
    logger.info("🔄 Iniciando fusión de dataframes")
    # Eliminar columnas no necesarias de df_alumn
    #df_alumn = df_alumn.drop(columns=['aluapp', 'aluapm', 'alunom', 'alurfc','alucur', 'aluseg'])
    df_alumn = df_alumn.drop(columns=['alurfc','alucur', 'aluseg'])
    # Pivotear calificaciones
    df_cal_pivot = df_cal.pivot(index='aluctr', columns=['matcve'], values='karcal')
    df_cal_pivot = df_cal_pivot.reset_index()
    # Pivoteo de tipos de calificación por materia
    df_calcve_pivot = df_cal.pivot(index='aluctr', columns='matcve', values='tcacve')
    df_calcve_pivot.columns = [f"{col}_calcve" for col in df_calcve_pivot.columns]
    df_calcve_pivot = df_calcve_pivot.reset_index()
    # Fusion de dataframes pivoteados y reordenamiento de columnas
    df_pivots_temp = pd.merge(df_cal_pivot, df_calcve_pivot, on='aluctr', how='inner')
    df_pivots_temp = df_pivots_temp.reindex(['aluctr','Algb_Lin', 'Algb_Lin_calcve','Calc_Dif', 'Calc_Dif_calcve','Calc_Int', 'Calc_Int_calcve',
                        'Estad', 'Estad_calcve', 'Fund_Inv', 'Fund_Inv_calcve', 'Quim', 'Quim_calcve',
                        'Etica', 'Etica_calcve'], axis=1)
    # Eliminacion de duplicados de df_dcalumn
    df_dcalumn = df_dcalumn.drop_duplicates(subset=['aluctr'], keep='last')
    # Fusion de dataframes de datos de alumnos
    df_main = pd.merge(df_dcalumn, df_alumn, on='aluctr', how='left')
    # Se eliminan duplicados de df_main
    df_main = df_main.drop_duplicates(subset=['aluctr'], keep='last')
    # Fusion de dataframes de datos de alumnos y calificaciones
    df_main = df_main.merge(df_pivots_temp, on='aluctr', how='inner')
    logger.info("✅ Fusión de dataframes completada!")
    return df_main

def filter_order_data(df_main):
    """Filtra y reordena los datos del dataframe principal.
    
    Args:
        df_main (pd.DataFrame): DataFrame principal con todos los datos
        
    Returns:
        pd.DataFrame: DataFrame filtrado y reordenado
        
    Note:
        - Filtra solo alumnos de 3er semestre en adelante
        - Mueve la variable dependiente (abandono) al final
    """
    logger.info("🔄 Comienza filtrado de datos (3er semestre en adelante)")
    # Filtro solo alumnos de 3er semestre cursado en adelante
    df_main = df_main[df_main['calnpe'] >= 3]
    # Se mueve la variable dependiente al final del dataframe
    dependient_var = df_main.pop("calsit")
    df_main.insert(loc=len(df_main.columns), column="abandono", value=dependient_var)
    logger.info("✅ Filtrado de datos completado!")
    return df_main

def handle_miss_matVals(df_main):
    """Maneja los valores faltantes en materias y sus claves.
    
    Args:
        df_main (pd.DataFrame): DataFrame principal
        
    Returns:
        pd.DataFrame: DataFrame con valores faltantes tratados
        
    Note:
        - Rellena valores faltantes en materias con -1
        - Rellena valores faltantes en claves de materia con -2
    """
    # Relleno de valores faltantes en materias y claves de materia (-1 y -2 respectivamente)
    logger.info("🔄 Rellenando valores faltantes en materias y claves de materia")
    materias = ['Algb_Lin', 'Calc_Dif', 'Calc_Int', 'Estad',
        'Fund_Inv', 'Quim', 'Etica']
    mat_claves = ['Algb_Lin_calcve', 'Calc_Dif_calcve', 'Calc_Int_calcve', 'Estad_calcve',
            'Fund_Inv_calcve', 'Quim_calcve', 'Etica_calcve']
    df_main[materias] = df_main[materias].fillna(-1)
    df_main[mat_claves] = df_main[mat_claves].fillna(-2)
    logger.info("✅ Proceso terminado.")
    return df_main

def drop_useless_cols(df_main):
    """Elimina columnas no útiles para el modelo.
    
    Args:
        df_main (pd.DataFrame): DataFrame principal
        
    Returns:
        pd.DataFrame: DataFrame sin las columnas eliminadas
        
    Note:
        - Elimina columnas con más del 15% de valores nulos
        - Elimina columnas con varianza 0
        - Elimina columnas irrelevantes para el modelo
    """
    logger.info("🔄 Eliminando columnas no útiles para el modelo")
    # Eliminación de columnas con más del 15% de valores nulos
    useless_cols = ['extcve', 'calter', 'calgpo', 'calobs', 'peerson', 'alute1', 'alute2', 'alumaii', 
    'alusmei', 'alusmea', 'alutsa', 'alupad', 'alupadt', 'alumadt', 'alutno', 'alutcl', 'alutnu', 
    'alutco', 'alutmu', 'alutci', 'alutte1', 'alutte2', 'alutmai', 'alufac', 'alutwi', 'alutce', 
    'alupasc', 'aluteotr', 'alutecll', 'alutenum', 'alutecol', 'aluteciu', 'alutemun', 'alutetel', 
    'alutepto', 'aluale', 'alupsi','aluoest', 'aluotra', 'alutinl', 'alutpot', 'alutsec']
    df_main = df_main.drop(columns=useless_cols)
    # Descarte de variables con varianza 0 y datos irrelevantes para el modelo
    drop_cols = ['siscve', 'calplai', 'alulare', 'alulfde', 'alulfha', 'lincve', 'aluteanp', 
    'aluteotrt', 'aludch', 'calcari', 'id', 'aluescpd', 'aluescpa', 'alulemp', 'tbecve', 'aluest', 
    'alupes', 'gincve', 'aluteing', 'alupegel', 'aluptoefl', 'cve', 'alucll', 'alunum', 'alucol', 
    'aluciu','alumad', 'alumai', 'alupas']
    df_main = df_main.drop(columns=drop_cols)
    logger.info("✅ Purga de columnas innecesarias terminada.")
    return df_main

def change_dtypes(df_main):
    """Cambia y ajusta los tipos de datos de las columnas.
    
    Args:
        df_main (pd.DataFrame): DataFrame principal
        
    Returns:
        pd.DataFrame: DataFrame con tipos de datos ajustados
        
    Note:
        - Convierte columnas a tipo Int64 preservando nulos
        - Convierte valores en blanco a nulos
        - Maneja casos especiales como asteriscos
        - Ajusta valores específicos en algunas columnas
    """
    #cambio de tipo de dato de columnas conservando los valores nulos, esos se tratarán después
    logger.info("🔄 Ajustando tipos de datos de columnas")
    change_dtypes = ['aluesc', 'alusex', 'aluegr', 'aluescp', 'discve', 'alulna', 'alucpo', 'alumun', 'alutra', 'alucen', 'placve', 'caling', 'alutecpo', 'alupexani']
    for col in change_dtypes:
        df_main[col] = df_main[col].astype('Int64')
    # Conversión de valores en blanco por nulos y reemplazo de valores extraños
    try:
            data_to_int = ['espcve', 'aluare', 'alusme', 'alueci']
            for col in data_to_int:
                # Primero se hace reemplazo y conversion a float por que no se puede hacer la conversion directa a Int64
                df_main[col] = df_main[col].replace(' ', np.nan).astype(float)
                df_main[col] = df_main[col].astype('Int64')
    except Exception as e:
        logger.error(f"Error al convertir columnas a Int64: {e}")
    # tratamiento independiente a variable 'alutcp' por tener entradas con asteriscos ('*****')
    df_main['alutcp'] = df_main['alutcp'].replace('*****', '0')
    df_main['alutcp'] = df_main['alutcp'].astype('Int64')
    df_main['alutcp'] = df_main['alutcp'].fillna(0)
    # Ajuste de variable 'calingt' para reemplazar valor " " a "N" (normal)
    df_main['calingt'] = df_main['calingt'].replace(' ', 'N')
    logger.info("✅ Ajuste de tipos de datos de columnas completado.")
    return df_main
    
def handle_location_codes(df_main, loc_codes):
    """Procesa y mapea los códigos de ubicación.
    
    Args:
        df_main (pd.DataFrame): DataFrame principal
        loc_codes (pd.DataFrame): DataFrame con códigos de ubicación
        
    Returns:
        pd.DataFrame: DataFrame con ubicaciones procesadas
        
    Note:
        - Separa códigos de ubicación en estado y municipio
        - Fusiona con catálogo de ubicaciones
        - Renombra columnas resultantes
        - Elimina columnas intermedias
    """
    logger.info("🔄 Procesando códigos de ubicación.")
    # Validar campos requeridos en loc_codes
    required_fields = ['muncve', 'estcve', 'munnom', 'estnom']
    missing_fields = [campo for campo in required_fields if campo not in loc_codes.columns]
    
    if missing_fields:
        error_msg = f"❌ Faltan los siguientes campos requeridos en el DataFrame de códigos de ubicación: {missing_fields}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    code_municip = []
    code_state = []
    df_main['alulna'] = df_main['alulna'].astype(str)
    df_main['alumun'] = df_main['alumun'].astype(str)

    logger.info("🔍 Separando códigos de ubicación.")
    def separa_codigos(codigo):
        """Función que separa el código de 5 o 4 dígitos en
        dos nuevos códigos de municipio y estado, respectivamente
        y los agrega a las listas correspondientes

        Args:
            codigo (str): código de 5 o 4 dígitos
        """
        if len(codigo) == 5:
            code_state.append(codigo[:2])
            code_municip.append(codigo[2:])
        elif len(codigo) == 4:
            if codigo == '<NA>':
                code_state.append(np.nan)
                code_municip.append(np.nan)
            else:
                code_state.append(codigo[:2])
                code_municip.append(codigo[2:])
        else:
            print(f"Código de ubicación inválido: {codigo}")
            code_state.append(np.nan)
            code_municip.append(np.nan)
    try:
        logger.info('🔍 Decodificando codigos de alulna...')
        df_main['alulna'].apply(separa_codigos)
    except Exception as e:
        logger.error(f"❌ Error al decodificar codigos de alulna: {e}")
    # insertando variables nuevas al dataframe
    try:
        logger.info('🔍 Anexando nuevas variables')
        df_main.insert(df_main.columns.get_loc('alulna')+1,"alulna_est", code_state)
        df_main.insert(df_main.columns.get_loc('alulna')+2,"alulna_mun", code_municip)
    except Exception as e:
        logger.error(f"❌ Error al anexar nuevas variables: {e}")
    # Reseteo de listas para volverlas a usar en otra columna
    del code_state[:]
    del code_municip[:]
    try:
        logger.info('🔍 Decodificando codigos de alumun...')
        df_main['alumun'].apply(separa_codigos)
    except Exception as e:
        logger.error(f"❌ Error al decodificar codigos de alumun: {e}")
    # insertando variables nuevas al dataframe
    try:
        logger.info('🔍 Anexando nuevas variables')
        df_main.insert(df_main.columns.get_loc('alumun')+1,"alumun_est", code_state)
        df_main.insert(df_main.columns.get_loc('alumun')+2,"alumun_mun", code_municip)
    except Exception as e:
        logger.error(f"❌ Error al anexar nuevas variables: {e}")

    # Cambiando tipo de datos de las nuevas columnas
    for col in ['alulna_est', 'alulna_mun', 'alumun_est', 'alumun_mun']:
        df_main[col] = df_main[col].astype('Int64')
    print('ok')        
    # Eliminando columnas originales
    print(f'Eliminando columnas originales [alulna, alumun]')
    df_main = df_main.drop(columns=['alulna', 'alumun'])
    print('ok')
    # Fusionar dataframe principal con códigos de municipio y estado de nacimiento
    df_main = df_main.merge(loc_codes, left_on=['alulna_mun', 'alulna_est'], right_on=['muncve', 'estcve'], how='left')
    # Renombrar nuevas columnas categóricas
    df_main = df_main.rename(columns={'munnom':'alu_nac_mun', 'estnom':'alu_nac_est'})
    # Eliminar columnas con códigos numéricos que ya no se usarán
    df_main = df_main.drop(columns=['muncve', 'estcve', 'cve', 'alulna_est', 'alulna_mun'])
    # Fusionar dataframe principal con códigos de municipio y estado de vivienda
    df_main = df_main.merge(loc_codes, left_on=['alumun_mun', 'alumun_est'], right_on=['muncve', 'estcve'], how='left')
    # Renombrar nuevas columnas categóricas
    df_main = df_main.rename(columns={'munnom':'alu_dir_mun', 'estnom':'alu_dir_est'})
    # Eliminar columnas con códigos numericos que ya no se usarán
    df_main = df_main.drop(columns=['muncve', 'estcve', 'cve', 'alumun_mun', 'alumun_est'])
    logger.info("✅ Proceso de códigos de ubicación completado.")   
    return df_main

def handle_school_codes(df_main, school_codes):
    """Mapea los códigos de escuelas a sus nombres.
    
    Args:
        df_main (pd.DataFrame): DataFrame principal
        school_codes (pd.DataFrame): DataFrame con códigos de escuelas
        
    Returns:
        pd.DataFrame: DataFrame con nombres de escuelas mapeados
    """
    logger.info("🔄 Procesando códigos de escuelas.")
    # Validar campos requeridos en school_codes
    required_fields = ['esccve', 'escnomcto']
    missing_fields = [campo for campo in required_fields if campo not in school_codes.columns]
    
    if missing_fields:
        error_msg = f"❌ Faltan los siguientes campos requeridos en el DataFrame de códigos de escuelas: {missing_fields}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    try:
        schools_dict = school_codes.set_index('esccve')['escnomcto'].to_dict()
        df_main['aluesc'] = df_main['aluesc'].map(schools_dict)
    except Exception as e:
        logger.error(f"❌ Error al mapear códigos de escuelas: {e}")
    logger.info("✅ Proceso de códigos de escuelas completado.")
    return df_main

def handle_course_esp_plan(df_main, df_plan_codes, df_esp_codes):
    """Procesa las variables de especialidad y plan de estudios.
    
    Args:
        df_main (pd.DataFrame): DataFrame principal
        df_plan_codes (pd.DataFrame): DataFrame con códigos de planes
        df_esp_codes (pd.DataFrame): DataFrame con códigos de especialidades
        
    Returns:
        pd.DataFrame: DataFrame con especialidades y planes procesados
        
    Note:
        - Llena valores faltantes en especialidad
        - Mapea códigos de plan de estudios
        - Mapea códigos de especialidad
    """
    logger.info("🔄 Procesando variables de especialidad y plan de estudios.")
    # Validar campos requeridos en df_plan_codes
    plan_required_fields = ['carcve', 'placve', 'placof']
    plan_missing_fields = [campo for campo in plan_required_fields if campo not in df_plan_codes.columns]
    
    if plan_missing_fields:
        error_msg = f"❌ Faltan los siguientes campos requeridos en el DataFrame de códigos de planes: {plan_missing_fields}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Validar campos requeridos en df_esp_codes
    esp_required_fields = ['espcve', 'placve', 'carcve', 'espnco']
    esp_missing_fields = [campo for campo in esp_required_fields if campo not in df_esp_codes.columns]
    
    if esp_missing_fields:
        error_msg = f"❌ Faltan los siguientes campos requeridos en el DataFrame de códigos de especialidades: {esp_missing_fields}"
        logger.error(error_msg)
        raise ValueError(error_msg) 
    # Llenado de valores faltantes en especialidad, se aplica aqui porque se requiere para la codificación de variables categóricas
    def fill_esp(carr, plan):
        esp = 0
        if carr == 1:
            if plan <= 2:
                esp = 1
            else:
                esp = 2
        elif carr == 2:                     # Solo aplica a Ing. Industrias Alim (carr=2)
            if (plan < 2) | (plan > 4):    # Si el plan de estudios es 1 o 5, solo hay una especialidad (esp=1)
                esp = 1
            else:                           # Si el plan de estudios es de 2 a 4, la especialidad es la segunda (esp=2)
                esp = 2
        elif carr == 3:
            esp = 1
        elif carr == 4:
            if plan<2:
                esp = 1
            else:
                esp = 2
        elif carr == 6:
            esp = 1
        return esp

    df_main['espcve'] = df_main.apply(
        lambda row: fill_esp(row['carcve'], row['placve']) if pd.isnull(row['espcve']) else row['espcve'],
        axis=1)

    # copia del dataframe original para usar en el remapeo de especialidad
    df_copy = df_main.copy()
    try:
        logger.info("🔍 Mapeo los códigos de plan de estudios")
        # Mapear los códigos de plan de estudios
        plan_dict = df_plan_codes.set_index(['carcve', 'placve'])['placof'].to_dict()
        # Aplicar el mapeo usando una función lambda
        df_main['placve'] = df_main.apply(lambda row: plan_dict.get((row['carcve'], row['placve']), row['placve']), axis=1)
    except Exception as e:
        logger.error(f"❌ Error al mapear códigos de plan de estudios: {e}")
    try:
        logger.info("🔍 Mapeo los códigos de especialidad")
        # Mapear los códigos de especialidad
        esp_dict = df_esp_codes.set_index(['espcve', 'placve', 'carcve'])['espnco'].to_dict()
        df_main['espcve'] = df_copy.apply(lambda row: esp_dict.get((row['espcve'], row['placve'], row['carcve'])), axis=1)
    except Exception as e:
        logger.error(f"❌ Error al mapear códigos de especialidad: {e}")

    # Eliminar la copia del dataframe original
    del df_copy
    logger.info("✅ Proceso de variables de especialidad y plan de estudios completado.")
    return df_main

def remap_variables(df_main):
    """Remapea variables categóricas a valores más descriptivos.
    
    Args:
        df_main (pd.DataFrame): DataFrame principal
        
    Returns:
        pd.DataFrame: DataFrame con variables remapeadas
        
    Note:
        - Convierte códigos numéricos a etiquetas descriptivas
        - Estandariza valores binarios
        - Mapea tipos de calificación a descripciones
    """
    logger.info("🔄 Remapeando variables categóricas.")
    def remap(df, col, map_dict):
        """Remapea los valores de una columna usando un diccionario"""
        print(f'convirtiendo datos de variable {col} {df[col].unique()}...')
        df[col] = df[col].map(map_dict)
        print(f'nuevos valores: {df[col].unique()}')
    try:
        remap(df_main, 'carcve', {1:'ISIC', 2:'IIAL', 3:'IIND', 4:'IGEM', 6:'IIAS'})
        remap(df_main,'calpri', {'*':1, ' ':0})
        remap(df_main,'alusex', {1:1, 2:0})
        remap(df_main, 'alusme', {1:"IMSS", 2:'PEMEX', 3:'ISSTE', 4:'ESTA', 5:'PART', 6:'SEG_POP'})
        remap(df_main, 'alueci', {1:'Solt', 2:'Cas', 3:'Viu', 4:'Div', 5:'UnLib'})
        remap(df_main, 'aluare', {1:'FisMat', 2:'QuimBio', 3:'EconAdmin', 4:'SocHum', 5:'Gral', 6:'Otro'})
        remap(df_main, 'alupadv', {'S':1, 'N':0, ' ':np.nan})
        remap(df_main, 'alumadv', {'S':1, 'N':0, ' ':np.nan})
        remap(df_main, 'alulexp', {'S':1, 'N':0, ' ':np.nan})
        remap(df_main, 'calingi', {0:'None', 1:'Akate', 2:'Amuzgo', 52:'Tarau', 60:'Toton'})
        df_main[['alupadv', 'alumadv', 'alulexp']] = df_main[['alupadv', 'alumadv', 'alulexp']].astype('Int64')
        calcveMats = ['Algb_Lin_calcve', 'Calc_Dif_calcve', 'Calc_Int_calcve', 'Estad_calcve', 'Fund_Inv_calcve', 'Quim_calcve', 'Etica_calcve']
        for mat in calcveMats:
            remap(df_main, mat, {-2:'S/Cursar', -1:'Desrt',0:'S/Cal', 1:'Ord_1ra', 2:'Ord_2da', 3:'Global',
                                4:'RC_1ra', 5:'RC_2da', 6:'Esp_1ra', 7:'Esp_2da', 91:'Conval', 92:'Reval', 93:'Equiv'})
    except Exception as e:
        logger.error(f"❌ Error al remapear variables categóricas: {e}")
    logger.info("✅ Proceso de remapeo de variables categóricas completado.")
    return df_main

def birthToAge(df_main):
    """Convierte fechas de nacimiento a edad.
    
    Args:
        df_main (pd.DataFrame): DataFrame principal
        
    Returns:
        pd.DataFrame: DataFrame con edades calculadas
        
    Note:
        - Maneja valores faltantes en fechas
        - Calcula edad al último periodo cursado
        - Elimina columna original de fecha
    """
    logger.info("🔄 Calculando edad al último periodo cursado.")
    # Reemplazo de valores faltantes por nulos
    df_main['alunac'] = df_main['alunac'].replace('/  /', np.nan)
    try:
        # Conversión de tipo de dato
        df_main['alunac'] = pd.to_datetime(df_main['alunac'], format='%m/%d/%Y', errors='coerce')
    except Exception as e:
        logger.error(f"❌ Error al convertir tipo de dato de fecha de nacimiento: {e}")

    def calculate_age(datebirth, ingress, period):
        """Calcula la edad de un alumno en base a su fecha de nacimiento, periodo de ingreso y periodo de estudio actual"""
        year_in = (ingress // 10) + 1800
        age_in = year_in - datebirth.year
        age_last_period = age_in + math.ceil(period/2)
        return age_last_period
    try:
        df_main['edad'] = df_main.apply(
            lambda row: calculate_age(row['alunac'], row['caling'], row['calnpe']), axis=1
        )
    except Exception as e:
        logger.error(f"❌ Error al calcular edad: {e}")
    # Eliminación de columna 'alunac' que ya no es necesaria
    df_main = df_main.drop(columns=['alunac'])
    # Conversión de edad a entero
    df_main['edad'] =df_main['edad'].astype('Int64')
    logger.info("✅ Proceso de conversión de edad completado.")
    return df_main

def reorder_and_rename_cols(df_main):
    """Reordena y renombra las columnas del DataFrame.
    
    Args:
        df_main (pd.DataFrame): DataFrame principal
        
    Returns:
        pd.DataFrame: DataFrame con columnas reordenadas y renombradas
        
    Raises:
        ValueError: Si faltan columnas requeridas en el DataFrame
    """
    logger.info("🔄 Reordenando y renombrando columnas.")
    print(df_main.columns)
    sorted_cols = ['carcve', 'placve', 'espcve', 'caling', 'calnpe', 'calcac', 'calnpec',
       'caltcala', 'caltcalr', 'calmata', 'calmat', 'calmatac', 'calpri',
       'calnpep', 'calingt', 'calingi', 'alusex', 'edad', 'alu_nac_est',
       'alu_nac_mun', 'aluesc', 'aluegr', 'aluare', 'alu_dir_est', 'alu_dir_mun', 'aluescp',
       'alucpo', 'alusme', 'alueci', 'alupadv', 'alumadv', 'alutcp', 'alutra',
       'alulexp', 'alutecpo', 'alupexani', 'discve',
       'alucen', 'Algb_Lin', 'Algb_Lin_calcve', 'Calc_Dif', 'Calc_Dif_calcve',
       'Calc_Int', 'Calc_Int_calcve', 'Estad', 'Estad_calcve', 'Fund_Inv',
       'Fund_Inv_calcve', 'Quim', 'Quim_calcve', 'Etica', 'Etica_calcve']
    dict_rename_vars = {
    'carcve':'cve_carrera', 'placve':'cve_plan_estud', 'espcve':'cve_esp', 'caling':'period_ingreso', 'calnpe':'period_ultimo',
    'calcac':'cred_acum', 'calnpec':'period_conval', 'caltcala':'calif_aprob', 'caltcalr':'calif_reprob', 'calmata':'mat_aprob',
    'calmat':'mat_cursadas', 'calmatac':'mat_con_ac', 'calpri':'opcn_estudios', 'calnpep':'period_aut_comite',
    'calingt':'tipo_ingreso', 'calingi':'leng_indig', 'alusex':'genero', 'alu_nac_est':'estado_nac', 'alu_nac_mun':'munic_nac',
    'aluesc':'escuela', 'aluegr':'año_egreso', 'aluare':'area_egreso', 'alu_dir_est':'estado_dir', 'alu_dir_mun':'munic_dir',
    'aluescp':'prom_ingreso', 'alucpo':'cod_postal', 'alusme':'serv_medico', 'alueci':'edo_civil', 'alupadv':'papa_vive',
    'alumadv':'mama_vive', 'alutcp':'cod_post_tutor', 'alutra':'empresa', 'alulexp':'exp_trabj', 'alutecpo':'cod_post_trabj',
    'alupexani':'score_exani', 'discve':'discapacidad', 'alucen':'cntro_trab'
    }
    df_students_names = df_main[['aluctr', 'aluapp', 'aluapm', 'alunom']]
    df_students_names = df_students_names.rename(columns={'aluctr':'# Control', 'aluapp':'Apellido Pat', 'aluapm':'Apellido Mat', 'alunom':'Nombre'})
    print(f'dataframe de datos de alumnos: {df_students_names}')
    # verificar que las columnas estén en el dataframe sin importar el orden
    missing_cols = set(sorted_cols) - set(df_main.columns)
    if len(missing_cols) > 0:
        logger.error(f'❌ Faltan columnas en el dataframe: {missing_cols}')
        raise ValueError(f'Faltan columnas en el dataframe: {missing_cols}')
    else:
        try:
            # Reordenamiento de columnas
            df_main = df_main.drop(columns=['abandono'])
            df_main = df_main.reindex(sorted_cols, axis=1)
            df_main = df_main.rename(columns=dict_rename_vars)
        except Exception as e:
            logger.error(f"❌ Error al reordenar y renombrar columnas: {e}")   
    logger.info("✅ Proceso de reordenamiento y renombramiento de columnas completado.")
    return df_main, df_students_names

def objToCat(df_main):
    """Convierte columnas de tipo object a categorical.
    
    Args:
        df_main (pd.DataFrame): DataFrame principal
        
    Returns:
        pd.DataFrame: DataFrame con columnas convertidas a categorical
    """
    logger.info("🔄 Convirtiendo columnas de tipo object a categorical.")
    for col in df_main.select_dtypes(include=['object']).columns:
        df_main[col] = df_main[col].astype('category')
    logger.info("✅ Proceso de conversión de columnas de tipo object a categorical completado.")
    return df_main

def preprocess_pipeline(config: PreprocessConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Ejecuta el pipeline completo de preprocesamiento.
    Args:
        config (PreprocessConfig): Configuración del preprocesamiento 
    Returns:
        pd.DataFrame: DataFrame procesado y listo para entrenamiento  
    Note:
        - Carga datos iniciales
        - Procesa calificaciones
        - Combina datos
        - Limpia y transforma variables
    """
    logger.info("🚀 Iniciando pipeline de preprocesamiento")
    try:
        df_cal, df_alumn, df_dcalumn = load_data(
            config.files['dalumn'],
            config.files['dcalum'],
            config.files['dkarde']
        )
        loc_codes = pd.read_csv(config.files['ubicaciones'], encoding='latin-1')
        school_codes = pd.read_csv(config.files['escuelas'], encoding='latin-1')
        plan_codes = pd.read_csv(config.files['plan_estudio'], encoding='latin-1')
        esp_codes = pd.read_csv(config.files['especialidad'], encoding='latin-1')

        df_cal = process_grades(df_cal)
        df_main = merge_dataframes(df_cal, df_alumn, df_dcalumn)
        df_main = filter_order_data(df_main)
        df_main = handle_miss_matVals(df_main)
        df_main = drop_useless_cols(df_main)
        dep_var_map = {1:0, 2:1, 4:1, 5:0}
        df_main['abandono'] = df_main['abandono'].map(dep_var_map)
        df_main = change_dtypes(df_main)
        df_main = handle_location_codes(df_main, loc_codes)
        df_main = handle_school_codes(df_main, school_codes)
        df_main = handle_course_esp_plan(df_main, plan_codes, esp_codes)
        df_main = remap_variables(df_main)
        df_main = birthToAge(df_main)
        df_main, df_students_names = reorder_and_rename_cols(df_main)
        df_main = objToCat(df_main)
        logger.info("🔄 Guardando dataset procesado")
        # df_main.to_csv(os.path.join(config.output_path, 'processed_data.csv'), index=False)
        logger.info("✅ Dataset procesado guardado")
        return (df_main, df_students_names)
    except Exception as e:
        logger.error(f"❌ Error en el pipeline de preprocesamiento: {str(e)}")
        raise

if __name__ == "__main__":
    # Ejemplo de uso
    config = load_config(main_path+'/config.yaml')
    valid_types = PreprocessConfig(**config)
    df_processed = preprocess_pipeline(valid_types)