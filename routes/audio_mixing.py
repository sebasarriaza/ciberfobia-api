from flask import Blueprint
from app_utils import *
import logging
from services.audio_mixing import process_audio_mixing
from services.authentication import authenticate
from services.cloud_storage import upload_file

# 📌 Crear un Blueprint para el endpoint de mezcla de audio
audio_mixing_bp = Blueprint('audio_mixing', __name__)
logger = logging.getLogger(__name__)

# 🚀 Endpoint para mezclar audio y video:
# - Protegido por autenticación (API key)
# - Valida que el payload cumpla el esquema definido
# - Coloca la tarea en la cola para procesamiento asíncrono
@audio_mixing_bp.route('/audio-mixing', methods=['POST'])
@authenticate  # 🔑 Verifica que la solicitud tenga una API key válida
@validate_payload({
    "type": "object",
    "properties": {
        "video_url": {"type": "string", "format": "uri"},
        "audio_url": {"type": "string", "format": "uri"},
        "video_vol": {"type": "number", "minimum": 0, "maximum": 100},
        "audio_vol": {"type": "number", "minimum": 0, "maximum": 100},
        "output_length": {"type": "string", "enum": ["video", "audio"]},
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"}
    },
    "required": ["video_url", "audio_url"],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)  # ⏳ Coloca la tarea en una cola para evitar bloqueos
def audio_mixing(job_id, data):
    # 📥 Extraer los parámetros del payload
    video_url = data.get('video_url')
    audio_url = data.get('audio_url')
    video_vol = data.get('video_vol', 100)
    audio_vol = data.get('audio_vol', 100)
    output_length = data.get('output_length', 'video')
    webhook_url = data.get('webhook_url')
    id = data.get('id')

    logger.info(f"Job {job_id}: Recibida solicitud de mezcla para {video_url} y {audio_url}")

    try:
        # 🎵 Procesar la mezcla de audio y video
        output_filename = process_audio_mixing(
            video_url, audio_url, video_vol, audio_vol, output_length, job_id, webhook_url
        )

        # ☁️ Subir el archivo resultante a la nube
        cloud_url = upload_file(output_filename)

        logger.info(f"Job {job_id}: Archivo mezclado subido a la nube: {cloud_url}")

        # 🔗 Retornar la URL del archivo subido, junto con la ruta y el código de estado 200
        return cloud_url, "/audio-mixing", 200

    except Exception as e:
        logger.error(f"Job {job_id}: Error durante el proceso de mezcla - {str(e)}")
        return str(e), "/audio-mixing", 500