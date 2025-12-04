from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
import bcrypt
import bson
import secrets
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# 1️⃣ Inicializar Flask
app = Flask(__name__)

# 2️⃣ Configurar CORS con credenciales
ALLOWED_ORIGIN = "https://www.easy-braille.com"
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGIN}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# 3️⃣ Conexión a MongoDB Atlas
try:
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise Exception("MONGO_URI no está definido")

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["easybraille"]
    usuarios = db["users"]
    traducciones = db["translations"]
except Exception as e:
    print(f"❌ Error conectando a MongoDB: {e}")
    usuarios = None
    traducciones = None

# Función para enviar emails de recuperación
def send_reset_email(to_email, reset_url):
    """Envía email de recuperación de contraseña usando SendGrid"""
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    
    if not sendgrid_api_key:
        print("⚠️ SENDGRID_API_KEY no configurado, solo se mostrará el URL en logs")
        print(f"🔐 URL de recuperación para {to_email}: {reset_url}")
        return True
    
    message = Mail(
        from_email='noreply@em8123.easy-braille.com',
        to_emails=to_email,
        subject='Recuperación de contraseña - EasyBraille',
        html_content=f'''
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <h2 style="color: #4a90e2;">Recuperación de contraseña</h2>
              <p>Has solicitado restablecer tu contraseña en EasyBraille.</p>
              <p>Haz clic en el siguiente botón para crear una nueva contraseña:</p>
              <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background-color: #4a90e2; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                  Restablecer Contraseña
                </a>
              </div>
              <p>O copia y pega este enlace en tu navegador:</p>
              <p style="word-break: break-all; color: #666;">{reset_url}</p>
              <p style="color: #e74c3c; font-weight: bold;">⚠️ Este enlace expirará en 1 hora.</p>
              <p style="color: #999; font-size: 12px; margin-top: 30px;">
                Si no solicitaste restablecer tu contraseña, puedes ignorar este correo de forma segura.
              </p>
            </div>
          </body>
        </html>
        ''')
    
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(f"✅ Email de recuperación enviado a {to_email} (status: {response.status_code})")
        return True
    except Exception as e:
        print(f"❌ Error enviando email a {to_email}: {e}")
        return False

# 4️⃣ Ruta raíz
@app.route("/")
def index():
    return jsonify({"message": "EasyBraille backend activo"})

# 5️⃣ Registro de usuario
@app.route("/api/auth/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if usuarios is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        data = request.get_json(silent=True)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Faltan campos"}), 400

        if usuarios.find_one({"email": email}):
            return jsonify({"error": "El usuario ya existe"}), 409

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        result = usuarios.insert_one({
            "email": email,
            "password": hashed_pw.decode(),
            "name": email.split("@")[0],
            "role": "user",
            "isActive": True,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        })

        user_id = str(result.inserted_id)
        print(f"✅ Usuario registrado: {email}")
        return jsonify({
            "message": "Usuario registrado correctamente",
            "user": {
                "name": email.split("@")[0],
                "email": email,
                "userId": user_id
            }
        }), 200

    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return jsonify({"error": "Error interno"}), 500

# 6️⃣ Inicio de sesión
@app.route("/api/auth/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if usuarios is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        data = request.get_json(silent=True)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Faltan campos"}), 400

        user = usuarios.find_one({"email": email})
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        stored_pw = user["password"]
        if isinstance(stored_pw, bson.binary.Binary):
            stored_pw = stored_pw.decode()
        elif isinstance(stored_pw, bytes):
            stored_pw = stored_pw.decode()

        if bcrypt.checkpw(password.encode("utf-8"), stored_pw.encode("utf-8")):
            print(f"✅ Login exitoso: {user}")
            return jsonify({
                "message": "Inicio de sesión exitoso",
                "user": {
                    "name": user["name"],
                    "email": user["email"],
                    "role": user.get("role", "user"),
                    "isActive": user.get("isActive", True),
                    "userId": str(user["_id"])
                }
            }), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        print(f"❌ Error en login: {e}")
        return jsonify({"error": "Error interno"}), 500

