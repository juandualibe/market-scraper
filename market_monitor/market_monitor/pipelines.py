import pymongo
import os
from dotenv import load_dotenv

# --- CONFIGURACIÓN DE RUTA ---
# Ruta absoluta para evitar conflictos entre carpetas en Windows
dotenv_path = r"C:\Users\juand\OneDrive\Escritorio\market-scraper\.env"

# Cargamos el archivo .env centralizado
load_dotenv(dotenv_path=dotenv_path)

class MarketMonitorPipeline:
    def __init__(self):
        # Obtenemos la URI desde el entorno
        self.mongo_uri = os.getenv("MONGO_URI")
        
        # Validación de seguridad: si no hay URI, el proceso se detiene con aviso claro
        if not self.mongo_uri:
            raise ValueError(f"No se encontró MONGO_URI. Verificá que el archivo exista en: {dotenv_path}")
            
        try:
            # Inicializamos el cliente de MongoDB
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client["market_db"]
            self.collection = self.db["productos_tia"]
            print("Conexión establecida con Atlas usando .env")
        except Exception as e:
            print(f"Error de conexión inicial en Pipeline: {e}")
            raise

    def process_item(self, item, spider):
        # --- LÓGICA DE LIMPIEZA DE DATOS ---
        # Verificamos que el producto tenga un nombre válido y no sea basura del DOM
        nombre = item.get('nombre')
        precio = item.get('precio', 0)

        if not nombre or nombre == "Producto sin nombre" or precio == 0:
            # Logueamos el salto pero no lo guardamos en la base de datos
            spider.logger.warning(f"Saltando producto inválido o vacío: {nombre}")
            return item

        try:
            # Insertamos el documento limpio en la colección de Atlas
            self.collection.insert_one(dict(item))
        except Exception as e:
            spider.logger.error(f"Error al insertar ítem en MongoDB: {e}")
        
        return item