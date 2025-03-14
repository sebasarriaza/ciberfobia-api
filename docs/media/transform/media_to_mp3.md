# Endpoint de Conversión a MP3

## 1. Visión General

El endpoint `/v1/media/transform/mp3` forma parte de la funcionalidad de transformación de medios de la API.  
Permite convertir archivos multimedia (audio o video) al formato MP3.  
Está integrado en la versión 1.0 de la API.

## 2. Endpoint

```
POST /v1/media/transform/mp3
```

## 3. Solicitud

### Encabezados

- **`x-api-key`** (requerido): Clave API para autenticación.

### Parámetros en el Cuerpo

- **`media_url`** (requerido, string): URL del archivo multimedia a convertir.
- **`webhook_url`** (opcional, string): URL para recibir una notificación vía webhook al finalizar la conversión.
- **`id`** (opcional, string): Identificador único para la solicitud.
- **`bitrate`** (opcional, string): Bitrate deseado para el archivo MP3 de salida, en formato `<valor>k` (por ejemplo, `128k`). Si no se especifica, se usa `128k` por defecto.

El decorador `validate_payload` en la ruta aplica el siguiente esquema JSON:

```json
{
    "type": "object",
    "properties": {
        "media_url": {"type": "string", "format": "uri"},
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"},
        "bitrate": {"type": "string", "pattern": "^[0-9]+k$"}
    },
    "required": ["media_url"],
    "additionalProperties": False
}
```

### Ejemplo de Solicitud

```json
{
    "media_url": "https://ejemplo.com/video.mp4",
    "webhook_url": "https://ejemplo.com/webhook",
    "id": "identificador-unico",
    "bitrate": "192k"
}
```

```bash
curl -X POST \
     -H "x-api-key: TU_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"media_url": "https://ejemplo.com/video.mp4", "webhook_url": "https://ejemplo.com/webhook", "id": "identificador-unico", "bitrate": "192k"}' \
     https://tu-api-endpoint.com/v1/media/transform/mp3
```

## 4. Respuesta

### Respuesta Exitosa

La respuesta exitosa sigue la estructura general definida en `app.py`. Ejemplo:

```json
{
    "endpoint": "/v1/media/transform/mp3",
    "code": 200,
    "id": "identificador-unico",
    "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
    "response": "https://almacenamiento-cloud.ejemplo.com/archivo-convertido.mp3",
    "message": "success",
    "pid": 12345,
    "queue_id": 6789,
    "run_time": 5.234,
    "queue_time": 0.123,
    "total_time": 5.357,
    "queue_length": 0,
    "build_number": "1.0.0"
}
```

### Respuestas de Error

- **400 Bad Request:** Se retorna cuando el payload es inválido o faltan parámetros requeridos.
- **401 Unauthorized:** Se retorna cuando falta o es inválida la cabecera `x-api-key`.
- **500 Internal Server Error:** Se retorna cuando ocurre un error inesperado durante la conversión.

Ejemplo de respuesta de error:

```json
{
    "code": 400,
    "id": "identificador-unico",
    "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
    "message": "Payload inválido: 'media_url' es una propiedad requerida",
    "pid": 12345,
    "queue_id": 6789,
    "queue_length": 0,
    "build_number": "1.0.0"
}
```

## 5. Manejo de Errores

El endpoint gestiona los siguientes errores comunes:

- ❌ Parámetros faltantes o inválidos (ej.: `media_url` o `bitrate`).
- 🔐 Fallos de autenticación (clave API inválida o ausente).
- 🚦 Si se excede el límite máximo de la cola, se retorna un error 429 (Too Many Requests).
- 🔥 Errores inesperados durante la conversión retornan un error 500.

## 6. Notas de Uso

- 🔗 El parámetro `media_url` debe apuntar a un archivo multimedia válido y accesible.
- 🔔 Si se proporciona `webhook_url`, se enviará una notificación al finalizar la conversión.
- 🆔 El parámetro `id` facilita la identificación y seguimiento de la solicitud.
- 🎚️ El parámetro `bitrate` permite especificar el bitrate deseado; si no se indica, se utiliza `128k` por defecto.

## 7. Problemas Comunes

- 🚫 Proporcionar una `media_url` inválida o inaccesible.
- ⚠️ Intentar convertir formatos de medios no soportados.
- ⏳ Exceder el límite máximo de la cola, lo que resultará en un error 429.

## 8. Buenas Prácticas

- 🔍 Valida que la `media_url` sea válida y accesible antes de enviar la solicitud.
- 🔔 Considera utilizar `webhook_url` para recibir notificaciones en lugar de hacer polling continuo.
- 🆔 Usa identificadores únicos para cada solicitud y facilitar el seguimiento en los registros.
- 🔄 Implementa mecanismos de reintento para errores transitorios o saturación de la cola.
- 📈 Monitorea los registros de la API para detectar errores o problemas durante el proceso de conversión.