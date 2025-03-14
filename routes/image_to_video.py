from flask import Blueprint
from app_utils import *
import logging
from services.image_to_video import process_image_to_video
from services.authentication import authenticate
from services.cloud_storage import upload_file

# 📌 Crear un Blueprint para el endpoint de conversión de imagen a video
image_to_video_bp = Blueprint('image_to_video', __name__)
logger = logging.getLogger(__name__)

# 🚀 Endpoint para convertir una imagen en un video:
# - Protegido por autenticación
# - Valida el payload JSON conforme al esquema definido
# - Procesa la solicitud en cola para evitar bloqueos
@image_to_video_bp.route('/image-to-video', methods=['POST'])
@authenticate  # 🔑 Verifica que la solicitud incluya una API key válida
@validate_payload({
    "type": "object",
    "properties": {
        "image_url": {"type": "string", "format": "uri"},
        "length": {"type": "number", "minimum": 1, "maximum": 60},
        "frame_rate": {"type": "integer", "minimum": 15, "maximum": 60},
        "zoom_speed": {"type": "number", "minimum": 0, "maximum": 100},
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"}
    },
    "required": ["image_url"],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)
def image_to_video(job_id, data):
    # 📥 Extraer parámetros del payload
    image_url = data.get('image_url')
    length = data.get('length', 5)
    frame_rate = data.get('frame_rate', 30)
    # 🔄 Ajustar el valor del zoom_speed: convertir de porcentaje a fracción
    zoom_speed = data.get('zoom_speed', 3) / 100
    webhook_url = data.get('webhook_url')
    id = data.get('id')

    logger.info(f"Job {job_id}: Solicitud de conversión de imagen a video recibida para {image_url}")

    try:
        # 🎬 Procesar la conversión de imagen a video
        output_filename = process_image_to_video(
            image_url, length, frame_rate, zoom_speed, job_id, webhook_url
        )

        # ☁️ Subir el archivo resultante a almacenamiento en la nube
        cloud_url = upload_file(output_filename)

        # 📤 Registrar y retornar la URL del video subido, junto con la ruta y el código 200
        logger.info(f"Job {job_id}: Video convertido subido a la nube: {cloud_url}")
        return cloud_url, "/image-to-video", 200

    except Exception as e:
        logger.error(f"Job {job_id}: Error al procesar la conversión de imagen a video: {str(e)}", exc_info=True)
        return str(e), "/image-to-video", 500
