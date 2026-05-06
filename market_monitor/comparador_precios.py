import pymongo
import os
from dotenv import load_dotenv
import pandas as pd
from thefuzz import process, fuzz

# Carga de las variables de entorno desde el archivo .env ubicado en la raíz
dotenv_path = r"C:\Users\juand\OneDrive\Escritorio\market-scraper\.env"
load_dotenv(dotenv_path=dotenv_path)

def comparar_precios():
    # Configuración de la conexión a MongoDB y acceso a la colección de precios
    mongo_uri = os.getenv("MONGO_URI")
    client = pymongo.MongoClient(mongo_uri)
    db = client["market_db"]
    collection = db["comparativa_precios_argentina"]

    # Conversión de los documentos de la base de datos a un DataFrame de Pandas para su manipulación
    df = pd.DataFrame(list(collection.find({}, {"_id": 0})))
    if df.empty:
        print("La base de datos está vacía.")
        return

    # Segmentación del conjunto de datos por tienda para realizar la comparación cruzada
    vea = df[df['tienda'] == 'Vea Digital'].copy()
    libertad = df[df['tienda'] == 'Hiper Libertad'].copy()

    resultados = []

    print("\nBuscando coincidencias mediante logica difusa entre Vea y Libertad...")

    # Iteración sobre los productos de la primera tienda para buscar sus pares en la segunda
    for index, row_vea in vea.iterrows():
        # Uso de thefuzz para encontrar el producto con el nombre más similar en la lista de Libertad
        # Se utiliza token_set_ratio para ignorar diferencias en el orden de las palabras
        match = process.extractOne(row_vea['nombre'], libertad['nombre'].tolist(), scorer=fuzz.token_set_ratio)
        
        # Se establece un umbral de similitud del 80% para validar que se trata del mismo producto
        if match and match[1] >= 80:
            nombre_libertad = match[0]
            row_libertad = libertad[libertad['nombre'] == nombre_libertad].iloc[0]
            
            # Cálculo de métricas de comparación y ahorro
            resultados.append({
                'Producto': row_vea['nombre'],
                'Precio Vea': row_vea['precio'],
                'Precio Libertad': row_libertad['precio'],
                'Diferencia': round(row_vea['precio'] - row_libertad['precio'], 2),
                'Más Barato': 'Libertad' if row_libertad['precio'] < row_vea['precio'] else 'Vea',
                'Similitud %': match[1]
            })

    # Estructuración final de los resultados obtenidos
    df_res = pd.DataFrame(resultados)
    
    print("\n--- REPORTE DE COMPARATIVA MARKET MONITOR ---")
    if df_res.empty:
        print("No se encontraron coincidencias suficientes. Revisar consistencia de datos en Atlas.")
    else:
        # Presentación de resultados ordenados por el nivel de precisión en la coincidencia
        print(df_res.sort_values(by='Similitud %', ascending=False).to_string(index=False))

if __name__ == "__main__":
    comparar_precios()