# ✅ Checklist de Deploy - Recuperación de Contraseña

## 📋 Pre-Deploy

### Código
- [x] ✅ Endpoints implementados en `backend/app.py`
  - [x] POST `/api/auth/forgot-password`
  - [x] POST `/api/auth/reset-password`
- [x] ✅ Función `send_reset_email()` agregada
- [x] ✅ Imports necesarios agregados
  - [x] `secrets`
  - [x] `timedelta`
  - [x] `SendGrid`
- [x] ✅ `requirements.txt` actualizado con `sendgrid`
- [x] ✅ Sin errores de sintaxis

### Documentación
- [x] ✅ `README_PASSWORD_RECOVERY.md` - Resumen completo
- [x] ✅ `PASSWORD_RESET_SETUP.md` - Configuración SendGrid
- [x] ✅ `DEPLOY_GUIDE.md` - Guía de deploy
- [x] ✅ `ENV_VARIABLES.md` - Variables de entorno
- [x] ✅ `backend/RECOVERY_API_EXAMPLES.md` - Ejemplos de uso
- [x] ✅ `backend/test_password_recovery.py` - Script de testing

---

## 🚀 Deploy

### Paso 1: Git
```bash
git status                                    # Verificar cambios
git add .                                     # Agregar todos los archivos
git commit -m "feat: recuperación de contraseña"  # Commit
git push origin main                          # Push a GitHub
```

Estado: [ ] ⏳ Pendiente

### Paso 2: Railway Auto-Deploy
- [ ] ⏳ Railway detecta cambios
- [ ] ⏳ Instalando dependencias (`sendgrid`)
- [ ] ⏳ Building...
- [ ] ⏳ Deploying...
- [ ] ✅ Deploy exitoso

**Ver progreso**: https://railway.app/ → Tu proyecto → Deployments

Estado: [ ] ⏳ Pendiente

---

## 🔧 Post-Deploy

### Testing Básico

#### Test 1: Verificar backend activo
```bash
curl https://easybraillebackend-production.up.railway.app/
```

Respuesta esperada:
```json
{"message": "EasyBraille backend activo"}
```

Estado: [ ] ⏳ Pendiente

#### Test 2: Endpoint forgot-password
```bash
curl -X POST https://easybraillebackend-production.up.railway.app/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```

Respuesta esperada:
```json
{"message": "Se ha enviado un correo con instrucciones de recuperación"}
```

Estado: [ ] ⏳ Pendiente

#### Test 3: Verificar logs
1. Ve a Railway Dashboard
2. Click en Deployments
3. View Logs
4. Busca: `🔐 Token de recuperación generado`

Estado: [ ] ⏳ Pendiente

#### Test 4: Token inválido (debe fallar)
```bash
curl -X POST https://easybraillebackend-production.up.railway.app/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{"token":"invalid","newPassword":"test123"}'
```

Respuesta esperada:
```json
{"error": "Token inválido o expirado"}
```

Estado: [ ] ⏳ Pendiente

---

## 📧 Configuración SendGrid (Opcional)

### Paso 1: Crear cuenta SendGrid
- [ ] Ir a https://sendgrid.com/
- [ ] Registrarse (gratis)
- [ ] Verificar email

Estado: [ ] ⏳ Opcional

### Paso 2: Generar API Key
- [ ] Settings → API Keys
- [ ] Create API Key
- [ ] Nombre: `EasyBraille-Production`
- [ ] Permisos: Mail Send
- [ ] Copiar API Key

Estado: [ ] ⏳ Opcional

### Paso 3: Verificar email sender
- [ ] Settings → Sender Authentication
- [ ] Single Sender Verification
- [ ] From Email: `noreply@easy-braille.com`
- [ ] Verificar email recibido

Estado: [ ] ⏳ Opcional

### Paso 4: Agregar variable en Railway
- [ ] Railway Dashboard
- [ ] Variables
- [ ] New Variable
- [ ] Nombre: `SENDGRID_API_KEY`
- [ ] Valor: `SG.xxxx...`
- [ ] Save

Estado: [ ] ⏳ Opcional

### Paso 5: Verificar envío de emails
```bash
curl -X POST https://easybraillebackend-production.up.railway.app/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email":"tu-email@example.com"}'
```

- [ ] Email recibido
- [ ] Link funciona
- [ ] No va a spam

Estado: [ ] ⏳ Opcional

---

