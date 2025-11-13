# 🚀 Despliegue del Backend en Render

## 📋 Pasos para desplegar en Render

### 1. **Preparar el repositorio**

El backend ya está configurado en la rama `backend`:
- ✅ `render.yaml` - Configuración para Render
- ✅ `Procfile` - Archivo para especificar comando de inicio
- ✅ `requirements.txt` - Dependencias Python actualizadas
- ✅ `Dockerfile` - Optimizado para Render
- ✅ `.gitignore` - Archivos ignorados

### 2. **Conectar GitHub con Render**

1. Ve a https://render.com
2. Haz login (o crea cuenta)
3. Click en "New +" → "Web Service"
4. Selecciona "Build and deploy from a Git repository"
5. Conecta tu cuenta de GitHub
6. Busca el repositorio: `EasyBraillev3`
7. Selecciona rama: `backend`
8. Click "Connect"

### 3. **Configurar el servicio en Render**

En la página de configuración del servicio:

| Campo | Valor |
|-------|-------|
| **Name** | `easybraille-backend` |
| **Environment** | `Docker` |
| **Plan** | `Free` (o Pro si quieres mejor performance) |
| **Root Directory** | Dejar vacío (raíz del repo) |

### 4. **Variables de entorno (Opcional)**

En "Environment", agrega si necesitas:
- `FLASK_ENV=production`
- `PYTHONUNBUFFERED=1`

### 5. **Deploy**

1. Click "Create Web Service"
2. Render construirá automáticamente el Docker
3. Esperará a que se complete la compilación (~3-5 min)
4. Tu backend estará disponible en: `https://easybraille-backend.onrender.com`

---

## 🔍 Verificar que funcione

```bash
# Probar el endpoint del backend
curl https://easybraille-backend.onrender.com/api/braille-image

# O desde JavaScript
fetch('https://easybraille-backend.onrender.com/api/braille-image', {
  method: 'POST',
  body: formData
})
```

---

## 📝 Estructura esperada por Render

```
EasyBraille-Backend/
├── backend/
│   ├── app.py              ← Main Flask app
│   ├── braille_detector.py
│   └── ...
├── Dockerfile              ← Para build en Render
├── render.yaml             ← Config de Render
├── Procfile                ← Comando de inicio
├── requirements.txt        ← Dependencias Python
└── .gitignore
```

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'backend'"

**Causa**: Flask no encuentra el módulo backend
**Solución**: Verificar que `app.py` está en `backend/app.py`

### Error: "Port already in use"

**Causa**: Puerto 8000 está ocupado
**Solución**: Render usa variables de entorno `$PORT`, ya está configurado

### Error: "CORS error cuando llama desde Frontend"

**Solución**: Agregar Frontend URL a CORS en `backend/app.py`:

```python
from flask_cors import CORS
import os

app = Flask(__name__)

# Configurar CORS para Render
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://easybraille-frontend.onrender.com",  # Tu frontend en Render
            "http://localhost:3000",  # Para desarrollo local
            "*"  # Para desarrollo - CAMBIAR EN PRODUCCIÓN
        ]
    }
})
```

### Error: "Build fails - not enough memory"

**Solución**: El plan Free tiene limitaciones. Opciones:
1. Usar plan Pro ($7/mes)
2. Optimizar dependencias (remover PyTorch si es posible)
3. Usar base de datos externa

---

## 📊 Monitoreo en Render

1. Abre tu servicio en Render
2. Ve a "Logs" para ver:
   - Logs de compilación
   - Logs de runtime
   - Errores y advertencias
3. Ve a "Metrics" para ver:
   - CPU usage
   - Memory usage
   - Request count

---

## 🔄 Actualizaciones futuras

Cada vez que hagas push a la rama `backend`:

```bash
git checkout backend
git commit -am "Cambios en backend"
git push origin backend
```

Render detectará automáticamente el cambio y hará redeploy. Puedes verlo en:
- Tab "Deploys" en Render
- Estado actual en tiempo real

---

## 📱 Conectar Frontend a Backend en Render

Cuando tengas el Frontend en Render también:

```typescript
// src/lib/api.ts
const BACKEND_URL = 
  process.env.NODE_ENV === 'production'
    ? 'https://easybraille-backend.onrender.com'
    : 'http://localhost:5000';

export async function detectBraille(image: File) {
  const formData = new FormData();
  formData.append('image', image);
  
  const response = await fetch(`${BACKEND_URL}/api/braille-image`, {
    method: 'POST',
    body: formData,
  });
  
  return response.json();
}
```

---

## ✅ Checklist

Antes de desplegar:

```
Backend Ready:
☐ Todos los archivos en rama 'backend'
☐ requirements.txt con todas las dependencias
☐ Dockerfile correcto
☐ render.yaml presente
☐ app.py en backend/app.py
☐ CORS configurado
☐ No hay archivos binarios grandes (.pt, .pkl)

En Render:
☐ Repositorio conectado
☐ Rama 'backend' seleccionada
☐ Variables de entorno configuradas
☐ Build exitoso
☐ Logs sin errores críticos
☐ Endpoint /api/braille-image responde
```

---

## 🎯 URL Final

Una vez desplegado, tu backend estará disponible en:

```
https://easybraille-backend.onrender.com
```

Desde Frontend (Next.js):

```typescript
const response = await fetch('https://easybraille-backend.onrender.com/api/braille-image', {
  method: 'POST',
  body: formData
});
```

---

**Creado**: 13 de Noviembre de 2025  
**Repositorio**: https://github.com/JesseAinsworth/EasyBraillev3.git  
**Rama**: backend
