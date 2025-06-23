# EduTrack
Sistema para el seguimiento, análisis y predcición de abandono escolar universitario untilizando Streamlit y machine learning con python.

## Tabla de contenidos
- [EduTrack](#edutrack)
  - [Tabla de contenidos](#tabla-de-contenidos)
  - [Descripción](#descripción)
  - [Características](#características)
  - [Instalación y uso](#instalación-y-uso)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Configuración](#configuración)
  - [Licencia](#licencia)
  - [Privacidad y Confidencialidad](#privacidad-y-confidencialidad)
  - [Contacto](#contacto)
  
## Descripción
EduTrack es una webapp desarrollada en python que permite analizar datos escolares, visualizar datos relevantes y predecir el riesgo de abandono escolar. Utiliza el framework Streamlit para la interfaz web y un modelo de machine learning basado en el algoritmo de arboles de desición.

## Características
  * Carga y procesamiento de datos escolares.
  * Predicción de riesgo de abandono escolar incluida su probabilidad de ocurrencia.
  * Subsistema de registro de eventos (logs) para seguimiento de eventos ya sea por monitoreo o por depuración.
  * Configuración de parámetros y rutas de acceso mediante archivos YAML.

## Instalación y uso
1.- Clona el repositorio:
```
git clone https://github.com/aezazueta/EduTrack.git 
```
2.- Crea y activa un entorno virtual (opcional pero recomendado)

```
python -m venv <nombre_del_ambiente>
.\<ambiente>\Scripts\activate   #En windows
source .venv/bin/activate       #En linux
```
3.- Instala las dependencias
```
pip install -r requirements.txt
```
4.- Ejecuta la aplicación
```
streamlit run streamlit_app.py
```

## Estructura del proyecto
```
EduTrack/
│
├── config/             # Archivos de configuración (YAML)
│
├── data/               # Datos crudos y procesados
│   ├── raw/            # Datos originales
│   └── processed/      # Datos procesados
│
├── docs/               # Documentación adicional
│
├── logs/               # Archivos de registro (logs)
│
├── src/                # Código fuente principal
│   ├── models/         # Modelos entrenados (ej. .joblib)
│   ├── pipelines/      # Pipelines de procesamiento y predicción
│   └── utils/          # Utilidades y funciones auxiliares
│
├── static/             # Recursos estáticos
│   ├── fonts/          # Tipografías
│   └── imgs/           # Imágenes
│
├── tests/              # Pruebas automatizadas
│
├── .streamlit/         # Configuración específica de Streamlit
│
├── .vscode/            # Configuración del editor VSCode
│
├── .venv/              # Entorno virtual de Python (no subir a git)
│
├── .git/               # Carpeta de control de versiones (Git)
│
├── streamlit_app.py    # Aplicación principal de Streamlit
├── requirements.txt    # Dependencias del proyecto
├── README.md           # Documentación principal
├── PLANNING.md         # Planeación del proyecto
├── TASK.md             # Tareas y pendientes
└── .cursorrules        # Reglas de Cursor
```

## Configuración
Elementos referentes a rutas de archivo, ubicaciónes y versión de la aplicación se pueden configurar en el archivo 
``` .\config\config.yaml```
El control de usuarios y cookies se configuran en 
```.\config\config_login.yaml```
Configuraciónes acera de la apariencia de la interfaz, aspectos del servidor, navegador y del cliente se modifican en 
```.\.steramlit\config.toml```

## Licencia
Este proyecto está licenciado bajo la MIT License. Los datos reales utilizados en la veersión institucional no se incluyen en este repositorio.

## Privacidad y Confidencialidad

Este proyecto fue desarrollado originalmente con datos reales en una institución educativa universitaria adscrita al Tecnológico Nacional de México. No obstante, **todos los datos incluidos en este repositorio han sido generados sintéticamente** y **no representan a ningún estudiante real**.

El propósito de este repositorio es exclusivamente **demostrativo y académico**. Ninguna parte de esta publicación compromete la privacidad institucional ni viola acuerdos de confidencialidad.

## Contacto
* 📧 Correo: alain.apok@gmail.com
* 🔗 GitHub: https://github.com/aezazueta
* 💼 LinkedIn: www.linkedin.com/in/alain-eduardo-zazueta-valenzuela-82a74a28