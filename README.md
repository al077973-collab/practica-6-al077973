# practica-6-al077973
# 🏗️ Análisis Sísmico de una Estructura por Piso

## 📘 Descripción General
Este proyecto implementa un programa en **Python con Tkinter** que realiza el **análisis sísmico por piso** de una estructura, evaluando la **deriva lateral máxima** en cada nivel.

El objetivo es determinar si la estructura cumple con el **límite de deriva permitido (0.005 m)** establecido por normativas sísmicas.  
El sistema utiliza una **interfaz gráfica amigable**, donde el usuario puede ingresar las propiedades de cada piso (masa, rigidez y fuerza sísmica aplicada) y obtener automáticamente los resultados del análisis.

---

## ⚙️ Funcionalidades
- Ingreso del **número de pisos** de la estructura.  
- Ingreso interactivo de:
  - Masa (kg)
  - Rigidez (N/m)
  - Fuerza sísmica (N)
- Cálculo automático de la **deriva por piso** usando la relación:
  \[
  \delta = \frac{F}{K}
  \]
- Identificación de:
  - Piso con **mayor deriva**.
  - Si **se excede o cumple** el límite de deriva (0.005 m).
- **Informe detallado** mostrado en pantalla con íconos visuales (✅ Cumple / ⚠️ Falla).

---

## 🧮 Fundamento Teórico

El análisis se basa en la ecuación de **deriva de entrepiso**:
\[
\text{Deriva} = \frac{F}{K}
\]
donde:  
- **F** = Fuerza sísmica aplicada al piso (N).  
- **K** = Rigidez lateral del piso (N/m).  
- **Deriva límite** = 0.005 m (criterio de servicio estructural).  

Si la deriva calculada excede este valor, el piso **no cumple** con el límite de desplazamiento permitido por normativas estructurales.

---

## 🧰 Tecnologías Utilizadas
- **Python 3.8+**
- **Tkinter** (librería estándar para GUI)
- **Math** (para operaciones básicas)

No se requieren librerías externas, por lo que el programa funciona en **IDLE, VS Code, PyCharm o consola** sin instalación adicional.

---

## 🖥️ Interfaz Gráfica

### 💡 Características visuales:
- Fondo degradado con tonos azul-gris.
- Estilo tipo “panel” para separar secciones.
- Campos con *placeholders* que guían el ingreso de datos.
- Reporte estructurado con tipografía monoespaciada.

### 🧩 Componentes principales:
| Sección | Descripción |
|----------|--------------|
| **Entrada superior** | Campo para número de pisos y botón *Generar Datos*. |
| **Tabla de datos** | Campos de entrada para masa, rigidez y fuerza sísmica por piso. |
| **Botón de cálculo** | Ejecuta el análisis sísmico. |
| **Panel de resultados** | Muestra la deriva de cada piso y el cumplimiento del límite. |

python "PROYECTO_ANALISIS SISMICO DE UNA ESTRUCTURA POR PISO.py"
