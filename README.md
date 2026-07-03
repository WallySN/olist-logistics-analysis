# Proyecto Olist - Análisis de Logística E-Commerce

## 📥 Descarga de Datos

Dataset original: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

### Pasos para descargar:
1. Crear cuenta gratis en [Kaggle](https://www.kaggle.com)
2. Ir al link de arriba
3. Hacer clic en **"Download"** (botón verde)
4. Descomprimir `archive.zip`
5. Crear carpeta `C:\data\olist\archive\`
6. Pegar los 9 archivos CSV ahí

---

## 🛠️ Instalación de Herramientas

| Herramienta | Link de descarga |
|-------------|------------------|
| MySQL + Workbench | https://dev.mysql.com/downloads/installer/ |
| Python | https://python.org/downloads/ |
| VS Code | https://code.visualstudio.com/download |
| Power BI | https://powerbi.microsoft.com/desktop/ |

---

## 🚀 Pasos para ejecutar el proyecto

### 1. Clonar repositorio
```bash
git clone https://github.com/WallySN/olist-logistics-analysis.git
cd olist-logistics-analysis
2. Crear base de datos en MySQL Workbench
sql
CREATE DATABASE olist_db;
USE olist_db;
Ejecutar las queries del archivo sql/queries_analisis.sql para crear las 9 tablas.
3. Configurar contraseña
Abrir scripts/import_olist.py y cambiar:
Python
PASSWORD = "TU_PASSWORD_AQUI"
Poner tu contraseña real de MySQL root.
4. Instalar librerías de Python
bash
pip install pandas sqlalchemy mysql-connector-python
5. Importar datos
bash
cd scripts
python import_olist.py
6. Verificar
Abrir MySQL Workbench → olist_db → SHOW TABLES;
📊 Datos incluidos
Table
Tabla	Registros	Descripción
customers	99,441	Clientes
orders	99,441	Órdenes
order_items	112,650	Items por orden
order_payments	103,886	Pagos
order_reviews	99,224	Reviews
products	32,951	Productos
sellers	3,095	Vendedores
geolocation	1,000,163	Geolocalización
category_translation	71	Traducción de categorías