# 7️⃣ Guardar traducción
@app.route("/api/translations", methods=["POST", "OPTIONS"])
def save_translation():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if traducciones is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        data = request.get_json(silent=True)
        userId = data.get("userId")
        originalText = data.get("originalText")
        brailleText = data.get("brailleText")
        translationType = data.get("translationType", "TEXT_TO_BRAILLE")
        language = data.get("language", "es")

        if not userId or not originalText or not brailleText:
            return jsonify({"error": "Faltan campos"}), 400

        now = datetime.utcnow()
        traducciones.insert_one({
            "userId": userId,
            "originalText": originalText,
            "brailleText": brailleText,
            "translationType": translationType,
            "language": language,
            "createdAt": now,
            "updatedAt": now
        })

        print(f"✅ Traducción guardada para usuario {userId}")
        return jsonify({"message": "Traducción guardada"}), 200

    except Exception as e:
        print(f"❌ Error al guardar traducción: {e}")
        return jsonify({"error": "Error interno"}), 500

# 8️⃣ Historial de traducciones
@app.route("/api/translations/history", methods=["GET", "OPTIONS"])
def get_translation_history():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if traducciones is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        userId = request.args.get("userId")
        if not userId:
            return jsonify({"error": "Falta el userId"}), 400

        history = list(traducciones.find(
            {"userId": userId},
            {"_id": 0}
        ).sort("createdAt", -1).limit(10))

        return jsonify({"history": history}), 200

    except Exception as e:
        print(f"❌ Error al obtener historial: {e}")
        return jsonify({"error": "Error interno"}), 500

