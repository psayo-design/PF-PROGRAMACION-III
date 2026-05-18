# IMPLEMENTACIÓN DE ÁRBOL B EN PYTHON

## Descripción del Proyecto

Este proyecto consiste en la implementación de un Árbol B dinámico utilizando el lenguaje de programación Python.

El sistema permite configurar el grado del Árbol B y realizar operaciones fundamentales sobre la estructura de datos, incluyendo:

- Inserción de claves
- Búsqueda de claves
- Eliminación de claves
- Carga masiva de datos desde archivos CSV
- Generación gráfica del árbol mediante Graphviz

El proyecto fue desarrollado como parte del Proyecto Final del curso de Programación.

---

# Características Principales

✔ Configuración dinámica del grado del Árbol B  
✔ Inserción de datos  
✔ Búsqueda eficiente  
✔ Eliminación de claves  
✔ Recorrido ordenado del árbol  
✔ Carga masiva desde archivos CSV  
✔ Generación de imágenes del árbol en formato PNG  
✔ Implementación basada en Programación Orientada a Objetos  

---

# Tecnologías Utilizadas

- Python 3
- Graphviz
- Librería graphviz para Python

---

# Requisitos del Sistema

## Instalar Python

Descargar desde:

https://www.python.org/downloads/

Verificar instalación:

```bash
python --version
```

---

## Instalar Graphviz

Descargar desde:

https://graphviz.org/download/

IMPORTANTE:

Durante la instalación en Windows, agregar Graphviz al PATH del sistema.

---

## Instalar Librería Graphviz para Python

Ejecutar:

```bash
pip install graphviz
```

---

# Ejecución del Proyecto

Ubicarse en la carpeta del proyecto y ejecutar:

```bash
python arbol_b.py
```

---

# Menú del Sistema

El programa presenta el siguiente menú interactivo:

```text
1. Insertar clave
2. Buscar clave
3. Eliminar clave
4. Mostrar recorrido
5. Cargar datos desde CSV
6. Generar gráfica del árbol
7. Salir
```

---

# Uso del Sistema

## Insertar Clave

Permite agregar una nueva clave al Árbol B.

### Ejemplo

```text
Ingrese la clave: 50
✔ Clave insertada correctamente.
```

---

## Buscar Clave

Permite verificar si una clave existe dentro del árbol.

### Ejemplo

```text
Ingrese la clave a buscar: 30
✔ Clave encontrada.
```

---

## Eliminar Clave

Permite eliminar una clave del árbol.

### Ejemplo

```text
Ingrese la clave a eliminar: 20
✔ Operación completada.
```

---

## Mostrar Recorrido

Muestra las claves almacenadas en orden.

### Ejemplo

```text
10 20 30 40 50
```

---

# Carga de Archivos CSV

El sistema permite realizar inserciones masivas mediante archivos CSV.

## Instrucciones

1. Colocar los archivos CSV en la misma carpeta del programa.
2. Seleccionar la opción 5 del menú.
3. Ingresar el nombre del archivo.

### Ejemplo

```text
Ingrese el nombre del archivo CSV: datos1.csv
```

---

## Formato de los Archivos CSV

Los archivos deben contener números enteros separados por comas.

### Ejemplo

```csv
10,20,30,40,50
60,70,80,90,100
```

---

# Archivos CSV Incluidos

El proyecto incluye archivos CSV de prueba para validar estabilidad y carga masiva.

## Archivos

- datos1.csv
- datos2.csv

Cada archivo contiene mínimo 100 registros.

---

# Generación Gráfica del Árbol

El sistema utiliza Graphviz para generar una representación visual del Árbol B.

## Instrucciones

1. Seleccionar la opción 6.
2. Ingresar el nombre de la imagen.

### Ejemplo

```text
Ingrese nombre de la imagen: arbol
```

### Resultado

```text
✔ Imagen generada: arbol.png
```

---

# Estructura del Proyecto

```text
/Proyecto_ArbolB
│
├── arbol_b.py
├── datos1.csv
├── datos2.csv
├── README.md
├── Manual_Usuario.pdf
└── Manual_Tecnico.pdf
```

---

# Complejidad de Operaciones

| Operación | Complejidad |
|---|---|
| Búsqueda | O(log n) |
| Inserción | O(log n) |
| Eliminación | O(log n) |

---

# Integrantes

## Integrante 1

- Nombre: Pablo Andrés Say Oliva
- Carnet: 9490 – 24 – 19051
- Participación: 100%

---

## Integrante 2

- Nombre: Daniel Alexander Ovalle Estrada 
- Carnet: 9490 – 24 – 4830
- Participación: 100%

---

## Integrante 3

- Nombre: Jorge Mario Romualdo Castillo Jiménez
- Carnet: 9490 – 24 – 25738
- Participación: 100%

---

## Integrante 4

- Nombre: David Estuardo Arevalo Zeceña
- Carnet: 9490 – 24 – 5905
- Participación: 100%

---

# Observaciones

- El sistema acepta únicamente valores enteros.
- Los valores inválidos dentro de los archivos CSV son ignorados.
- Es obligatorio tener Graphviz instalado para generar imágenes.
