from flask import Blueprint
from app_utils import *
import logging
from services.ffmpeg_toolkit import process_video_combination
from services.authentication import authenticate
from services.cloud_storage import upload_file

# 📌 Crear un Blueprint para el endpoint de combinación de videos
combine_bp = Blueprint('combine', __name__)
logger = logging.getLogger(__name__)

# 🚀 Endpoint para combinar videos:
# - Protegido por autenticación
# - Valida el payload JSON según el esquema definido
# - Procesa la tarea en cola para evitar bloqueos
@combine_bp.route('/combine-videos', methods=['POST'])
@authenticate  # 🔑 Verifica la API key
@validate_payload({
    "type": "object",
    "properties": {
        "video_urls": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "video_url": {"type": "string", "format": "uri"}
                },
                "required": ["video_url"]
            },
            "minItems": 1
        },
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"}
    },
    "required": ["video_urls"],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)
def combine_videos(job_id, data):
    # 📥 Extraer la lista de URLs de video y otros parámetros
    media_urls = data['video_urls']
    webhook_url = data.get('webhook_url')
    id = data.get('id')

    logger.info(f"Job {job_id}: Recibida solicitud para combinar {len(media_urls)} videos")

    try:
        # 🔄 Procesar la combinación de videos utilizando FFmpeg
        output_file = process_video_combination(media_urls, job_id)
        logger.info(f"Job {job_id}: Proceso de combinación completado con éxito")

        # ☁️ Subir el archivo resultante a almacenamiento en la nube
        cloud_url = upload_file(output_file)
        logger.info(f"Job {job_id}: Video combinado subido a la nube: {cloud_url}")

        # 🔗 Retornar la URL del video subido, la ruta del endpoint y el código 200
        return cloud_url, "/combine-videos", 200

    except Exception as e:
        logger.error(f"Job {job_id}: Error durante la combinación de videos - {str(e)}")
        return str(e), "/combine-videos", 500
