# Market Monitor - Web Scraper & API REST

> 🚧 **Estado:** En desarrollo activo.

Este proyecto es un ecosistema en desarrollo de ingeniería de datos, diseñado para la extracción, normalización y exposición de precios de e-commerce en Córdoba, Argentina. Permite el monitoreo y la comparación de brechas de precios entre grandes cadenas de retail de forma automatizada.

## Arquitectura del Sistema

El sistema se divide en tres grandes módulos que interactúan mediante una base de datos centralizada:

1. **Módulo de Extracción (Python & Scrapy):**
   - **Crawler Multi-Store:** Spiders optimizados para navegar el catálogo de supermercados (Vea e Hiper Libertad).
   - **Bypass de seguridad:** Implementación de User-Agents reales y manejo de tiempos de espera para asegurar la recolección de datos públicos.
   - **ETL Pipeline:** Transformación de datos crudos a tipos numéricos, normalización de precios mediante multiplicadores dinámicos y filtros de limpieza para descartar registros obsoletos.

2. **Módulo de API (Node.js & Express):**
   - Servidor REST que expone los datos capturados mediante Mongoose.
   - **Buscador Inteligente:** Endpoints con soporte para búsqueda por expresiones regulares (Regex).
   - **CORS Habilitado:** Configuración para el consumo de datos desde clientes web y aplicaciones móviles.

3. **Módulo de Análisis y Frontend:**
   - **Comparador de Precios:** Lógica de negocio para el cruce de productos entre distintas tiendas.
   - **Dashboard de Visualización:** Interfaz reactiva construida con HTML5 y Tailwind CSS para el monitoreo de estadísticas y búsqueda de productos en tiempo real.

## Stack Tecnológico

- **Python 3.8+** (Scrapy, Pymongo)
- **Node.js** (Express, Mongoose)
- **MongoDB Atlas** (NoSQL Database)
- **Frontend:** Tailwind CSS

## Endpoints

- `GET /api/productos` — Lista completa de productos unificados y normalizados.
- `GET /api/productos/buscar?q=X` — Filtra productos por coincidencia de nombre.
- `GET /api/productos/tienda?name=X` — Filtra el catálogo por una tienda específica.

## Validación y Calidad de Datos

- **Filtro de Umbral:** Se implementó una validación mínima de $500 ARS para neutralizar errores de indexación en las APIs de origen y garantizar la veracidad de la información.
- **Deduplicación:** Gestión de claves únicas para evitar la duplicidad de ítems en la base de datos central.

## Configuración Local y Ejecución

### 1. Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto (`market-scraper/`) con el siguiente contenido:

```env
MONGO_URI=tu_cadena_de_conexion_mongodb_atlas
PORT=3000
```

### 2. Instalación de Dependencias

```bash
# Python
cd market_monitor && pip install -r requirements.txt

# Node.js
cd api && npm install
```

### 3. Comandos de Ejecución

```bash
# Actualizar catálogo Vea
cd market_monitor && scrapy crawl vea_crawler

# Actualizar catálogo Libertad
cd market_monitor && scrapy crawl libertad_crawler

# Iniciar servidor API
cd api && node server.js
```