import bson

@app.route("/api/auth/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return '', 200

    if usuarios is None:
        return jsonify({"error": "Base de datos no disponible"}), 500

    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Formato inválido"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Faltan campos"}), 400

        user = usuarios.find_one({"email": email})
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        stored_pw = user["password"]

        # Manejo flexible: Binary o String
        if isinstance(stored_pw, bson.binary.Binary):
            stored_pw = stored_pw.decode()  # convertir a string
        elif isinstance(stored_pw, bytes):
            stored_pw = stored_pw.decode()

        if bcrypt.checkpw(password.encode("utf-8"), stored_pw.encode("utf-8")):
            print(f"✅ Usuario autenticado: {email}")
            return jsonify({
                "message": "Inicio de sesión exitoso",
                "user": {
                    "name": user["name"],
                    "email": user["email"],
                    "role": user.get("role", "user"),
                    "isActive": user.get("isActive", True)
                }
            }), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        print(f"❌ Error en login: {e}")
        return jsonify({"error": "Error interno"}), 500
