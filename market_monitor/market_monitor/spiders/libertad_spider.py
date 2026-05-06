import scrapy
import json
from datetime import datetime

class LibertadSpider(scrapy.Spider):
    name = 'libertad_crawler'
    allowed_domains = ['www.hiperlibertad.com.ar']
    
    def start_requests(self):
        # Mapeo de rutas jerarquicas de la tienda para organizar la extraccion por rubro
        subcategorias = {
            "Vinagres": "vinagres",
            "Aceites de Oliva": "aceites-de-oliva",
            "Acetos": "acetos",
            "Aceites de Girasol": "aceites-de-girasol",
            "Otras variedades de aceites": "otras-variedades-de-aceites",
            "Aceites de Maíz": "aceites-de-maiz",
            "Aceites Mezcla": "aceites-mezcla"
        }

        for nombre_cat, path in subcategorias.items():
            # Consulta directa a la API de catalogo de VTEX usando los slugs de cada categoria
            # Se definen parametros de paginacion para obtener los primeros 50 productos
            url = f'https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/almacen/aceites-y-vinagres/{path}?_from=0&_to=49'
            yield scrapy.Request(url=url, callback=self.parse, meta={'subcat': nombre_cat})

    def parse(self, response):
        # Recuperacion de la subcategoria desde los metadatos de la peticion
        subcat_actual = response.meta.get('subcat')
        try:
            # Procesamiento de la respuesta JSON del servidor
            data = json.loads(response.text)
            if not data:
                return

            for prod in data:
                nombre = prod.get('productName', '').strip()
                items = prod.get('items', [])
                
                if items:
                    # Acceso a la oferta comercial para extraer el precio de venta vigente
                    sellers = items[0].get('sellers', [])
                    if sellers:
                        precio = sellers[0].get('commertialOffer', {}).get('Price', 0)
                        
                        # Estructuracion del item para su posterior procesamiento en el pipeline
                        if precio > 0:
                            yield {
                                'nombre': nombre,
                                'precio': float(precio),
                                'subcategoria': subcat_actual,
                                'tienda': 'Hiper Libertad',
                                'fecha_scraping': datetime.now().strftime('%Y-%m-%d')
                            }
            
            self.logger.info(f"Procesada subcategoria: {subcat_actual}")

        except Exception as e:
            self.logger.error(f"Error en parseo de subcategoria {subcat_actual}: {e}")

    # Configuracion del motor de descarga para mimetizar trafico humano y evitar bloqueos
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'DOWNLOAD_DELAY': 4,
    }