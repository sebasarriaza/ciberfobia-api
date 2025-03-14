# routes/media_to_mp3.py
from flask import Blueprint, current_app
from app_utils import *
import logging
from services.ffmpeg_toolkit import process_conversion
from services.authentication import authenticate
from services.cloud_storage import upload_file
import os

# 📌 Crear un Blueprint para el endpoint de conversión a MP3
convert_bp = Blueprint('convert', __name__)
logger = logging.getLogger(__name__)

# 🚀 Endpoint para convertir medios a MP3:
# - Protegido por autenticación (verifica la API key)
# - Valida el payload JSON según el esquema definido
# - Procesa la solicitud en cola para evitar bloqueos
@convert_bp.route('/media-to-mp3', methods=['POST'])
@authenticate  # 🔑 Verifica que la API key es válida
@validate_payload({
    "type": "object",
    "properties": {
        "media_url": {"type": "string", "format": "uri"},
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"},
        "bitrate": {"type": "string", "pattern": "^[0-9]+k$"}
    },
    "required": ["media_url"],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)  # ⏳ Procesa la solicitud en una cola para no bloquear la respuesta inmediata
def convert_media_to_mp3(job_id, data):
    # 📥 Extraer parámetros del payload
    media_url = data['media_url']
    webhook_url = data.get('webhook_url')
    id = data.get('id')
    bitrate = data.get('bitrate', '128k')

    logger.info(f"Job {job_id}: Solicitud recibida para convertir a MP3 la URL: {media_url}")

    try:
        # 🎬 Procesar la conversión del medio a MP3 con el bitrate especificado
        output_file = process_conversion(media_url, job_id, bitrate)
        logger.info(f"Job {job_id}: Conversión completada con éxito")

        # ☁️ Subir el archivo convertido a almacenamiento en la nube
        cloud_url = upload_file(output_file)
        logger.info(f"Job {job_id}: Medio convertido subido a la nube: {cloud_url}")

        # 🔗 Retornar la URL del archivo subido, la ruta y el código 200
        return cloud_url, "/media-to-mp3", 200

    except Exception as e:
        logger.error(f"Job {job_id}: Error durante el proceso de conversión - {str(e)}")
        return str(e), "/media-to-mp3", 500
