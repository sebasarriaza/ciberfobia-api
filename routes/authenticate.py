from flask import Blueprint, request, jsonify, current_app
from app_utils import *
from functools import wraps
import os

# 📌 Crear un Blueprint para el endpoint de autenticación
auth_bp = Blueprint('auth', __name__)

# 🔑 Obtener la API key predefinida del entorno
API_KEY = os.environ.get('API_KEY')

# 🚀 Endpoint de autenticación
# Ejecuta la verificación de la API key proporcionada en los encabezados de la solicitud
@auth_bp.route('/authenticate', methods=['GET'])
@queue_task_wrapper(bypass_queue=True)  # ⚡ Se ejecuta inmediatamente sin pasar por la cola
def authenticate_endpoint(**kwargs):
    # 📥 Obtener la API key del encabezado 'X-API-Key'
    api_key = request.headers.get('X-API-Key')
    
    # ✅ Comparar la API key recibida con la API key predefinida
    if api_key == API_KEY:
        return "Authorized", "/authenticate", 200  # Autorizado
    else:
        return "Unauthorized", "/authenticate", 401  # No autorizado
