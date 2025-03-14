from flask import Blueprint
from app_utils import *
import logging
from services.extract_keyframes import process_keyframe_extraction
from services.authentication import authenticate
from services.cloud_storage import upload_file

# 📌 Crear un Blueprint para el endpoint de extracción de fotogramas clave
extract_keyframes_bp = Blueprint('extract_keyframes', __name__)
logger = logging.getLogger(__name__)

# 🚀 Endpoint para extraer fotogramas clave de un video:
# - Protegido por autenticación (API key)
# - Valida que el payload JSON cumpla el esquema definido
# - Procesa la solicitud en cola para evitar bloqueos
@extract_keyframes_bp.route('/extract-keyframes', methods=['POST'])
@authenticate  # 🔑 Verifica que la solicitud incluya una API key válida
@validate_payload({
    "type": "object",
    "properties": {
        "video_url": {"type": "string", "format": "uri"},
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"}
    },
    "required": ["video_url"],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)
def extract_keyframes(job_id, data):
    # 📥 Extraer parámetros del payload
    video_url = data.get('video_url')
    webhook_url = data.get('webhook_url')
    id = data.get('id')

    logger.info(f"Job {job_id}: Solicitud de extracción de fotogramas clave recibida para {video_url}")

    try:
        # 🎬 Procesar la extracción de fotogramas clave del video
        image_paths = process_keyframe_extraction(video_url, job_id)

        # ☁️ Subir cada fotograma extraído y recolectar las URLs resultantes
        image_urls = []
        for image_path in image_paths:
            cloud_url = upload_file(image_path)
            image_urls.append({"image_url": cloud_url})

        logger.info(f"Job {job_id}: Fotogramas clave subidos a almacenamiento en la nube")

        # 🔗 Retornar las URLs de los fotogramas subidos con un código de estado 200
        return {"image_urls": image_urls}, "/extract-keyframes", 200

    except Exception as e:
        logger.error(f"Job {job_id}: Error durante la extracción de fotogramas clave - {str(e)}")
        return str(e), "/extract-keyframes", 500
