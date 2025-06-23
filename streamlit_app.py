import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime
import os
import base64
from src.utils.config_utils import PreprocessConfig, load_config
from src.utils import config_logging, log_function
from src.pipelines import pipeline_data_preparation as pl_dp, pipeline_preprocessing as pl_prep, pipeline_prediction as pl_pred

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

main_path = os.path.dirname(os.path.abspath(__file__))
logger = config_logging()
config_dict = load_config(main_path + '/config/config.yaml')
valid_types = PreprocessConfig(**config_dict)

st.set_page_config(
    page_title='EduTrack TecEldorado',
    page_icon=valid_types.files['images']+"eldorado-tecnm.ico",
    menu_items={
        'Get Help': 'https://www.google.com',
        'Report a bug': "https://docs.streamlit.io",
        'About': "### WebApp y modelo de predicción desarrollados por: **MEE. Alain Eduardo Zazueta Valenzuela**"
    }  
)

@st.cache_data
def load_data(files_dict: dict):
    """
    Función cacheada para cargar datos del archivo.
    Esto evita recargar el mismo archivo múltiples veces.
    """
    for file in files_dict.keys():
        try:
            # Obtener el archivo cargado para esta tabla
            uploaded_file = files_dict[file]
            
            if uploaded_file is not None:
                # Determinar la extensión del archivo
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                # Construir la ruta de destino
                #destination_path = os.path.join(main_path, 'data', 'raw', f"{file}.csv")
                print(f'guardando destino del archivo: {config_dict[file]}')
                destination_path = config_dict[file]

                # Leer el archivo según su extensión
                if file_extension == 'csv':
                    df = pd.read_csv(uploaded_file)
                elif file_extension in ['xlsx', 'xls']:
                    df = pd.read_excel(uploaded_file)
                else:
                    st.error(f"Formato de archivo no soportado: {file_extension}")
                    continue
                
                # Guardar como CSV
                df.to_csv(destination_path, index=False)
                st.success(f"✅ Archivo {file} guardado exitosamente")
                
        except Exception as e:
            show_error_load(e)
            continue
    

@st.cache_data
def send2preprocess(config: dict):
    """
    Función cacheada para procesar el DataFrame.
    Aquí puedes agregar cualquier preprocesamiento necesario.
    """
    # valid_types = PreprocessConfig(**config)
    return pl_prep.preprocess_pipeline(valid_types)

