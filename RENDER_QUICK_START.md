# 🚀 RENDER DEPLOY - GUÍA RÁPIDA

## En 5 minutos

### 1️⃣ Ve a https://render.com

Haz login o crea cuenta (puedes usar GitHub)

### 2️⃣ New Web Service

- Click "New +" → "Web Service"
- "Build and deploy from a Git repository"
- Conecta GitHub si no está conectado
- Selecciona repo: `EasyBraillev3`
- Rama: `backend`

### 3️⃣ Configura el servicio

```
Name: easybraille-backend
Environment: Docker
Plan: Free (o Pro para mejor performance)
```

### 4️⃣ Click "Create Web Service"

Render hará todo automáticamente:
- Descargará el código
- Construirá la imagen Docker
- Desplegará

**⏱️ Espera 3-5 minutos**

### 5️⃣ ¡Listo! 

Tu backend estará en:
```
https://easybraille-backend.onrender.com
```

---

## ✅ Verificar que funcione

Abre en el navegador:
```
https://easybraille-backend.onrender.com/
```

Deberías ver:
```json
{
  "status": "ok",
  "service": "EasyBraille Backend",
  "environment": "production"
}
```

---

## 🔗 Conectar con Frontend

Cuando tengas el Frontend también en Render, usa:

```typescript
const API_URL = 'https://easybraille-backend.onrender.com';

const response = await fetch(`${API_URL}/api/braille-image`, {
  method: 'POST',
  body: formData
});
```

---

## 📊 Ver logs

1. Abre tu servicio en Render
2. Tab "Logs"
3. Podrás ver:
   - Compilación
   - Errores
   - Requests

---

## 🔄 Actualizaciones

Cada vez que hagas push a la rama `backend`:

```bash
git push origin backend
```

Render detecta automáticamente y redeploya en ~2-3 minutos.

---

**Archivos creados para Render:**
- ✅ `render.yaml` - Configuración de Render
- ✅ `Dockerfile` - Imagen Docker optimizada
- ✅ `Procfile` - Comando de inicio
- ✅ `requirements.txt` - Dependencias actualizadas
- ✅ `backend/config.py` - Configuración para producción
- ✅ `backend/app_render.py` - App mejorada con logs
- ✅ `RENDER_DEPLOY.md` - Guía completa

**¡Todo listo para desplegar!**
