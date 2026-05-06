// Le indicamos que el .env está un nivel arriba de la carpeta /api
require('dotenv').config({ path: '../.env' }); 

const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Verificación de carga de variable (útil para debug)
if (!process.env.MONGO_URI) {
    console.error("ERROR: MONGO_URI no definida en el archivo .env");
    process.exit(1);
}

// Conexión a MongoDB Atlas
mongoose.connect(process.env.MONGO_URI, { dbName: 'market_db' })
    .then(() => console.log('API conectada a MongoDB Atlas'))
    .catch(err => console.error('Error de conexión en API:', err));

// Esquema del producto
const ProductoSchema = new mongoose.Schema({
    nombre: String,
    precio: Number,
    sku: String,
    fecha_scraping: String
}, { collection: 'productos_tia' });

const Producto = mongoose.model('Producto', ProductoSchema);

// --- ENDPOINTS ---

// 1. Obtener todos los productos
app.get('/api/productos', async (req, res) => {
    try {
        const productos = await Producto.find().sort({ precio: 1 });
        res.json(productos);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 2. Filtrar por precio (Ej: /api/productos/baratos?max=2.5)
app.get('/api/productos/baratos', async (req, res) => {
    const maxPrecio = req.query.max || 2.5;
    try {
        const productos = await Producto.find({ precio: { $lte: parseFloat(maxPrecio) } });
        res.json(productos);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`API corriendo en http://localhost:${PORT}`);
});