require('dotenv').config({ path: '../.env' }); 

const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();

// Middleware para habilitar CORS y procesamiento de JSON
app.use(cors());
app.use(express.json());

// Verificación de que la cadena de conexión a la base de datos esté presente
if (!process.env.MONGO_URI) {
    console.error("Error: MONGO_URI no definida en el archivo .env");
    process.exit(1);
}

// Configuración de la conexión a MongoDB Atlas apuntando a la base de datos market_db
mongoose.connect(process.env.MONGO_URI, { dbName: 'market_db' })
    .then(() => console.log('API conectada a MongoDB Atlas'))
    .catch(err => console.error('Error de conexión en la base de datos:', err));

// Definición del esquema y mapeo a la colección de la comparativa
const ProductoSchema = new mongoose.Schema({
    nombre: String,
    precio: Number,
    tienda: String,
    subcategoria: String,
    fecha_scraping: String
}, { collection: 'comparativa_precios_argentina' });

const Producto = mongoose.model('Producto', ProductoSchema);

// Rutas de la API

// Obtiene la lista completa de productos ordenados de menor a mayor precio
app.get('/api/productos', async (req, res) => {
    try {
        const productos = await Producto.find().sort({ precio: 1 });
        res.json(productos);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Busca productos por nombre utilizando expresiones regulares para permitir coincidencias parciales
app.get('/api/productos/buscar', async (req, res) => {
    const term = req.query.q;
    try {
        const productos = await Producto.find({ 
            nombre: { $regex: term, $options: 'i' } 
        }).sort({ precio: 1 });
        res.json(productos);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Filtra los productos según el nombre específico de la tienda
app.get('/api/productos/tienda', async (req, res) => {
    const tiendaNombre = req.query.name;
    try {
        const productos = await Producto.find({ tienda: tiendaNombre });
        res.json(productos);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Configuración del puerto y puesta en marcha del servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor escuchando en puerto ${PORT}`);
});