## 🧪 Testing Completo con Python

```bash
cd backend
python test_password_recovery.py
```

Verificar:
- [ ] Test 1: Solicitar token - PASS
- [ ] Test 2: Token inválido - PASS
- [ ] Test 3: Contraseña corta - PASS

Estado: [ ] ⏳ Pendiente

---

## 🌐 Testing desde Frontend

### Paso 1: Solicitar recuperación
1. Ir a https://www.easy-braille.com/reset-password
2. Ingresar email registrado
3. Click en "Enviar"
4. Verificar mensaje de éxito

Estado: [ ] ⏳ Pendiente

### Paso 2: Obtener token
**Sin SendGrid:**
- [ ] Ir a Railway Logs
- [ ] Copiar token del log

**Con SendGrid:**
- [ ] Revisar bandeja de entrada
- [ ] Abrir email
- [ ] Click en link

Estado: [ ] ⏳ Pendiente

### Paso 3: Restablecer contraseña
1. Formulario con token pre-cargado aparece
2. Ingresar nueva contraseña
3. Click en "Restablecer"
4. Verificar mensaje de éxito

Estado: [ ] ⏳ Pendiente

### Paso 4: Login con nueva contraseña
1. Ir a https://www.easy-braille.com/login
2. Ingresar email y nueva contraseña
3. Click en "Iniciar sesión"
4. ✅ Login exitoso

Estado: [ ] ⏳ Pendiente

---

## 🔍 Verificación en MongoDB

### Ver tokens activos
```javascript
use easybraille
db.users.find(
  { resetPasswordToken: { $exists: true } },
  { email: 1, resetPasswordToken: 1, resetPasswordExpires: 1 }
)
```

Estado: [ ] ⏳ Pendiente

### Verificar contraseña actualizada
```javascript
db.users.findOne(
  { email: "test@example.com" },
  { email: 1, updatedAt: 1 }
)
```

Estado: [ ] ⏳ Pendiente

---

## ✅ Verificación Final

### Funcionalidad
- [ ] Usuario puede solicitar recuperación
- [ ] Token se genera y guarda en BD
- [ ] Email se envía (o token aparece en logs)
- [ ] Link del email abre formulario correcto
- [ ] Usuario puede restablecer contraseña
- [ ] Token se elimina después de usar
- [ ] Usuario puede hacer login con nueva contraseña
- [ ] Token expirado muestra error
- [ ] Contraseña corta muestra error

### Seguridad
- [ ] Tokens son aleatorios y únicos
- [ ] Tokens expiran en 1 hora
- [ ] No se revela si un email existe
- [ ] Contraseñas se hashean con bcrypt
- [ ] Tokens se eliminan después de usar
- [ ] CORS configurado correctamente

### Performance
- [ ] Endpoints responden rápido (<2s)
- [ ] No hay errores en logs
- [ ] MongoDB conectado correctamente

---

## 🎉 Todo Completo

Si todos los checks están marcados:

- ✅ **Backend funcional**
- ✅ **Endpoints disponibles**
- ✅ **Testing exitoso**
- ✅ **Seguridad implementada**
- ✅ **Documentación completa**

**Estado**: 🚀 PRODUCCIÓN LISTA

---

## 📊 Resumen

| Componente | Estado |
|------------|--------|
| Código Backend | ✅ Completo |
| Dependencias | ✅ Actualizadas |
| Endpoints | ✅ Implementados |
| Testing Scripts | ✅ Creados |
| Documentación | ✅ Completa |
| Deploy | ⏳ Pendiente |
| SendGrid | ⏳ Opcional |
| Testing Final | ⏳ Pendiente |

---

## 🆘 Si algo falla

### Deploy fallido
1. Revisar logs de Railway
2. Verificar `requirements.txt`
3. Re-trigger deploy: `git commit --allow-empty -m "trigger"`

### Endpoints no responden
1. Verificar Railway Logs
2. Verificar `MONGO_URI` está configurado
3. Verificar CORS headers

### Emails no llegan
1. Verificar `SENDGRID_API_KEY` en Railway
2. Verificar email sender en SendGrid
3. Revisar logs para errores de SendGrid

### Token siempre inválido
1. Verificar token en MongoDB
2. Verificar timezone del servidor
3. Copiar token exactamente como aparece

---

**Fecha**: Noviembre 21, 2025  
**Última actualización**: Implementación completa  
**Próximo paso**: `git push origin main`
