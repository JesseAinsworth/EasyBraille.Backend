import requests
import os

# Simple client that posts an image file to the AI service and returns JSON response.
# The AI service is expected to expose an endpoint like /process-image that accepts
# a multipart/form-data 'image' file and returns JSON { texto: ..., detecciones: [...] }

TIMEOUT = int(os.environ.get("AI_CLIENT_TIMEOUT", "30"))


def send_image_to_ai_service(ai_service_url: str, image_path: str) -> dict:
    """Send image at image_path to ai_service_url and return parsed JSON.

    ai_service_url can be either the full URL to the endpoint (e.g. https://.../process-image)
    or a base URL; if it's a base URL we will append '/api/braille-image'.
    """
    if not ai_service_url:
        raise ValueError("AI service URL not configured")

    # Normalize URL: if path doesn't look like an endpoint, append expected route
    if not ai_service_url.rstrip("/").endswith("/api/braille-image"):
        endpoint = ai_service_url.rstrip("/") + "/api/braille-image"
    else:
        endpoint = ai_service_url

    with open(image_path, "rb") as f:
        files = {"image": (os.path.basename(image_path), f, "image/jpeg")}
        resp = requests.post(endpoint, files=files, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
