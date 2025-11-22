# 🔐 Configuración de Recuperación de Contraseña

## ✅ Implementación Completada

Se han agregado los siguientes endpoints al backend:

### 1. POST `/api/auth/forgot-password`
Solicita un token de recuperación de contraseña.

**Request:**
```json
{
  "email": "usuario@example.com"
}
```

**Response:**
```json
{
  "message": "Se ha enviado un correo con instrucciones de recuperación"
}
```

### 2. POST `/api/auth/reset-password`
Restablece la contraseña usando el token recibido.

**Request:**
```json
{
  "token": "token-de-recuperacion",
  "newPassword": "nuevaPassword123"
}
```

**Response:**
```json
{
  "message": "Contraseña actualizada correctamente"
}
```

---

## 📧 Configuración de Email (SendGrid)

### Paso 1: Crear cuenta en SendGrid

1. Visita [SendGrid](https://sendgrid.com/)
2. Crea una cuenta gratuita (incluye 100 emails/día)
3. Verifica tu email

### Paso 2: Crear API Key

1. Ve a **Settings** → **API Keys**
2. Click en **Create API Key**
3. Nombre: `EasyBraille-PasswordReset`
4. Permisos: **Full Access** o **Mail Send** (restringido)
5. Copia la API Key generada (solo se muestra una vez)

### Paso 3: Verificar dominio/email (Importante)

SendGrid requiere verificación para enviar emails:

**Opción A: Single Sender Verification (Más rápido)**
1. Ve a **Settings** → **Sender Authentication**
2. Click en **Verify a Single Sender**
3. Completa el formulario con:
   - From Email Address: `noreply@easy-braille.com`
   - From Name: `EasyBraille`
4. Verifica el email de confirmación

**Opción B: Domain Authentication (Profesional)**
1. Ve a **Settings** → **Sender Authentication**
2. Click en **Authenticate Your Domain**
3. Sigue las instrucciones para agregar registros DNS

### Paso 4: Configurar variable de entorno en Railway

1. Ve a tu proyecto en [Railway](https://railway.app/)
2. Selecciona tu servicio backend
3. Ve a la pestaña **Variables**
4. Agrega nueva variable:
   ```
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxx
   ```
5. Click en **Deploy** (se reiniciará automáticamente)

---

## 🧪 Testing

### Probar sin SendGrid configurado

Si no configuras `SENDGRID_API_KEY`, el sistema funcionará en modo desarrollo:
- Los tokens se generarán correctamente
- El URL de recuperación se mostrará en los logs
- NO se enviará email real

### Ver logs en Railway

```bash
# En Railway Dashboard → Deployments → View Logs
```

Busca líneas como:
```
🔐 Token de recuperación generado para usuario@example.com
⚠️ SENDGRID_API_KEY no configurado, solo se mostrará el URL en logs
🔐 URL de recuperación: https://www.easy-braille.com/reset-password?token=...
```

### Prueba manual con cURL

**1. Solicitar recuperación:**
```bash
curl -X POST https://easybraillebackend-production.up.railway.app/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\"}"
```

**2. Copiar token de los logs**

**3. Restablecer contraseña:**
```bash
curl -X POST https://easybraillebackend-production.up.railway.app/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d "{\"token\":\"EL-TOKEN-COPIADO\",\"newPassword\":\"nuevaPass123\"}"
```

### Prueba desde el Frontend

1. Ve a https://www.easy-braille.com/reset-password
2. Ingresa un email registrado
3. Si SendGrid está configurado: revisa tu bandeja de entrada
4. Si NO está configurado: revisa los logs de Railway
5. Copia el token y completa el formulario

---

## 🔒 Características de Seguridad

✅ **Tokens seguros**: Generados con `secrets.token_urlsafe(32)`  
✅ **Expiración**: Los tokens expiran después de 1 hora  
✅ **No revelar usuarios**: El endpoint no indica si el email existe  
✅ **Hashing bcrypt**: Las contraseñas se hashean antes de guardar  
✅ **Limpieza de tokens**: Los tokens usados se eliminan de la BD  
✅ **Validación**: Contraseñas mínimo 6 caracteres  

---

## 📊 Monitoreo

### Ver actividad de recuperación de contraseña

En MongoDB Atlas:
```javascript
// Usuarios con tokens activos
db.users.find({
  resetPasswordToken: { $exists: true }
})

// Tokens expirados
db.users.find({
  resetPasswordExpires: { $lt: new Date() }
})
```

### Limpiar tokens expirados (opcional)

Puedes agregar un cronjob o ejecutar manualmente:
```javascript
db.users.updateMany(
  { resetPasswordExpires: { $lt: new Date() } },
  { $unset: { resetPasswordToken: "", resetPasswordExpires: "" } }
)
```

---

## 🆘 Solución de Problemas

### Error: "Token inválido o expirado"
- El token ya fue usado
- Pasó más de 1 hora desde que se solicitó
- El token está mal copiado

**Solución**: Solicitar nuevo token

### Error: "Base de datos no disponible"
- MongoDB Atlas no está conectado
- Variable `MONGO_URI` mal configurada

**Solución**: Verificar conexión a MongoDB en Railway

### No llegan los emails
- `SENDGRID_API_KEY` no configurada o inválida
- Email no verificado en SendGrid (Single Sender)
- Revisar logs para ver errores de SendGrid

**Solución**: 
1. Verificar API Key en Railway
2. Verificar email en SendGrid Dashboard
3. Revisar logs de Railway

### Emails van a spam
- Dominio no autenticado en SendGrid
- SPF/DKIM no configurados

**Solución**: Usar Domain Authentication en SendGrid

---

## 🚀 Próximos Pasos (Opcional)

1. **Rate Limiting**: Limitar intentos de recuperación por IP
2. **Email Templates**: Usar plantillas profesionales de SendGrid
3. **2FA**: Agregar autenticación de dos factores
4. **Notificaciones**: Avisar cuando se cambie la contraseña
5. **Historial**: Registrar intentos de recuperación

---

## 📌 Links Útiles

- [SendGrid Documentation](https://docs.sendgrid.com/)
- [Railway Docs](https://docs.railway.app/)
- [bcrypt Documentation](https://github.com/pyca/bcrypt/)

---

**Fecha de implementación**: Noviembre 21, 2025  
**Repositorio**: https://github.com/JesseAinsworth/EasyBraille.Backend.git  
**Endpoints activos**: ✅
