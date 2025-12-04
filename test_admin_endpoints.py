"""
Script de prueba para verificar los endpoints del panel de administración
"""
import requests
import json

# URL del backend (cambiar según el entorno)
BACKEND_URL = "https://easybraillebackend-production.up.railway.app"
# Para desarrollo local, usar: BACKEND_URL = "http://localhost:8080"

def test_endpoint(name, url, method="GET"):
    """Prueba un endpoint y muestra el resultado"""
    print(f"\n{'='*60}")
    print(f"🧪 Probando: {name}")
    print(f"📡 URL: {url}")
    print(f"🔧 Método: {method}")
    print('='*60)
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, timeout=10)
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Respuesta:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏱️ Timeout: El servidor no respondió a tiempo")
    except requests.exceptions.ConnectionError:
        print("🔌 Error de conexión: No se pudo conectar al servidor")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  PRUEBA DE ENDPOINTS DEL PANEL DE ADMINISTRACIÓN        ║
    ║  EasyBraille Backend                                     ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Probar cada endpoint
    test_endpoint(
        "Test de Conexión",
        f"{BACKEND_URL}/api/admin/test-connection"
    )
    
    test_endpoint(
        "Estadísticas del Dashboard",
        f"{BACKEND_URL}/api/admin/stats"
    )
    
    test_endpoint(
        "Lista de Usuarios",
        f"{BACKEND_URL}/api/admin/users"
    )
    
    test_endpoint(
        "Lista de Traducciones",
        f"{BACKEND_URL}/api/admin/translations?limit=10"
    )
    
    print(f"\n{'='*60}")
    print("✅ Pruebas completadas")
    print('='*60)

if __name__ == "__main__":
    main()
