# Endpoint de Transformación de Imagen a Video

## 1. Visión General

El endpoint `/v1/image/transform/video` forma parte de la aplicación API en Flask y se encarga de convertir una imagen en un archivo de video.  
Está registrado en `app.py` bajo el blueprint `v1_image_transform_video_bp`, importado desde el módulo `routes.v1.image.transform.image_to_video`.

## 2. Endpoint

- **Ruta URL:** `/v1/image/transform/video`  
- **Método HTTP:** `POST`

## 3. Solicitud

### Encabezados

- `x-api-key` (requerido): Clave API para autenticación.

### Parámetros en el Cuerpo

El cuerpo de la solicitud debe estar en formato JSON e incluir los siguientes parámetros:

| Parámetro      | Tipo    | Requerido | Descripción                                                                          |
|----------------|---------|-----------|--------------------------------------------------------------------------------------|
| `image_url`    | string  | Sí        | URL de la imagen a convertir en video.                                               |
| `length`       | number  | No        | Duración deseada del video en segundos (predeterminado: 5).                          |
| `frame_rate`   | integer | No        | Número de fotogramas por segundo del video de salida (predeterminado: 30).           |
| `zoom_speed`   | number  | No        | Velocidad del efecto de zoom (rango 0-100, predeterminado: 3).                       |
| `webhook_url`  | string  | No        | URL para recibir una notificación vía webhook al finalizar la conversión.            |
| `id`           | string  | No        | Identificador opcional para la solicitud.                                            |

El decorador `validate_payload` en el módulo `routes.v1.image.transform.image_to_video` aplica el siguiente esquema JSON:

```json
{
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
}
```

### Ejemplo de Solicitud

```json
{
    "image_url": "https://ejemplo.com/imagen.jpg",
    "length": 10,
    "frame_rate": 24,
    "zoom_speed": 5,
    "webhook_url": "https://ejemplo.com/webhook",
    "id": "solicitud-123"
}
```

```bash
curl -X POST \
     -H "x-api-key: TU_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"image_url": "https://ejemplo.com/imagen.jpg", "length": 10, "frame_rate": 24, "zoom_speed": 5, "webhook_url": "https://ejemplo.com/webhook", "id": "solicitud-123"}' \
     http://tu-api-endpoint/v1/image/transform/video
```

## 4. Respuesta

### Respuesta Exitosa

Al procesarse correctamente, el endpoint retorna una respuesta JSON con la siguiente estructura:

```json
{
    "code": 200,
    "id": "solicitud-123",
    "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
    "response": "https://almacenamiento-cloud.ejemplo.com/video-convertido.mp4",
    "message": "success",
    "run_time": 2.345,
    "queue_time": 0.123,
    "total_time": 2.468,
    "pid": 12345,
    "queue_id": 1234567890,
    "queue_length": 0,
    "build_number": "1.0.0"
}
```

*El campo `response` contiene la URL del video convertido y subido al almacenamiento en la nube.*

### Respuestas de Error

#### 429 Too Many Requests

Si se alcanza el límite máximo de la cola, se retorna un error 429:

```json
{
    "code": 429,
    "id": "solicitud-123",
    "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
    "message": "MAX_QUEUE_LENGTH (10) reached",
    "pid": 12345,
    "queue_id": 1234567890,
    "queue_length": 10,
    "build_number": "1.0.0"
}
```

#### 500 Internal Server Error

Si ocurre una excepción durante la conversión, se retorna un error 500:

```json
{
    "code": 500,
    "id": "solicitud-123",
    "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
    "message": "Mensaje de error descriptivo",
    "pid": 12345,
    "queue_id": 1234567890,
    "queue_length": 0,
    "build_number": "1.0.0"
}
```

## 5. Manejo de Errores

El endpoint gestiona varios tipos de errores:
- **Parámetros faltantes o inválidos:** Si el cuerpo de la solicitud carece de parámetros obligatorios o contiene valores fuera del rango permitido, se retorna un error 400.
- **Límite de cola excedido:** Si se alcanza el máximo de solicitudes en cola (y `bypass_queue` está en `False`), se retorna un error 429.
- **Errores durante la conversión:** Cualquier excepción durante el proceso de conversión retorna un error 500.

## 6. Notas de Uso

- ✅ El parámetro `image_url` debe ser una URL válida que apunte a una imagen accesible.  
- ⏱️ El parámetro `length` define la duración del video (en segundos) y debe estar entre 1 y 60.  
- 🎞️ El parámetro `frame_rate` determina la cantidad de fotogramas por segundo, aceptando valores entre 15 y 60.  
- 🔍 El parámetro `zoom_speed` controla la velocidad del efecto de zoom, en un rango de 0 a 100.  
- 🔗 El parámetro `webhook_url` es opcional y permite recibir notificaciones al completar la conversión.  
- 🆔 El parámetro `id` es opcional y sirve para identificar la solicitud.

## 7. Problemas Comunes

- 🚫 Una URL de imagen inválida o inaccesible puede provocar errores en el procesamiento.  
- ⚠️ Valores fuera de los rangos permitidos para `length`, `frame_rate` o `zoom_speed` retornarán un error 400.  
- ⏳ Si la cola de procesamiento está saturada, se devolverá un error 429.  
- 🌐 Problemas de conectividad pueden afectar la entrega del webhook.

## 8. Buenas Prácticas

- 🔎 Verifica que la URL de la imagen es válida y accesible antes de enviar la solicitud.  
- 🔔 Utiliza el parámetro `webhook_url` para recibir notificaciones en lugar de hacer polling continuo.  
- 🆔 Asigna identificadores únicos y descriptivos a cada solicitud para facilitar el seguimiento en los logs.  
- ⚡ Considera usar `bypass_queue` para solicitudes sensibles al tiempo si es necesario.