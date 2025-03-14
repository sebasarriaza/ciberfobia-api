from flask import Blueprint
from app_utils import *
import logging
import os
from services.transcription import process_transcription
from services.authentication import authenticate
from services.cloud_storage import upload_file

# 📌 Crear un Blueprint para el endpoint de transcripción de medios
transcribe_bp = Blueprint('transcribe', __name__)
logger = logging.getLogger(__name__)

# 🚀 Endpoint para transcribir medios:
# - Protegido por autenticación (verifica API key)
# - Valida el payload JSON según el esquema definido
# - Procesa la solicitud en cola para no bloquear la respuesta inmediata
@transcribe_bp.route('/transcribe-media', methods=['POST'])
@authenticate  # 🔑 Verifica la autenticación
@validate_payload({
    "type": "object",
    "properties": {
        "media_url": {"type": "string", "format": "uri"},
        "output": {"type": "string", "enum": ["transcript", "srt", "vtt", "ass"]},
        "webhook_url": {"type": "string", "format": "uri"},
        "max_chars": {"type": "integer"},
        "id": {"type": "string"}
    },
    "required": ["media_url"],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)
def transcribe(job_id, data):
    # 📥 Extraer parámetros del payload
    media_url = data['media_url']
    output = data.get('output', 'transcript')
    webhook_url = data.get('webhook_url')
    max_chars = data.get('max_chars', 56)
    id = data.get('id')

    logger.info(f"Job {job_id}: Solicitud de transcripción recibida para {media_url}")

    try:
        # 🎙️ Procesar la transcripción del medio
        result = process_transcription(media_url, output, max_chars)
        logger.info(f"Job {job_id}: Proceso de transcripción completado exitosamente")

        # 📤 Si el resultado es una ruta de archivo, se sube a la nube
        if output in ['srt', 'vtt', 'ass']:
            cloud_url = upload_file(result)
            os.remove(result)  # 🗑️ Eliminar el archivo temporal después de la subida
            return cloud_url, "/transcribe-media", 200
        else:
            # 📄 Si el resultado es texto, se retorna directamente
            return result, "/transcribe-media", 200

    except Exception as e:
        logger.error(f"Job {job_id}: Error durante el proceso de transcripción - {str(e)}")
        return str(e), "/transcribe-media", 500