@st.cache_data
def send2prepare(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    obj = pl_dp.DataPreparationPipeline(df)
    return obj.get_prepared_data()

@st.cache_data
def send2predict(df: pd.DataFrame, config: PreprocessConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    # QUEDA PENDIENTE EL MÓDULO QUE CARGA EL DATAFRAME EN EL MODELO Y RETORNA LAS PREDICCIONES
    # valid_types = PreprocessConfig(**config)
    obj = pl_pred.Predictionpipeline(df, valid_types)
    return obj.get_predictions()
    

def log_error(error):
    """
    Función para registrar errores en el archivo de log
    """
    with open("log.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {str(error)}\n")

def show_error_load(e):
    st.error("❌ Error al cargar, verifique el formato del archivo")
    log_error(e)
    st.info("Sugerencias:\n"
        "- Asegúrate de que el archivo no esté corrupto\n"
        "- Verifica que el archivo tenga el formato correcto\n"
        "- Para archivos Excel, asegúrate de que la hoja tenga datos"
        "- Verifica que estés cargando un solo archivo.")

LOGO_ELD = valid_types.files['images']+'logo_tec_eldorado_500X468.png'
LOGO_TECNM = valid_types.files['images']+'logo_TecNM_216X300.png'
# Función para convertir imagen local a base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
def close_the_session():
    logger.info(f'❗ Finalización de sesión, usuario {st.session_state.get('name')}')
def access_app():
    #st.set_page_config(layout="wide")
    logger.info(f'✅ Inicio de sesión exitoso, usuario {st.session_state.get('name')}')
    # Convertir imágenes locales a base64
    img_izq_base64 = get_base64_image(LOGO_ELD)
    img_der_base64 = get_base64_image(LOGO_TECNM)

    # HTML con imágenes en base64
    html_code = f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 15vh;">
        <img src="data:image/png;base64,{img_izq_base64}" alt="Imagen izquierda" style="max-width: 140px; margin-right:20px; ">
        <h1 style='text-align: center; font-size: 3em;'>TecNM campus Eldorado</h1>
        <img src="data:image/png;base64,{img_der_base64}" alt="Imagen derecha" style="max-width: 100px; margin-left: 20px; ">
    </div>
    <h2 style='text-align: center;'>Predictor de abandono escolar EduTrack</h2>
    <br>
    <br>
    <br>
    """
    # Mostrar en Streamlit
    st.markdown(html_code, unsafe_allow_html=True)




    st.markdown("""
    <style>
        .upload-box {
            border: 2px dashed #4A90E2;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            background-color: #f8f9fa;
        }
        .upload-box:hover {
            background-color: #e9ecef;
        }
    </style>
    """, unsafe_allow_html=True)


    #st.markdown("<h3 style='text-align: center;'>Carga de datos</h3>", unsafe_allow_html=True)
    st.subheader("Carga de datos")

    files_dict = {}
    #tabsList = ["Arch. dalumn", "Arch. dcalumn", "Arch. dkarde", "Arch. dplane",
    #"Arch. despec", "Arch. descue", "Arch. dmunic", "Arch. dest"]

    filesList = ["dalumn", "dcalumn", "dkarde", "dplane",
    "despec", "descue", "dmunic", "dest"]

    col1, col2 = st.columns(2)
    colsList = [col1, col2]
    count=0


    with st.container(border=True):
        for col in colsList:
            with col:
                for index in range(4):
                    #st.markdown(f"<div class='upload-box'><strong>{index}</strong><br>Arrastra y suelta aquí<br><small>Límite: 200MB • Formatos: CSV, XLS, XLSX</small></div>", unsafe_allow_html=True)
                    #st.write(f"Cargue el archivo **:blue-background[{filesList[count]}]** :page_facing_up:")
                    with st.expander(f"Cargue el archivo **:blue-background[{filesList[count]}]** :page_facing_up:"):
                        file = st.file_uploader(    
                        "Cargue el archivo **:blue-background[{filesList[count]}]** :page_facing_up: :material/table_view:",
                        label_visibility='hidden',
                        type=["csv", "xls", "xlsx"],
                        key=f"loader{count}",
                        help="Formato de archivo soportado: csv, xls, xlsx"
                        )
                        files_dict[filesList[count]] = file
                        if file is not None:
                            st.write(f"Archivo cargado: {file.name}")
                            st.badge(label="Archivo cargado", icon=":material/check:",color="green")
                    st.divider()
                    count+=1

    #hide_col1, visible_col2, hide_col3 = st.columns(3)
    #with visible_col2:
        #st.write(f"**contenido** del dicionario {files_dict}")
        # if st.button("Procesar", type='primary', icon='🚨'):
    #pressed = st.button("Procesar", type='primary', icon=':material/psychology:', use_container_width=True)
    if st.button("Procesar", type='primary', icon=':material/psychology:'):
        
        load_data(files_dict)
        dfProcessed, df_students_names = send2preprocess(config_dict)
        print('esto devuelve preprocess:')
        print(dfProcessed)
        dfPrepared = send2prepare(dfProcessed)
        print('esto devuelve prepared:')
        print(dfPrepared)
        df_predicted, df_predicted_proba = send2predict(dfPrepared, config_dict)
        df_data_to_show = pd.concat([df_students_names, df_predicted, df_predicted_proba], axis=1)
        print(df_students_names)
        st.dataframe(df_data_to_show)
        subcol1, subcol2 = st.columns([2.5,1])
        with subcol1:
            st.download_button(
                label="💾 Descargar resultados",
                data=df_data_to_show.to_csv(index=False).encode("latin-1"),
                file_name= f"Predicciones-{datetime.now()}.csv",
                mime="text/csv",
            )
        with subcol2:
            if st.button("Borrar caché", type='secondary', icon='📛'):
                st.cache_data.clear()

###############################################################################################################
with open(valid_types.files['config_login']) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
try:
    authenticator.login(location='main',
    max_login_attempts=5,
    max_concurrent_users=2,
    single_session=True,
    fields={'Form name':'Inicio de sesión', 'Username':'Usuaio', 'Password':'Contraseña', 'Login':'Acceder', 'Captcha':'Captcha'})
    
except Exception as e:
    st.error(e)
print(st.session_state.get('authentication_status'))
if st.session_state.get('authentication_status'):
    version = None
    access_app()
    col1, col2 = st.columns([3,1])
    with col2:
        if st.button('Cerrar sesión'):
            close_the_session()
            authenticator.logout(location='unrendered')
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')

st.markdown(f'<footer style="text-align: right;">Ver. {valid_types.version}</footer>', unsafe_allow_html=True)

