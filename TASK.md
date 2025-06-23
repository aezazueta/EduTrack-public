# TASKS.md - Tareas Iniciales del Proyecto

## Configuración Inicial del Entorno

### 1. Setup del Proyecto (Prioridad: Alta)
**Tiempo estimado: 2-3 horas**

- [ ] Crear repositorio Git y estructura de carpetas
- [ ] Configurar entorno virtual Python
- [ ] Crear `requirements.txt` con dependencias base:
  ```
  streamlit>=1.28.0
  pandas>=1.5.0
  numpy>=1.21.0
  scikit-learn>=1.0.0
  joblib>=1.2.0
  plotly>=5.0.0
  openpyxl>=3.0.0
  ```
- [ ] Configurar `.gitignore` para Python y Streamlit
- [ ] Crear README.md básico con instrucciones de instalación

### 2. Configuración de Desarrollo (Prioridad: Alta)
**Tiempo estimado: 1-2 horas**

- [ ] Configurar herramientas de desarrollo:
  - [ ] Black para formateo automático
  - [ ] Flake8 para linting
  - [ ] Pre-commit hooks (opcional)
- [ ] Crear archivo `pyproject.toml` o `setup.cfg` para configuraciones
- [ ] Configurar IDE/Editor con extensiones de Python

## Desarrollo del Core del Sistema

### 3. Módulo de Carga de Modelos (Prioridad: Alta)
**Tiempo estimado: 4-6 horas**

- [ ] **Crear `src/models/model_loader.py`**:
  - [ ] Función para cargar modelos pickle/joblib
  - [ ] Validación de formato de modelo
  - [ ] Manejo de errores de carga
  - [ ] Cache con `@st.cache_resource`

```python
# Ejemplo de estructura:
@st.cache_resource
def load_model(model_path: str):
    """Carga modelo ML con caché optimizado"""
    pass
```

- [ ] **Crear `src/models/predictor.py`**:
  - [ ] Clase wrapper para modelos
  - [ ] Métodos de predicción individual y en lote
  - [ ] Validación de entrada de datos

### 4. Módulo de Procesamiento de Datos (Prioridad: Alta)
**Tiempo estimado: 3-4 horas**

- [ ] **Crear `src/data/processor.py`**:
  - [ ] Función para cargar CSV/Excel
  - [ ] Validación de columnas requeridas
  - [ ] Limpieza básica de datos
  - [ ] Cache con `@st.cache_data`

- [ ] **Crear `src/data/validator.py`**:
  - [ ] Validar estructura de datos
  - [ ] Detectar valores faltantes
  - [ ] Validar tipos de datos

### 5. Interface Principal Streamlit (Prioridad: Alta)
**Tiempo estimado: 6-8 horas**

- [ ] **Crear `src/app.py` con estructura básica**:
  - [ ] Configuración de página Streamlit
  - [ ] Sidebar para navegación
  - [ ] Layout principal con pestañas/secciones

- [ ] **Implementar secciones principales**:
  - [ ] **Carga de Modelo**: File uploader para modelos
  - [ ] **Carga de Datos**: File uploader para datasets
  - [ ] **Predicciones**: Botón para ejecutar predicciones
  - [ ] **Resultados**: Display de predicciones con métricas básicas

```python
# Estructura base de app.py:
import streamlit as st
from models.model_loader import load_model
from data.processor import process_data

st.set_page_config(
    page_title="Predictor de Deserción Escolar",
    page_icon="🎓",
    layout="wide"
)
```

## Utilidades y Optimización

### 6. Sistema de Cache y Estado (Prioridad: Media)
**Tiempo estimado: 2-3 horas**

- [ ] **Crear `src/utils/cache_utils.py`**:
  - [ ] Utilidades para limpiar caché
  - [ ] Gestión de session state
  - [ ] Monitoreo de uso de memoria

- [ ] **Implementar gestión de estado**:
  - [ ] Estado del modelo cargado
  - [ ] Estado de datos procesados
  - [ ] Historial de predicciones en sesión

### 7. Visualizaciones Básicas (Prioridad: Media)
**Tiempo estimado: 3-4 horas**

- [ ] **Crear `src/utils/viz_utils.py`**:
  - [ ] Gráficos de distribución de predicciones
  - [ ] Métricas de resumen (conteos, porcentajes)
  - [ ] Tabla de resultados formateada

- [ ] **Implementar en app principal**:
  - [ ] Dashboard básico con métricas
  - [ ] Gráficos interactivos con Plotly
  - [ ] Opción de descarga de resultados

## Testing y Documentación

### 8. Pruebas Básicas (Prioridad: Media)
**Tiempo estimado: 2-3 horas**

- [ ] **Crear estructura de testing**:
  - [ ] `tests/test_model_loader.py`
  - [ ] `tests/test_data_processor.py`
  - [ ] Datos de prueba sintéticos

- [ ] **Pruebas unitarias básicas**:
  - [ ] Test de carga de modelos válidos/inválidos
  - [ ] Test de procesamiento de datos
  - [ ] Test de validaciones

### 9. Documentación Inicial (Prioridad: Baja)
**Tiempo estimado: 1-2 horas**

- [ ] **Completar README.md**:
  - [ ] Instrucciones de instalación detalladas
  - [ ] Guía de uso básico
  - [ ] Estructura del proyecto
  - [ ] Screenshots de la aplicación

- [ ] **Docstrings en funciones principales**:
  - [ ] Documentar parámetros y returns
  - [ ] Ejemplos de uso
  - [ ] Excepciones que pueden lanzar

## Preparación de Datos de Ejemplo

### 10. Dataset y Modelo de Ejemplo (Prioridad: Media)
**Tiempo estimado: 2-3 horas**

- [ ] **Crear o conseguir dataset de ejemplo**:
  - [ ] Datos sintéticos de estudiantes
  - [ ] Columnas típicas: edad, notas, asistencia, etc.
  - [ ] Formato CSV limpio

- [ ] **Modelo de ejemplo**:
  - [ ] Entrenar modelo simple (RandomForest/LogisticRegression)
  - [ ] Guardar con joblib/pickle
  - [ ] Documentar features esperadas

## Configuración Final

### 11. Optimización y Pulimiento (Prioridad: Baja)
**Tiempo estimado: 2-4 horas**

- [ ] **Optimizaciones de rendimiento**:
  - [ ] Revisar uso de caché
  - [ ] Optimizar carga de datos grandes
  - [ ] Lazy loading donde sea posible

- [ ] **UI/UX mejoras**:
  - [ ] Spinners y progress bars
  - [ ] Mensajes de error user-friendly
  - [ ] Tooltips y ayuda contextual

- [ ] **Configuración de producción**:
  - [ ] Variables de entorno
  - [ ] Configuración de límites de archivo
  - [ ] Logging básico

## Checklist de Completion

### Criterios de Éxito para MVP
- [ ] ✅ La aplicación carga y funciona sin errores
- [ ] ✅ Se puede cargar un modelo ML exitosamente
- [ ] ✅ Se puede cargar un dataset CSV
- [ ] ✅ Las predicciones se generan correctamente
- [ ] ✅ Los resultados se muestran de forma clara
- [ ] ✅ La aplicación responde en < 5 segundos para operaciones normales
- [ ] ✅ El código sigue estándares de Python (PEP 8)

### Próximos Pasos Post-MVP
1. Implementar validación avanzada de modelos
2. Agregar más tipos de visualizaciones
3. Sistema de logging completo
4. Deploy en plataforma cloud (Streamlit Cloud, Heroku, etc.)
5. Métricas de performance del modelo
6. Comparación de múltiples modelos