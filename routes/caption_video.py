from flask import Blueprint, current_app
from app_utils import *
import logging
from services.caption_video import process_captioning
from services.authentication import authenticate
from services.cloud_storage import upload_file
import os

# 📌 Crear un Blueprint para el endpoint de subtitulación
caption_bp = Blueprint('caption', __name__)
logger = logging.getLogger(__name__)

# 🚀 Endpoint para agregar subtítulos a un video:
# - Protegido por autenticación
# - Valida el payload JSON según el esquema definido
# - Procesa la solicitud de subtitulado en cola
@caption_bp.route('/caption-video', methods=['POST'])
@authenticate  # 🔑 Verifica la API key
@validate_payload({
    "type": "object",
    "properties": {
        "video_url": {"type": "string", "format": "uri"},
        "srt": {"type": "string"},
        "ass": {"type": "string"},
        "options": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "option": {"type": "string"},
                    "value": {}  # Permite cualquier tipo para value
                },
                "required": ["option", "value"]
            }
        },
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"}
    },
    "required": ["video_url"],
    "oneOf": [
        {"required": ["srt"]},
        {"required": ["ass"]}
    ],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)  # ⏳ Se procesa en la cola para no bloquear la respuesta
def caption_video(job_id, data):
    # 📥 Extraer datos del payload
    video_url = data['video_url']
    caption_srt = data.get('srt')
    caption_ass = data.get('ass')
    options = data.get('options', [])
    webhook_url = data.get('webhook_url')
    id = data.get('id')

    logger.info(f"Job {job_id}: Recibida solicitud de subtitulado para {video_url}")
    logger.info(f"Job {job_id}: Opciones recibidas: {options}")

    # 🔄 Determinar el tipo de subtítulos a usar (ASS o SRT)
    if caption_ass is not None:
        captions = caption_ass
        caption_type = "ass"
    else:
        captions = caption_srt
        caption_type = "srt"

    try:
        # 🎬 Procesar el subtitulado del video
        output_filename = process_captioning(video_url, captions, caption_type, options, job_id)
        logger.info(f"Job {job_id}: Proceso de subtitulado completado con éxito")

        # ☁️ Subir el video subtitulado a la nube
        cloud_url = upload_file(output_filename)
        logger.info(f"Job {job_id}: Video subtitulado subido a almacenamiento en la nube: {cloud_url}")

        # 🔗 Retornar la URL del video subido con código 200
        return cloud_url, "/caption-video", 200

    except Exception as e:
        logger.error(f"Job {job_id}: Error durante el proceso de subtitulado - {str(e)}", exc_info=True)
        return str(e), "/caption-video", 500
