# Endpoint de Concatenación de Video

## 1. Visión General

El endpoint `/v1/video/concatenate` forma parte de la API de Video y se encarga de combinar múltiples archivos de video en un solo archivo.  
- Los videos se concatenan en el orden en que aparecen en la solicitud.  
- El video resultante se sube a la nube y se retorna la URL de acceso. 🎥🔗

## 2. Endpoint

- **Ruta URL:** `/v1/video/concatenate`  
- **Método HTTP:** `POST`

## 3. Solicitud

### Encabezados

- **`x-api-key`** (requerido): Clave API para autenticación. 🔑

### Parámetros en el Cuerpo

El cuerpo de la solicitud debe ser un objeto JSON con las siguientes propiedades:

- **`video_urls`** (requerido, array de objetos):  
  - Cada objeto debe tener la propiedad `video_url` (string, formato URI) que contiene la URL del video.  
- **`webhook_url`** (opcional, string, formato URI):  
  - URL a la que se enviará la respuesta mediante webhook.  
- **`id`** (opcional, string):  
  - Identificador para la solicitud.

El decorador `validate_payload` aplica el siguiente esquema JSON:

```json
{
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
    "additionalProperties": false
}
```

### Ejemplo de Solicitud

```json
{
    "video_urls": [
        {"video_url": "https://example.com/video1.mp4"},
        {"video_url": "https://example.com/video2.mp4"},
        {"video_url": "https://example.com/video3.mp4"}
    ],
    "webhook_url": "https://example.com/webhook",
    "id": "request-123"
}
```

```bash
curl -X POST \
     -H "x-api-key: TU_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
        "video_urls": [
            {"video_url": "https://example.com/video1.mp4"},
            {"video_url": "https://example.com/video2.mp4"},
            {"video_url": "https://example.com/video3.mp4"}
        ],
        "webhook_url": "https://example.com/webhook",
        "id": "request-123"
     }' \
     https://tu-api-endpoint.com/v1/video/concatenate
```

## 4. Respuesta

### Respuesta Exitosa

La respuesta exitosa sigue el formato general definido en `app.py`. Por ejemplo:

```json
{
    "endpoint": "/v1/video/concatenate",
    "code": 200,
    "id": "request-123",
    "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
    "response": "https://almacenamiento-cloud.example.com/combined-video.mp4",
    "message": "success",
    "pid": 12345,
    "queue_id": 6789,
    "run_time": 10.234,
    "queue_time": 2.345,
    "total_time": 12.579,
    "queue_length": 0,
    "build_number": "1.0.0"
}
```

El campo `response` contiene la URL del video combinado subido a la nube.

### Respuestas de Error

- **400 Bad Request:**  
  Se retorna cuando el cuerpo de la solicitud es inválido o faltan parámetros.

  ```json
  {
    "code": 400,
    "message": "Invalid request payload"
  }
  ```

- **401 Unauthorized:**  
  Se retorna cuando falta o es inválido el encabezado `x-api-key`.

  ```json
  {
    "code": 401,
    "message": "Unauthorized"
  }
  ```

- **429 Too Many Requests:**  
  Se retorna cuando se alcanza el límite máximo de la cola.

  ```json
  {
    "code": 429,
    "id": "request-123",
    "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
    "message": "MAX_QUEUE_LENGTH (100) reached",
    "pid": 12345,
    "queue_id": 6789,
    "queue_length": 100,
    "build_number": "1.0.0"
  }
  ```

- **500 Internal Server Error:**  
  Se retorna cuando ocurre un error inesperado durante la concatenación de video.

  ```json
  {
    "code": 500,
    "message": "An error occurred during video concatenation"
  }
  ```

## 5. Manejo de Errores

El endpoint gestiona los siguientes errores comunes:
- **Parámetros faltantes o inválidos:** Retorna un error 400 si el cuerpo no cumple el esquema JSON. ❌
- **API key inválida o ausente:** Retorna un error 401. 🔐
- **Límite de cola alcanzado:** Retorna un error 429 si la longitud de la cola supera el límite definido. 🚦
- **Errores inesperados durante la concatenación:** Retorna un error 500 con detalles del problema. 🔥

## 6. Notas de Uso

- Los archivos de video a concatenar deben ser accesibles mediante las URLs proporcionadas. 📹
- El orden de los videos en el array `video_urls` determina el orden de concatenación. 🔢
- Si se proporciona `webhook_url`, la respuesta se enviará a dicha URL mediante webhook. 🔔
- El parámetro `id` es opcional y se utiliza para identificar la solicitud. 🆔

## 7. Problemas Comunes

- 🚫 Proporcionar URLs de video inválidas o inaccesibles.
- ⏳ Exceder el límite máximo de la cola, lo que resultará en un error 429.
- 🔥 Errores inesperados durante el proceso de concatenación que generan un error 500.

## 8. Buenas Prácticas

- 🔍 Valida las URLs de los videos antes de enviar la solicitud para asegurarte de que sean accesibles y correctas.
- 📊 Monitorea la longitud de la cola y ajusta la variable `MAX_QUEUE_LENGTH` según la demanda.
- 🔄 Implementa mecanismos de reintento para manejar errores temporales o saturación de la cola.
- 🆔 Usa identificadores descriptivos en el parámetro `id` para facilitar el seguimiento y la correlación de solicitudes.