# 9️⃣ Recuperación de contraseña - Solicitar token
@app.route("/api/auth/forgot-password", methods=["POST", "OPTIONS"])
def forgot_password():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if usuarios is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        data = request.get_json(silent=True)
        email = data.get("email")

        if not email:
            return jsonify({"error": "Email requerido"}), 400

        user = usuarios.find_one({"email": email})
        if not user:
            # Por seguridad, no revelar si el usuario existe
            return jsonify({"message": "Si el correo existe, recibirás instrucciones de recuperación"}), 200

        # Generar token único
        reset_token = secrets.token_urlsafe(32)
        reset_expires = datetime.utcnow() + timedelta(hours=1)  # Token válido por 1 hora

        # Guardar token en la base de datos
        usuarios.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "resetPasswordToken": reset_token,
                    "resetPasswordExpires": reset_expires
                }
            }
        )

        # Enviar correo con el token
        reset_url = f"https://www.easy-braille.com/reset-password?token={reset_token}"
        send_reset_email(email, reset_url)

        print(f"🔐 Token de recuperación generado para {email}")

        return jsonify({
            "message": "Se ha enviado un correo con instrucciones de recuperación"
        }), 200

    except Exception as e:
        print(f"❌ Error en forgot-password: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# 🔟 Recuperación de contraseña - Restablecer con token
@app.route("/api/auth/reset-password", methods=["POST", "OPTIONS"])
def reset_password():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if usuarios is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        data = request.get_json(silent=True)
        token = data.get("token")
        new_password = data.get("newPassword")

        if not token or not new_password:
            return jsonify({"error": "Token y contraseña requeridos"}), 400

        if len(new_password) < 6:
            return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400

        # Buscar usuario con token válido y no expirado
        user = usuarios.find_one({
            "resetPasswordToken": token,
            "resetPasswordExpires": {"$gt": datetime.utcnow()}
        })

        if not user:
            return jsonify({"error": "Token inválido o expirado"}), 400

        # Hash de la nueva contraseña
        hashed_pw = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

        # Actualizar contraseña y eliminar token
        usuarios.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "password": hashed_pw.decode(),
                    "updatedAt": datetime.utcnow()
                },
                "$unset": {
                    "resetPasswordToken": "",
                    "resetPasswordExpires": ""
                }
            }
        )

        print(f"✅ Contraseña restablecida exitosamente para {user['email']}")

        return jsonify({
            "message": "Contraseña actualizada correctamente"
        }), 200

    except Exception as e:
        print(f"❌ Error en reset-password: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# 1️⃣1️⃣ Estadísticas del panel de administración
@app.route("/api/admin/stats", methods=["GET", "OPTIONS"])
def get_admin_stats():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if usuarios is None or traducciones is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        # Calcular fechas
        now = datetime.utcnow()
        start_of_month = datetime(now.year, now.month, 1)
        start_of_week = now - timedelta(days=7)

        # Total de usuarios
        total_users = usuarios.count_documents({})
        
        # Usuarios activos
        active_users = usuarios.count_documents({"isActive": True})
        
        # Usuarios administradores
        admin_users = usuarios.count_documents({"role": "admin"})
        
        # Usuarios regulares
        regular_users = usuarios.count_documents({"role": "user"})

        # Total de traducciones
        total_translations = traducciones.count_documents({})
        
        # Traducciones esta semana
        translations_this_week = traducciones.count_documents({
            "createdAt": {"$gte": start_of_week}
        })

        # Traducciones por tipo
        translations_by_type = list(traducciones.aggregate([
            {"$group": {"_id": "$translationType", "count": {"$sum": 1}}}
        ]))

        # Traducciones por mes (últimos 6 meses)
        six_months_ago = datetime(now.year, now.month, 1) - timedelta(days=180)
        translations_last_6_months = list(traducciones.aggregate([
            {"$match": {"createdAt": {"$gte": six_months_ago}}},
            {"$group": {
                "_id": {
                    "year": {"$year": "$createdAt"},
                    "month": {"$month": "$createdAt"}
                },
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id.year": 1, "_id.month": 1}}
        ]))

        # Usuarios por mes (últimos 6 meses)
        users_last_6_months = list(usuarios.aggregate([
            {"$match": {"createdAt": {"$gte": six_months_ago}}},
            {"$group": {
                "_id": {
                    "year": {"$year": "$createdAt"},
                    "month": {"$month": "$createdAt"}
                },
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id.year": 1, "_id.month": 1}}
        ]))

        # Calcular precisión IA y tiempo de respuesta (valores de ejemplo)
        ai_accuracy = 95.5
        avg_response_time = 1.2
        success_rate = 98.0

        return jsonify({
            "stats": {
                "users": {
                    "total": total_users,
                    "active": active_users,
                    "admins": admin_users,
                    "regular": regular_users,
                    "last6Months": users_last_6_months
                },
                "translations": {
                    "total": total_translations,
                    "thisWeek": translations_this_week,
                    "byType": translations_by_type,
                    "last6Months": translations_last_6_months
                },
                "ai": {
                    "totalInteractions": total_translations,
                    "avgAccuracy": ai_accuracy,
                    "avgResponseTime": avg_response_time,
                    "successRate": success_rate
                }
            }
        }), 200

    except Exception as e:
        print(f"❌ Error al obtener estadísticas admin: {e}")
        return jsonify({"error": "Error interno"}), 500

# 1️⃣2️⃣ Lista de usuarios para admin
@app.route("/api/admin/users", methods=["GET", "OPTIONS"])
def get_all_users():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if usuarios is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        # Obtener todos los usuarios (sin contraseñas)
        users_list = list(usuarios.find(
            {},
            {
                "_id": 1,
                "email": 1,
                "name": 1,
                "role": 1,
                "isActive": 1,
                "createdAt": 1,
                "updatedAt": 1
            }
        ).sort("createdAt", -1))

        # Convertir ObjectId a string
        for user in users_list:
            user["_id"] = str(user["_id"])

        return jsonify({
            "users": users_list,
            "total": len(users_list)
        }), 200

    except Exception as e:
        print(f"❌ Error al obtener usuarios: {e}")
        return jsonify({"error": "Error interno"}), 500

# 1️⃣3️⃣ Lista de traducciones para admin
@app.route("/api/admin/translations", methods=["GET", "OPTIONS"])
def get_all_translations():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if traducciones is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        # Obtener todas las traducciones con límite
        limit = int(request.args.get("limit", 50))
        
        translations_list = list(traducciones.find(
            {},
            {"_id": 0}
        ).sort("createdAt", -1).limit(limit))

        return jsonify({
            "translations": translations_list,
            "total": len(translations_list)
        }), 200

    except Exception as e:
        print(f"❌ Error al obtener traducciones: {e}")
        return jsonify({"error": "Error interno"}), 500

# 1️⃣4️⃣ Probar conexión a la base de datos
@app.route("/api/admin/test-connection", methods=["GET", "OPTIONS"])
def test_connection():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        if usuarios is None or traducciones is None:
            return jsonify({
                "connected": False,
                "message": "Base de datos no disponible"
            }), 500

        # Intentar hacer un ping a la base de datos
        client.admin.command('ping')
        
        return jsonify({
            "connected": True,
            "message": "Conexión exitosa a MongoDB",
            "database": "easybraille"
        }), 200

    except Exception as e:
        print(f"❌ Error al probar conexión: {e}")
        return jsonify({
            "connected": False,
            "message": f"Error: {str(e)}"
        }), 500

# 1️⃣5️⃣ Configuración Railway/Gunicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
