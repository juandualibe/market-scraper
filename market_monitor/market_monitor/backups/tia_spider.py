import scrapy

class TiaSpider(scrapy.Spider):
    name = 'tia_crawler'
    # URL de la categoría para extraer los productos
    start_urls = ['https://www.tia.com.ec/despensa/aceites']

    def parse(self, response):
        # Seleccionamos cada contenedor de producto en la lista
        for producto in response.css('li.product-item'):
            
            # --- TRATAMIENTO DEL NOMBRE ---
            # Extraemos el nombre y validamos que no sea None antes de usar .strip()
            nombre_raw = producto.css('.product-item-link::text').get()
            nombre_final = nombre_raw.strip() if nombre_raw else "Producto sin nombre"

            # --- LIMPIEZA DE PRECIOS (Transformación a Float) ---
            # Extraemos el texto del precio (ej: "$6,79")
            precio_raw = producto.css('.price::text').get()
            
            # Lo transformamos a float (6.79) para que sea útil en MongoDB Atlas
            precio_final = 0.0
            if precio_raw:
                try:
                    # Quitamos el $, cambiamos la coma por punto y limpiamos espacios
                    precio_final = float(precio_raw.replace('$', '').replace(',', '.').strip())
                except ValueError:
                    # Si el formato es inesperado, asignamos 0.0 para no romper el proceso
                    precio_final = 0.0

            # --- GENERACIÓN DEL ITEM ---
            yield {
                'nombre': nombre_final,
                'precio': precio_final,
                'sku': producto.css('.product-item-info::attr(data-product-id)').get(),
                'fecha_scraping': '2026-05-06' # Fecha actual para el historial
            }

        # --- LÓGICA DE PAGINACIÓN ---
        # Buscamos el enlace de "Siguiente" en el DOM
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            # Seguimos el enlace de forma recursiva llamando a esta misma función
            yield response.follow(next_page, self.parse)