# 🔧 Variables de Entorno - EasyBraille Backend

## 📋 Variables Requeridas

### Existentes (Ya configuradas)

```env
# MongoDB Connection
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/easybraille

# Puerto (Railway lo asigna automáticamente)
PORT=8080
```

### Nuevas (Para recuperación de contraseña)

```env
# SendGrid API Key (Opcional pero recomendado para producción)
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxx
```

---

## 🚀 Configurar en Railway

### 1. Ir al Dashboard de Railway

1. Visita: https://railway.app/
2. Selecciona tu proyecto: **EasyBraille Backend**
3. Click en el servicio
4. Ve a la pestaña **Variables**

### 2. Agregar SENDGRID_API_KEY

**Opción A: Con SendGrid (Recomendado)**

1. Click en **New Variable**
2. Nombre: `SENDGRID_API_KEY`
3. Valor: `SG.xxxxxxxxxxxxxxxxxxxx` (tu API Key de SendGrid)
4. Click en **Add**
5. Railway reiniciará automáticamente el servicio

**Opción B: Sin SendGrid (Solo para testing)**

- No agregues la variable
- Los logs mostrarán el token de recuperación
- No se enviarán emails reales

### 3. Verificar Variables

Deberías ver:
```
✅ MONGO_URI
✅ PORT
✅ SENDGRID_API_KEY (si lo configuraste)
```

---

## 🔑 Obtener SendGrid API Key

### Paso 1: Crear Cuenta

1. Ve a: https://sendgrid.com/
2. Click en **Start for Free**
3. Completa el registro
4. Verifica tu email

### Paso 2: Generar API Key

1. Login en SendGrid
2. Ve a: **Settings** → **API Keys**
3. Click en **Create API Key**
4. Completa:
   - **API Key Name**: `EasyBraille-Production`
   - **API Key Permissions**: 
     - **Full Access** (más simple)
     - O **Restricted Access** → Solo **Mail Send** (más seguro)
5. Click en **Create & View**
6. **⚠️ IMPORTANTE**: Copia la API Key (solo se muestra una vez)
7. Guárdala temporalmente

### Paso 3: Verificar Email Sender

SendGrid requiere verificar el email desde el que enviarás:

1. Ve a: **Settings** → **Sender Authentication**
2. Click en **Get Started** en **Single Sender Verification**
3. Completa el formulario:
   ```
   From Name: EasyBraille
   From Email Address: noreply@easy-braille.com
   Reply To: support@easy-braille.com (opcional)
   Company Address: Tu dirección
   ```
4. Click en **Create**
5. Revisa tu email y verifica

**⚠️ IMPORTANTE**: Usa exactamente el mismo email (`noreply@easy-braille.com`) que configuraste en el código.

---

## 🧪 Verificar Configuración

### Sin SendGrid

```bash
# En Railway Logs deberías ver:
⚠️ SENDGRID_API_KEY no configurado, solo se mostrará el URL en logs
🔐 URL de recuperación para test@example.com: https://...
```

### Con SendGrid Configurado

```bash
# En Railway Logs deberías ver:
🔐 Token de recuperación generado para test@example.com
✅ Email de recuperación enviado a test@example.com (status: 202)
```

### Probar Envío de Email

```bash
curl -X POST https://easybraillebackend-production.up.railway.app/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email":"tu-email@example.com"}'
```

Revisa:
1. **Railway Logs**: Para ver si se envió
2. **Tu bandeja de entrada**: Para verificar llegada
3. **SendGrid Dashboard**: Stats → Activity

---

## 🔐 Seguridad

### Proteger API Keys

- ✅ **NUNCA** subas API Keys a GitHub
- ✅ Usa variables de entorno
- ✅ Rota las keys periódicamente
- ✅ Usa permisos restringidos cuando sea posible

### Rotar API Key

Si tu API Key se compromete:

1. Ve a SendGrid → Settings → API Keys
2. Localiza la key comprometida
3. Click en **Delete**
4. Crea una nueva key
5. Actualiza la variable en Railway

---

## 🎯 Límites y Cuotas

### Plan Gratuito de SendGrid

- **100 emails/día** (suficiente para empezar)
- Verificación de dominio no requerida (con Single Sender)
- Sin tarjeta de crédito

### Monitorear Uso

1. SendGrid Dashboard → **Stats**
2. Ver emails enviados hoy
3. Alertas si te acercas al límite

### Upgrade (Opcional)

Si necesitas más:
- **Essentials**: $19.95/mes → 50,000 emails/mes
- **Pro**: $89.95/mes → 100,000 emails/mes

---

## 📊 Testing Local

### Archivo .env (Local)

```bash
# Crear archivo .env en la raíz del proyecto
touch .env
```

```env
# .env
MONGO_URI=mongodb+srv://...
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxx
PORT=8080
```

### Cargar variables en Python

El código ya está configurado para leer `os.environ.get()`, que toma variables de:
- Railway (producción)
- `.env` (local, si usas `python-dotenv`)

### Ejecutar localmente

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python backend/app.py
```

---

## ⚙️ Variables Adicionales (Futuras)

Si quieres expandir la funcionalidad:

```env
# Rate Limiting
MAX_RESET_ATTEMPTS=5
RESET_COOLDOWN_MINUTES=15

# Token Expiration
RESET_TOKEN_EXPIRY_HOURS=1

# Email Templates
SENDGRID_TEMPLATE_ID=d-xxxxxxxxxxxxxxxxxxxx

# Frontend URL (por si cambia)
FRONTEND_URL=https://www.easy-braille.com

# SMTP Alternativo (si no usas SendGrid)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=tu-email@gmail.com
EMAIL_PASSWORD=tu-app-password
```

---

## 📝 Resumen de Variables

| Variable | Requerida | Valor | Donde |
|----------|-----------|-------|-------|
| `MONGO_URI` | ✅ | `mongodb+srv://...` | Railway |
| `PORT` | ✅ | `8080` | Railway (auto) |
| `SENDGRID_API_KEY` | ⚠️ Opcional | `SG.xxx` | Railway |

**⚠️ Opcional** = Funciona sin ella, pero con funcionalidad limitada

---

## 🆘 Problemas Comunes

### Error: "SendGrid API Key inválido"

**Solución**: Verifica que la key sea correcta y tenga permisos de **Mail Send**

### Error: "Email not verified"

**Solución**: Verifica el email sender en SendGrid Dashboard

### Emails van a spam

**Solución**: 
- Usa Domain Authentication (avanzado)
- Pide a los usuarios agregar a contactos
- Verifica SPF/DKIM records

---

**Última actualización**: Noviembre 21, 2025  
**Versión**: 1.0
