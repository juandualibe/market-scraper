import scrapy
import json
from datetime import datetime

class VeaSpider(scrapy.Spider):
    name = 'vea_crawler'
    allowed_domains = ['www.vea.com.ar']
    
    def __init__(self, *args, **kwargs):
        super(VeaSpider, self).__init__(*args, **kwargs)
        # Estructura de datos para asegurar la unicidad de los productos durante la ejecucion
        self.nombres_vistos = set()

    def start_requests(self):
        # Mapeo de categorias especificas segun la estructura de navegacion de la tienda
        subcategorias = {
            "Aceites Comunes": "Aceites/Comunes",
            "Aceites Especiales": "Aceites/Especiales",
            "Acetos": "Acetos",
            "Jugos de Limón": "Jugos-de-Limon",
            "Vinagres": "Vinagres"
        }

        for nombre_cat, path in subcategorias.items():
            # Construccion de peticiones hacia la API de catalogo de la plataforma
            url = f'https://www.vea.com.ar/api/catalog_system/pub/products/search/Almacen/Aceites-y-Vinagres/{path}?_from=0&_to=49'
            yield scrapy.Request(url=url, callback=self.parse, meta={'subcat': nombre_cat})

    def parse(self, response):
        try:
            # Procesamiento de la respuesta en formato JSON
            data = json.loads(response.text)
            if not data:
                return

            for prod in data:
                nombre = prod.get('productName', '').strip()
                nombre_norm = nombre.lower()

                # Control de redundancia para evitar el procesamiento de productos duplicados en distintas categorias
                if nombre_norm in self.nombres_vistos:
                    continue 
                
                self.nombres_vistos.add(nombre_norm)

                items = prod.get('items', [])
                if items:
                    # Extraccion del precio de venta desde la oferta comercial del primer item
                    sellers = items[0].get('sellers', [])
                    if sellers:
                        precio = sellers[0].get('commertialOffer', {}).get('Price', 0)
                        
                        # Generacion del objeto de datos normalizado para el pipeline
                        if precio > 0:
                            yield {
                                'nombre': nombre,
                                'precio': float(precio),
                                'subcategoria': response.meta.get('subcat'),
                                'tienda': 'Vea Digital',
                                'fecha_scraping': datetime.now().strftime('%Y-%m-%d')
                            }
            
            self.logger.info(f"Cantidad de items unicos procesados: {len(self.nombres_vistos)}")

        except Exception as e:
            self.logger.error(f"Error en el procesamiento de datos JSON: {e}")

    # Configuracion de las politicas de descarga para mantener la persistencia y evitar bloqueos
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'DOWNLOAD_DELAY': 2,
    }