"""
Script de prueba para los endpoints de recuperación de contraseña
Uso: python test_password_recovery.py
"""

import requests
import json
import time
from datetime import datetime

# Configuración
BASE_URL = "https://easybraillebackend-production.up.railway.app"
# Para testing local, usa: BASE_URL = "http://localhost:8080"

TEST_EMAIL = "test@example.com"
TEST_NEW_PASSWORD = "nuevaPassword123"

def print_section(title):
    """Imprime una sección separada visualmente"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_forgot_password(email):
    """Prueba el endpoint de solicitud de recuperación"""
    print_section("TEST 1: Solicitar Token de Recuperación")
    
    url = f"{BASE_URL}/api/auth/forgot-password"
    payload = {"email": email}
    
    print(f"📤 Enviando request a: {url}")
    print(f"📧 Email: {email}")
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"📥 Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            print("\n✅ Token solicitado correctamente")
            print("⚠️  Revisa los logs del backend para obtener el token")
            print("    (o tu email si SendGrid está configurado)")
            return True
        else:
            print("\n❌ Error en la solicitud")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error de conexión: {e}")
        return False

def test_reset_password(token, new_password):
    """Prueba el endpoint de restablecimiento de contraseña"""
    print_section("TEST 2: Restablecer Contraseña")
    
    url = f"{BASE_URL}/api/auth/reset-password"
    payload = {
        "token": token,
        "newPassword": new_password
    }
    
    print(f"📤 Enviando request a: {url}")
    print(f"🔑 Token: {token[:20]}... (truncado)")
    print(f"🔐 Nueva contraseña: {'*' * len(new_password)}")
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"📥 Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            print("\n✅ Contraseña restablecida correctamente")
            return True
        else:
            print("\n❌ Error al restablecer contraseña")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error de conexión: {e}")
        return False

def test_invalid_token():
    """Prueba con un token inválido"""
    print_section("TEST 3: Token Inválido")
    
    url = f"{BASE_URL}/api/auth/reset-password"
    payload = {
        "token": "token-invalido-123",
        "newPassword": "password123"
    }
    
    print(f"📤 Intentando con token inválido...")
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"📥 Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        if response.status_code == 400:
            print("\n✅ Validación correcta: token rechazado")
            return True
        else:
            print("\n❌ Debería retornar 400 para token inválido")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error de conexión: {e}")
        return False

def test_short_password(token):
    """Prueba con una contraseña muy corta"""
    print_section("TEST 4: Contraseña muy corta")
    
    url = f"{BASE_URL}/api/auth/reset-password"
    payload = {
        "token": token or "token-de-prueba",
        "newPassword": "12345"  # Menos de 6 caracteres
    }
    
    print(f"📤 Intentando con contraseña de 5 caracteres...")
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"📥 Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        if response.status_code == 400:
            print("\n✅ Validación correcta: contraseña rechazada")
            return True
        else:
            print("\n❌ Debería retornar 400 para contraseña corta")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error de conexión: {e}")
        return False

def main():
    """Ejecuta todos los tests"""
    print("\n" + "🧪"*30)
    print("  TESTS DE RECUPERACIÓN DE CONTRASEÑA")
    print("  EasyBraille Backend")
    print("🧪"*30)
    print(f"\n🌐 Backend URL: {BASE_URL}")
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Test 1: Solicitar token
    result1 = test_forgot_password(TEST_EMAIL)
    results.append(("Solicitar token", result1))
    
    time.sleep(1)
    
    # Test 2: Token inválido
    result3 = test_invalid_token()
    results.append(("Token inválido", result3))
    
    time.sleep(1)
    
    # Test 3: Contraseña corta
    result4 = test_short_password(None)
    results.append(("Contraseña corta", result4))
    
    # Test 4: Restablecer con token real (requiere intervención manual)
    print_section("TEST 5: Restablecer con Token Real (Manual)")
    print("⚠️  Para completar este test:")
    print("1. Copia el token de los logs del backend o del email")
    print("2. Ejecuta:")
    print(f"   python -c \"from test_password_recovery import test_reset_password; test_reset_password('TU-TOKEN', '{TEST_NEW_PASSWORD}')\"")
    
    # Resumen
    print_section("📊 RESUMEN DE TESTS")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n📈 Resultado: {passed}/{total} tests pasados")
    
    if passed == total:
        print("\n🎉 ¡Todos los tests automáticos pasaron!")
    else:
        print("\n⚠️  Algunos tests fallaron. Revisa los detalles arriba.")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
