# Market Monitor - Web Scraper & API REST

Este proyecto es un ecosistema completo de ingeniería de datos diseñado para la extracción, normalización y exposición de precios de e-commerce.

## Arquitectura del Sistema
El sistema se divide en dos grandes módulos que interactúan mediante una base de datos centralizada:

1. **Módulo de Extracción (Python & Scrapy):**
    * Spider optimizada para navegar el catálogo de supermercados (ej. Tía).
    * **Bypass de seguridad:** Implementación de User-Agents reales y manejo de `robots.txt` para asegurar la recolección de datos públicos.
    * **ETL Pipeline:** Transformación de datos crudos (strings de moneda) a tipos numéricos (`float`) y limpieza de valores nulos antes de la carga.

2. **Módulo de API (Node.js & Express):**
    * Servidor REST que expone los datos capturados.
    * Conexión segura a **MongoDB Atlas** mediante Mongoose.
    * Endpoints con capacidades de filtrado dinámico por precio.

## Stack Tecnológico
* **Python 3.x** (Scrapy, Pymongo)
* **Node.js** (Express, Mongoose)
* **MongoDB Atlas** (NoSQL Database)

## Endpoints
* `GET /api/productos`: Lista completa de productos scrapeados.
* `GET /api/productos/baratos?max=X`: Filtra productos con precio menor o igual a X.

## Consideraciones de Ciberdefensa
Se implementó un `DOWNLOAD_DELAY` de 2 segundos para evitar la saturación de los servidores objetivo y un manejo de excepciones para garantizar la resiliencia del scraper ante cambios en la estructura del DOM.

## Configuración Local

1. **Variables de Env**: Crear un archivo `.env` en la raíz del proyecto (`market-scraper/`) con el siguiente contenido:
   
   MONGO_URI=tu_cadena_de_conexion_mongodb_atlas
   PORT=3000

2. **Ejecución**:
   * **Módulo Scraper**: cd market_monitor && scrapy crawl tia_crawler
   * **Módulo API**: cd api && node server.js