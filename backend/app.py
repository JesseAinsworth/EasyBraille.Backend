@app.route("/api/auth/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return '', 200  # ✅ Respuesta al preflight

    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Faltan campos"}), 400

        # Aquí iría la lógica real de autenticación (ej. comparar con DB)
        if email == "test@example.com" and password == "123456":
            return jsonify({
                "message": "Inicio de sesión exitoso",
                "user": {
                    "name": email.split("@")[0],
                    "email": email
                }
            }), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        print(f"❌ Error en login: {e}")
        return jsonify({"error": "Error interno"}), 500
