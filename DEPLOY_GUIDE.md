# 🚀 Guía Rápida de Deploy - Recuperación de Contraseña

## ✅ Cambios Realizados

1. ✅ Actualizado `requirements.txt` con `sendgrid>=6.11`
2. ✅ Agregado endpoint `POST /api/auth/forgot-password`
3. ✅ Agregado endpoint `POST /api/auth/reset-password`
4. ✅ Implementada función `send_reset_email()`
5. ✅ Agregados imports necesarios (`secrets`, `timedelta`, `SendGrid`)

---

## 📋 Pasos para Deploy en Railway

### 1. Commit y Push a GitHub

```bash
git add .
git commit -m "feat: agregar endpoints de recuperación de contraseña"
git push origin main
```

### 2. Railway Auto-Deploy

Railway detectará los cambios automáticamente y:
- ✅ Instalará las nuevas dependencias (`sendgrid`)
- ✅ Reiniciará el servicio con los nuevos endpoints

**Ver progreso**: Railway Dashboard → Deployments

---

## ⚙️ Configuración Requerida

### Opción A: Con SendGrid (Producción)

1. **Crear cuenta SendGrid**: https://sendgrid.com/
2. **Generar API Key**: Settings → API Keys → Create
3. **Verificar email**: Settings → Sender Authentication → Verify Single Sender
4. **Agregar variable en Railway**:
   ```
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxx
   ```

### Opción B: Sin SendGrid (Testing)

- Los endpoints funcionarán
- El token aparecerá en los logs de Railway
- NO se enviarán emails reales

---

## 🧪 Verificación Post-Deploy

### 1. Verificar que el deploy fue exitoso

```bash
# Railway Dashboard → Deployments → Ver logs
# Buscar: "✅ Deployment successful"
```

### 2. Probar endpoint de forgot-password

```bash
curl -X POST https://easybraillebackend-production.up.railway.app/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```

**Respuesta esperada:**
```json
{
  "message": "Se ha enviado un correo con instrucciones de recuperación"
}
```

### 3. Revisar logs en Railway

Sin SendGrid:
```
🔐 Token de recuperación generado para test@example.com
⚠️ SENDGRID_API_KEY no configurado, solo se mostrará el URL en logs
🔐 URL de recuperación: https://www.easy-braille.com/reset-password?token=...
```

Con SendGrid:
```
🔐 Token de recuperación generado para test@example.com
✅ Email de recuperación enviado a test@example.com (status: 202)
```

### 4. Probar endpoint de reset-password

```bash
# Copiar token de los logs
curl -X POST https://easybraillebackend-production.up.railway.app/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{"token":"TU-TOKEN-AQUI","newPassword":"nuevaPass123"}'
```

**Respuesta esperada:**
```json
{
  "message": "Contraseña actualizada correctamente"
}
```

---

## 📊 Checklist de Verificación

### Backend
- [ ] Deploy exitoso en Railway
- [ ] Logs muestran "Token de recuperación generado"
- [ ] No hay errores en los logs
- [ ] Endpoint `/api/auth/forgot-password` responde 200
- [ ] Endpoint `/api/auth/reset-password` responde 200 con token válido
- [ ] Token inválido retorna error 400

### SendGrid (Opcional)
- [ ] API Key agregada en Railway
- [ ] Email verificado en SendGrid
- [ ] Emails llegan correctamente
- [ ] Link en el email funciona

### Base de Datos
- [ ] Token se guarda en MongoDB (`resetPasswordToken`)
- [ ] Fecha de expiración se guarda (`resetPasswordExpires`)
- [ ] Token se elimina después de usar
- [ ] Contraseña se actualiza correctamente

### Frontend
- [ ] Página `/reset-password` carga correctamente
- [ ] Formulario de solicitud funciona
- [ ] Formulario de cambio de contraseña funciona
- [ ] Redirecciona al login después de cambiar contraseña

---

## 🐛 Troubleshooting

### Error: Module 'sendgrid' not found

**Causa**: Railway no instaló las dependencias

**Solución**:
```bash
# Verificar requirements.txt tiene sendgrid
cat requirements.txt | grep sendgrid

# Re-trigger deploy
git commit --allow-empty -m "trigger redeploy"
git push origin main
```

### Error: "Base de datos no disponible"

**Causa**: MONGO_URI no está configurado

**Solución**: Verificar variables en Railway Dashboard

### Emails no llegan

**Causa**: SendGrid API Key inválida o email no verificado

**Solución**:
1. Verificar API Key en Railway
2. Verificar email en SendGrid Dashboard
3. Revisar logs para errores de SendGrid

### Token siempre inválido

**Causa**: Diferencia de timezone o token no se guardó

**Solución**:
```javascript
// Verificar en MongoDB Atlas
db.users.find({ email: "test@example.com" }, { 
  resetPasswordToken: 1, 
  resetPasswordExpires: 1 
})
```

---

## 📝 Archivos Modificados

```
EasyBraille.Backend/
├── requirements.txt                          # ✅ Actualizado
├── backend/
│   ├── app.py                                # ✅ Modificado
│   ├── test_password_recovery.py             # ✅ Nuevo
│   └── RECOVERY_API_EXAMPLES.md              # ✅ Nuevo
├── PASSWORD_RESET_SETUP.md                   # ✅ Nuevo
└── DEPLOY_GUIDE.md                           # ✅ Nuevo (este archivo)
```

---

## 🎯 Próximos Pasos

1. **Hacer commit y push**
   ```bash
   git add .
   git commit -m "feat: recuperación de contraseña implementada"
   git push origin main
   ```

2. **Esperar deploy de Railway** (2-3 minutos)

3. **Verificar endpoints funcionan**

4. **(Opcional) Configurar SendGrid**
   - Crear cuenta
   - Generar API Key
   - Verificar email
   - Agregar variable en Railway

5. **Probar flujo completo desde el frontend**
   - Ir a https://www.easy-braille.com/reset-password
   - Solicitar recuperación
   - Revisar email o logs
   - Cambiar contraseña
   - Hacer login con nueva contraseña

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisar logs de Railway**: Dashboard → Deployments → View Logs
2. **Verificar variables de entorno**: Dashboard → Variables
3. **Probar con curl**: Usar los comandos de arriba
4. **Verificar MongoDB**: Usar MongoDB Atlas para ver los datos

---

## ✨ Listo para Producción

Una vez completados todos los pasos:

- ✅ Los usuarios podrán recuperar sus contraseñas
- ✅ Los tokens expirarán después de 1 hora
- ✅ Todo funcionará sin intervención manual
- ✅ Los emails llegarán automáticamente (con SendGrid)

---

**Fecha**: Noviembre 21, 2025  
**Versión**: 1.0  
**Estado**: ✅ Listo para deploy
