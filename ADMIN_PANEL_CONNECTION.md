# Conexión del Panel de Administración con el Backend

## 🎯 Resumen
Se han agregado los endpoints necesarios al backend para que el panel de administración del frontend pueda mostrar datos reales desde MongoDB.

## ✅ Endpoints Creados en el Backend

### 1. **GET /api/admin/stats**
Devuelve todas las estadísticas del dashboard

**Respuesta:**
```json
{
  "stats": {
    "users": {
      "total": 10,
      "active": 8,
      "admins": 2,
      "regular": 8,
      "last6Months": [
        {"_id": {"year": 2025, "month": 11}, "count": 5},
        {"_id": {"year": 2025, "month": 12}, "count": 5}
      ]
    },
    "translations": {
      "total": 50,
      "thisWeek": 12,
      "byType": [
        {"_id": "TEXT_TO_BRAILLE", "count": 30},
        {"_id": "BRAILLE_TO_TEXT", "count": 20}
      ],
      "last6Months": [
        {"_id": {"year": 2025, "month": 11}, "count": 25},
        {"_id": {"year": 2025, "month": 12}, "count": 25}
      ]
    },
    "ai": {
      "totalInteractions": 50,
      "avgAccuracy": 95.5,
      "avgResponseTime": 1.2,
      "successRate": 98.0
    }
  }
}
```

### 2. **GET /api/admin/users**
Lista todos los usuarios registrados

**Respuesta:**
```json
{
  "users": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "email": "usuario@example.com",
      "name": "Usuario",
      "role": "user",
      "isActive": true,
      "createdAt": "2025-12-04T10:00:00.000Z",
      "updatedAt": "2025-12-04T10:00:00.000Z"
    }
  ],
  "total": 1
}
```

### 3. **GET /api/admin/translations?limit=50**
Lista las traducciones más recientes

**Parámetros:**
- `limit` (opcional): Número máximo de traducciones a devolver (default: 50)

**Respuesta:**
```json
{
  "translations": [
    {
      "userId": "507f1f77bcf86cd799439011",
      "originalText": "Hola mundo",
      "brailleText": "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕",
      "translationType": "TEXT_TO_BRAILLE",
      "language": "es",
      "createdAt": "2025-12-04T10:00:00.000Z",
      "updatedAt": "2025-12-04T10:00:00.000Z"
    }
  ],
  "total": 1
}
```

### 4. **GET /api/admin/test-connection**
Prueba la conexión con la base de datos

**Respuesta:**
```json
{
  "connected": true,
  "message": "Conexión exitosa a MongoDB",
  "database": "easybraille"
}
```

## 🔧 Configuración del Frontend

El frontend ya está configurado para usar estos endpoints a través de rutas proxy en Next.js. Los archivos proxy están en:

- `src/app/api/admin/[...slug]/route.ts` - Proxy general para rutas admin
- `src/app/api/admin/test-connection/route.ts` - Endpoint específico de prueba

## 🚀 Pasos para Desplegar

### 1. Backend (Ya completado)
Los endpoints ya están agregados a `backend/app.py`. Solo necesitas:

```bash
# Desde el directorio del backend
git add .
git commit -m "Add admin panel endpoints"
git push origin main
```

Si estás usando Railway/Render, el backend se desplegará automáticamente.

### 2. Frontend

El frontend ya está configurado y debería funcionar automáticamente una vez que el backend esté desplegado. El archivo que carga las estadísticas es:

`src/app/admin/page.tsx` - Líneas 208-293

La función `loadStats()` llama a `/api/admin/stats` que es redirigida al backend.

## 🧪 Pruebas

### Probar Backend Directamente

```bash
# URL del backend en producción
BACKEND_URL="https://easybraillebackend-production.up.railway.app"

# Probar conexión
curl $BACKEND_URL/api/admin/test-connection

# Probar estadísticas
curl $BACKEND_URL/api/admin/stats

# Probar usuarios
curl $BACKEND_URL/api/admin/users

# Probar traducciones
curl $BACKEND_URL/api/admin/translations?limit=10
```

### Probar desde el Frontend

1. Iniciar sesión como administrador en el frontend
2. Navegar a `/admin`
3. El panel debería mostrar automáticamente los datos desde el backend
4. Usar el botón "Probar Conexión" para verificar el estado

## 📊 Estructura de Datos

### Usuarios en MongoDB
```javascript
{
  _id: ObjectId,
  email: String,
  password: String (hasheada),
  name: String,
  role: "user" | "admin",
  isActive: Boolean,
  createdAt: Date,
  updatedAt: Date
}
```

### Traducciones en MongoDB
```javascript
{
  userId: String,
  originalText: String,
  brailleText: String,
  translationType: "TEXT_TO_BRAILLE" | "BRAILLE_TO_TEXT",
  language: String,
  createdAt: Date,
  updatedAt: Date
}
```

## ❗ Importante

1. **CORS**: El backend ya está configurado con CORS para permitir peticiones desde `https://www.easy-braille.com`

2. **Variables de Entorno**: Asegúrate de que el backend tenga configurada la variable:
   ```
   MONGO_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/easybraille
   ```

3. **Proxy del Frontend**: El frontend usa la variable de entorno:
   ```
   NEXT_PUBLIC_API_URL=https://easybraillebackend-production.up.railway.app
   ```

## 🐛 Troubleshooting

### El panel muestra "Sin datos"

1. Verificar que el backend esté desplegado y funcionando
2. Probar los endpoints directamente con curl
3. Revisar los logs del backend
4. Usar el botón "Probar Conexión" en el panel

### Error 404 en los endpoints

1. Asegurarse de que el backend esté desplegado con los cambios más recientes
2. Verificar que la ruta sea correcta: `/api/admin/stats` (no `/admin/stats`)

### Error de CORS

1. Verificar que `ALLOWED_ORIGIN` en el backend incluya el dominio del frontend
2. Asegurarse de que los headers CORS estén correctamente configurados

## 📝 Próximos Pasos

Una vez desplegado el backend:

1. El panel de administración se conectará automáticamente
2. Verás datos reales en lugar del mensaje "Sin datos en la base de datos"
3. Las gráficas se llenarán con datos históricos
4. Las tablas de usuarios y traducciones mostrarán información real

---

**¿Necesitas ayuda?** Revisa los logs del backend y del frontend para ver mensajes de error detallados.
