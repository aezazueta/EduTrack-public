from sklearn.preprocessing import MinMaxScaler
from src.utils.logging_utils import config_logging
import math
import pandas as pd
import numpy as np
import logging

logger = config_logging()

class DataPreparationPipeline:
    def __init__(self, df_processed: pd.DataFrame) -> None:
        """Inicializa el pipeline de preparación de datos.

        Args:
            df_processed (pd.DataFrame): DataFrame que contiene los datos procesados
                                       provenientes de la pipeline de preprocesamiento.

        Returns:
            None: El constructor inicializa los atributos de la clase pero no retorna nada.
        """
        self.df_processed = df_processed
        self.df_prepared = self.start_data_preparation(df_processed)

    def get_prepared_data(self) -> pd.DataFrame:
        """Retorna el DataFrame procesado.

        Returns:
            pd.DataFrame: DataFrame con los datos procesados.
        """
        return self.df_prepared

    def drop_useless_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        """Elimina columnas innecesarias basadas en análisis exploratorio."""
        try:
            logger.info("🔄 Iniciando purga de columnas innecesarias post EDA")
            drop_cols = ['opcn_estudios', 'empresa', 'exp_trabj', 'cod_post_trabj', 'cod_post_tutor', 'score_exani',
                        'discapacidad', 'cntro_trab', 'papa_vive', 'mama_vive', 'calif_reprob', 'leng_indig', 'estado_nac',
                        'munic_nac', 'estado_dir', 'munic_dir', 'serv_medico', 'edo_civil']
            df = df.drop(columns=drop_cols)
            logger.info("✅ Columnas eliminadas")
            return df
        except Exception as e:
            logger.error(f"❌ Error al eliminar columnas: {str(e)}")
            raise

    def handle_atypical_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Maneja valores atípicos en el DataFrame."""
        try:
            logger.info("🔄 Iniciando manejo de valores atípicos")
            # Reemplaza los valores atípicos de la columna 'cod_postal' con el valor más frecuente
            df['cod_postal'] = df['cod_postal'].replace(0, df['cod_postal'].mode()[0])

            # Reemplaza valores atípicos de la columna 'año_egreso' que solo tienen 2 digitos
            wrong_grad_years = df[(df['año_egreso'] < 1800) & (df['año_egreso'] > 0)]['año_egreso'].index
            for row in wrong_grad_years:
                df.at[row, 'año_egreso'] = df.at[row, 'año_egreso'] + 2000

            wrong_ages = df[df['edad'] < 15]['edad'].index
            # En cada caso se reemplaza por la suma de 18 y el ultimo periodo cursado
            for row in wrong_ages:
                df.at[row, 'edad'] = math.ceil((df.at[row, 'period_ultimo'])/2) + 18

            logger.info("✅ Valores atípicos manejados")
            return df
        except Exception as e:
            logger.error(f"❌ Error al manejar valores atípicos: {str(e)}")
            raise

    def imputation_of_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Imputa valores faltantes en el DataFrame."""
        try:
            logger.info("🔄 Iniciando imputación de valores faltantes")
            modaEgreso = df['area_egreso'].mode().values[0]
            df['area_egreso'] = df['area_egreso'].fillna(modaEgreso)
            df['period_ingreso'] = df['period_ingreso'].ffill()
            df['edad'] = df.apply(
                lambda row: (18 + math.ceil(row['period_ultimo']/2)) if pd.isnull(row['edad']) else row['edad'],
                axis=1)
            
            def set_school(cp, cp_list):
                for codpos in cp_list:
                    if cp == codpos:
                        result = df[df['cod_postal'] == codpos]['escuela'].mode()
                        if not result.empty:
                            return result.iloc[0]
                        else:
                            return df['escuela'].mode()[0]
                return df['escuela'].mode()[0]

            cp_list = df['cod_postal'].unique()
            df['escuela'] = df.apply(
                lambda row: set_school(row['cod_postal'], cp_list) if pd.isnull(row['escuela']) else row['escuela'],
                axis=1)
            df['escuela'] = df['escuela'].astype('category')

            if df['escuela'].isna().sum() > 0:
                logger.error("❌ Advertencia, aún quedan datos perdidos en campo 'escuela'")
                raise ValueError("❌ Advertencia, aún quedan datos perdidos en campo 'escuela'")

            missed_grad_years = df[df['año_egreso'] == 0].index
            for row in missed_grad_years:
                df.at[row, 'año_egreso'] = (df.at[row, 'period_ingreso'] // 10) + 1800

            def fix_grad_grade(grade):
                if pd.isna(grade):
                    return grade
                elif grade > 0 and grade <= 10:
                    return grade*10
                else:
                    return grade

            df['prom_ingreso'] = df['prom_ingreso'].replace(0, np.nan)
            df['prom_ingreso'] = df['prom_ingreso'].apply(fix_grad_grade)
            df['prom_ingreso'] = df['prom_ingreso'].fillna(df['prom_ingreso'].mean())
            df['prom_ingreso'] = round(df['prom_ingreso'], 2)

            # Verificar que todas las columnas tengan la misma cantidad de datos no nulos
            non_null_counts = df.count()
            expected_count = len(df)
            
            if not all(count == expected_count for count in non_null_counts):
                columns_with_null = non_null_counts[non_null_counts != expected_count]
                logger.error(f"❌ Las siguientes columnas tienen valores nulos: {columns_with_null}")
                raise ValueError(f"❌ Las siguientes columnas tienen valores nulos: {columns_with_null}")
            
            logger.info("✅ Verificación de valores nulos completada")
            return df
        except Exception as e:
            logger.error(f"❌ Error en la imputación de valores faltantes: {str(e)}")
            raise

    def coding_cat_vars(self, df: pd.DataFrame) -> pd.DataFrame:
        """Codifica variables categóricas usando one-hot encoding."""
        try:
            logger.info('🔄 Iniciando codificación de variables categóricas.')
            cat_vars = df.select_dtypes(include="category").columns
            
            def data_discretization(df: pd.DataFrame, cols: list, threshold=0.05):
                for col in cols:
                    freq = df[col].value_counts(normalize=True).sort_values()
                    cat_cum = freq.cumsum()
                    cat_low_freq = cat_cum[cat_cum <= threshold].index
                    df[col] = df[col].apply(lambda x: 'otros' if x in cat_low_freq else x)
                return df

            df = data_discretization(df, cat_vars)
            dummies = pd.get_dummies(df[cat_vars], prefix_sep='>', drop_first=True, dtype=int)
            df = pd.concat([df, dummies], axis=1)
            df = df.drop(columns=cat_vars)

            logger.info(f'✅ Codificación de variables categóricas terminada.')
            return df
        except Exception as e:
            logger.error(f"❌ Error en la codificación de variables categóricas: {str(e)}")
            raise

    def normalize_vars(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normaliza variables numéricas usando MinMaxScaler."""
        try:
            logger.info('🔄 Iniciando normalización de variables.')
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            binary_cols = [col for col in numeric_cols if set(df[col].unique()).issubset({0, 1})]
            cols_to_norm = [col for col in numeric_cols if col not in binary_cols]
            
            if cols_to_norm:
                scaler = MinMaxScaler()
                df[cols_to_norm] = scaler.fit_transform(df[cols_to_norm])
                logger.info(f'✅ Normalización completada para {len(cols_to_norm)} variables.')
            else:
                logger.info('ℹ️ No se encontraron variables numéricas para normalizar.')

            return df
        except Exception as e:
            logger.error(f"❌ Error en la normalización de variables: {str(e)}")
            raise

    def start_data_preparation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Inicia el pipeline de preparación de datos."""
        try:
            df = self.drop_useless_cols(df)
            df = self.handle_atypical_values(df)
            df = self.imputation_of_missing_values(df)
            df = self.coding_cat_vars(df)
            df = self.normalize_vars(df)
            return df
        except Exception as e:
            logger.error(f"❌ Error en el pipeline de preparación de datos: {str(e)}")
            raise

"""
🔄 Inicio de procesos
📂 Carga de archivos
✅ Operaciones exitosas
❌ Errores
🔍 Validaciones
✨ Finalización exitosa
"""