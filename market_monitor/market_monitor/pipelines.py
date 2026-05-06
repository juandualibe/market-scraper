import pymongo
import os
from dotenv import load_dotenv

# Carga de configuración desde el entorno local
dotenv_path = r"C:\Users\juand\OneDrive\Escritorio\market-scraper\.env"
load_dotenv(dotenv_path=dotenv_path)

class MarketMonitorPipeline:
    def __init__(self):
        # Inicialización de la conexión con MongoDB Atlas
        self.mongo_uri = os.getenv("MONGO_URI")
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client["market_db"]
            self.collection = self.db["comparativa_precios_argentina"]
            
            # Definición de un índice único compuesto para evitar la duplicidad de registros.
            # Se asegura que la combinación de nombre y tienda sea irrepetible en la colección.
            self.collection.create_index([("nombre", 1), ("tienda", 1)], unique=True)
            
            print("Pipeline activo: Índice único verificado para deduplicación.")
        except Exception as e:
            print(f"Error de conexión en Pipeline: {e}")

    def process_item(self, item, spider):
        nombre = item.get('nombre')
        precio = item.get('precio', 0)
        tienda = item.get('tienda')

        # Lógica de normalización y limpieza de precios
        
        # 1. Corrección de magnitud: Si el precio es menor a 50, se ajusta por un factor
        # de 1000 para corregir valores expresados en centavos o escalas menores.
        if 0 < precio < 50:
            precio = precio * 1000
            item['precio'] = precio

        # 2. Filtrado por umbral mínimo: Se descartan ítems con precios inferiores a $500.
        # Esta regla elimina registros que representan datos obsoletos o errores de carga en origen.
        if precio < 500:
            spider.logger.warning(f"Item descartado por precio insuficiente: {nombre} (${precio})")
            return None 

        # Persistencia de datos mediante operación de reemplazo con inserción (Upsert)
        if nombre and precio > 0:
            try:
                # La operación replace_one garantiza que si el producto ya existe en la tienda,
                # se actualice con la información más reciente del scraping actual.
                self.collection.replace_one(
                    {"nombre": nombre, "tienda": tienda},
                    dict(item),
                    upsert=True
                )
            except Exception as e:
                spider.logger.error(f"Error durante la operación Upsert en MongoDB: {e}")
        
        return item

    def close_spider(self, spider):
        # Cierre ordenado de la conexión al finalizar la ejecución del spider
        self.client.close()