# 📚 Ejemplos de Uso - API de Recuperación de Contraseña

## 🔥 Casos de Uso Reales

### Caso 1: Usuario olvidó su contraseña

**Frontend (React):**
```javascript
const handleForgotPassword = async (email) => {
  try {
    const response = await fetch('/api/auth/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Mostrar mensaje exitoso
      toast.success('Revisa tu correo para restablecer tu contraseña');
    } else {
      toast.error(data.error || 'Error al enviar correo');
    }
  } catch (error) {
    toast.error('Error de conexión');
  }
};
```

**Backend Response:**
```json
{
  "message": "Se ha enviado un correo con instrucciones de recuperación"
}
```

---

### Caso 2: Usuario hace clic en el link del email

El usuario recibe un email con:
```
https://www.easy-braille.com/reset-password?token=AbCdEf123456789...
```

El frontend extrae el token de la URL:
```javascript
const searchParams = new URLSearchParams(window.location.search);
const token = searchParams.get('token');
```

---

### Caso 3: Usuario ingresa nueva contraseña

**Frontend (React):**
```javascript
const handleResetPassword = async (token, newPassword) => {
  try {
    const response = await fetch('/api/auth/reset-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        token, 
        newPassword 
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      toast.success('Contraseña actualizada exitosamente');
      // Redirigir a login
      navigate('/login');
    } else {
      toast.error(data.error || 'Error al restablecer contraseña');
    }
  } catch (error) {
    toast.error('Error de conexión');
  }
};
```

**Backend Response (exitoso):**
```json
{
  "message": "Contraseña actualizada correctamente"
}
```

**Backend Response (error):**
```json
{
  "error": "Token inválido o expirado"
}
```

---

## 🧪 Testing con Python

### Test 1: Solicitar recuperación

```python
import requests
import json

url = "https://easybraillebackend-production.up.railway.app/api/auth/forgot-password"
payload = {"email": "test@example.com"}

response = requests.post(url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

**Output esperado:**
```
Status: 200
Response: {'message': 'Se ha enviado un correo con instrucciones de recuperación'}
```

### Test 2: Restablecer con token

```python
import requests

url = "https://easybraillebackend-production.up.railway.app/api/auth/reset-password"
payload = {
    "token": "tu-token-aqui",
    "newPassword": "nuevaPassword123"
}

response = requests.post(url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

**Output esperado:**
```
Status: 200
Response: {'message': 'Contraseña actualizada correctamente'}
```

---

## 🔍 Testing con JavaScript (Node.js)

```javascript
// forgot-password.js
const fetch = require('node-fetch');

async function testForgotPassword() {
  const response = await fetch(
    'https://easybraillebackend-production.up.railway.app/api/auth/forgot-password',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'test@example.com' })
    }
  );
  
  const data = await response.json();
  console.log('Status:', response.status);
  console.log('Response:', data);
}

testForgotPassword();
```

---

## 📊 Flujo Completo

```
1. Usuario → Frontend → POST /api/auth/forgot-password
   ↓
2. Backend genera token y lo guarda en MongoDB
   ↓
3. Backend envía email con link (via SendGrid)
   ↓
4. Usuario hace clic en link del email
   ↓
5. Frontend extrae token de la URL
   ↓
6. Usuario ingresa nueva contraseña
   ↓
7. Frontend → Backend → POST /api/auth/reset-password
   ↓
8. Backend valida token, actualiza contraseña
   ↓
9. Backend elimina token de la BD
   ↓
10. Usuario puede hacer login con nueva contraseña
```

---

## ⚠️ Casos de Error

### Error 1: Email no existe
```json
// Request
{ "email": "noexiste@example.com" }

// Response (200 OK - por seguridad)
{ "message": "Si el correo existe, recibirás instrucciones de recuperación" }
```

### Error 2: Token expirado
```json
// Request
{ 
  "token": "token-viejo",
  "newPassword": "nueva123"
}

// Response (400 Bad Request)
{ "error": "Token inválido o expirado" }
```

### Error 3: Contraseña muy corta
```json
// Request
{ 
  "token": "token-valido",
  "newPassword": "12345"
}

// Response (400 Bad Request)
{ "error": "La contraseña debe tener al menos 6 caracteres" }
```

### Error 4: Falta token
```json
// Request
{ "newPassword": "nueva123" }

// Response (400 Bad Request)
{ "error": "Token y contraseña requeridos" }
```

---

## 🔐 Verificación en MongoDB

### Ver tokens activos
```javascript
// MongoDB Shell
use easybraille
db.users.find(
  { resetPasswordToken: { $exists: true } },
  { email: 1, resetPasswordExpires: 1, resetPasswordToken: 1 }
)
```

### Verificar expiración
```javascript
db.users.find({
  resetPasswordExpires: { $lt: new Date() }
})
```

### Limpiar tokens manualmente
```javascript
db.users.updateMany(
  {},
  { $unset: { resetPasswordToken: "", resetPasswordExpires: "" } }
)
```

---

## 🚀 Integración con el Frontend Existente

El frontend ya tiene estos archivos configurados:

1. **`src/pages/ResetPassword.tsx`**
   - Maneja la UI de recuperación
   - Dos formularios: solicitar token + ingresar nueva contraseña

2. **Proxy API** (`/api/auth/forgot-password`, `/api/auth/reset-password`)
   - Ya configurado para redirigir al backend

3. **No se requieren cambios adicionales en el frontend** ✅

---

## 📧 Contenido del Email

El usuario recibirá un email HTML con:

- **Asunto**: "Recuperación de contraseña - EasyBraille"
- **From**: noreply@easy-braille.com
- **Botón**: "Restablecer Contraseña" (azul, centrado)
- **Link alternativo**: URL completa por si el botón no funciona
- **Advertencia**: "Este enlace expirará en 1 hora"
- **Nota de seguridad**: "Si no solicitaste esto, ignora este correo"

---

## 🎯 Checklist de Verificación

Antes de considerar completa la implementación:

- [ ] `requirements.txt` actualizado con `sendgrid`
- [ ] Endpoints agregados al `backend/app.py`
- [ ] Variable `SENDGRID_API_KEY` configurada en Railway
- [ ] Email verificado en SendGrid (Single Sender)
- [ ] Probado con usuario real
- [ ] Email recibido correctamente
- [ ] Token válido restablece la contraseña
- [ ] Token expirado muestra error apropiado
- [ ] Nueva contraseña funciona en login

---

**Documentación creada**: Noviembre 21, 2025  
**Para**: EasyBraille Backend  
**Versión**: 1.0
