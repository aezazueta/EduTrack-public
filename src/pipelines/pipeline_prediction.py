from altair import DataFormat
import pandas as pd
import joblib
from src.utils import load_config, config_logging, log_function
from src.utils.config_utils import PreprocessConfig
from src.utils.logging_utils import config_logging

# Configuración global del logger
# Importar el logger desde el módulo de preprocesamiento
# import logging

# Configuración del logger
# logging.basicConfig(level=logging.INFO)
logger = config_logging()

class Predictionpipeline:
    def __init__(self, df_prepared: pd.DataFrame, config: PreprocessConfig) -> None:
        """
        """
        self.df_prepared = df_prepared
        self.df_predicted = self
        self.config = config
        

    def get_predictions(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        model = joblib.load(open(self.config.files['model'], 'rb'))
        df = self.df_prepared #creado solo para omitir el error de abajo  ELIMINAR DESPUES
        y_predicted = model.predict(df)
        y_predicted = pd.DataFrame(y_predicted, columns=['Prediccion'])
        y_predicted['Prediccion'] = y_predicted['Prediccion'].map({1:'Abandono', 0:'No abandono'})

        y_predicted_proba = model.predict_proba(df)
        y_predicted_proba = pd.DataFrame(y_predicted_proba, columns=['NA', 'A'])
        y_predicted_proba['Probabilidad'] = round((y_predicted_proba[['NA', 'A']].max(axis=1)) * 100, 2)
        #y_predicted_proba['Probabilidad'] = y_predicted_proba['Probabilidad'] * 100
        #print(f'Predicted proba: \n {y_predicted_proba}')
        return (y_predicted, y_predicted_proba['Probabilidad'])

def printName():
    print(f'valor del atributo __name__:{__name__}')
