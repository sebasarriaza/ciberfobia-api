# Documentación de la Transcripción de Medios

## Visión General

El endpoint de transcripción de medios forma parte del conjunto de la API v1 y ofrece capacidades de transcripción y traducción de audio/video.  
Este endpoint utiliza un sistema de colas para manejar tareas de transcripción de larga duración y soporta webhooks para procesamiento asíncrono.  
Está integrado en la aplicación principal de Flask como un Blueprint y permite recibir resultados de transcripción tanto de forma directa como mediante URLs de almacenamiento en la nube.

## Endpoint

- **URL:** `/v1/media/transcribe`
- **Método:** `POST`
- **Blueprint:** `v1_media_transcribe_bp`

## Solicitud

### Encabezados

- **`x-api-key`**: (requerido) Clave de autenticación para el acceso a la API. 🔑
- **`Content-Type`**: (requerido) Debe ser `application/json`. 📄

### Parámetros en el Cuerpo

#### Parámetros Requeridos
- **`media_url`** (string)  
  - **Formato:** URI  
  - **Descripción:** URL del archivo multimedia que se va a transcribir. 🌐

#### Parámetros Opcionales
- **`task`** (string)  
  - **Valores permitidos:** `"transcribe"`, `"translate"`  
  - **Predeterminado:** `"transcribe"`  
  - **Descripción:** Especifica si se debe transcribir o traducir el audio. 🎙️🔄
  
- **`include_text`** (boolean)  
  - **Predeterminado:** `true`  
  - **Descripción:** Incluir la transcripción en texto plano en la respuesta. 📝
  
- **`include_srt`** (boolean)  
  - **Predeterminado:** `false`  
  - **Descripción:** Incluir subtítulos en formato SRT en la respuesta. 💬
  
- **`include_segments`** (boolean)  
  - **Predeterminado:** `false`  
  - **Descripción:** Incluir segmentos con marcas de tiempo en la respuesta. ⏱️
  
- **`word_timestamps`** (boolean)  
  - **Predeterminado:** `false`  
  - **Descripción:** Incluir marcas de tiempo para cada palabra. ⏲️
  
- **`response_type`** (string)  
  - **Valores permitidos:** `"direct"`, `"cloud"`  
  - **Predeterminado:** `"direct"`  
  - **Descripción:** Define si se retornarán los resultados directamente o mediante URLs de almacenamiento en la nube. ☁️
  
- **`language`** (string)  
  - **Descripción:** Código del idioma de origen para la transcripción. 🌍
  
- **`webhook_url`** (string)  
  - **Formato:** URI  
  - **Descripción:** URL para recibir los resultados de la transcripción de forma asíncrona. 🔗
  
- **`id`** (string)  
  - **Descripción:** Identificador personalizado para el trabajo de transcripción. 🆔

### Ejemplo de Solicitud

```bash
curl -X POST "https://api.ejemplo.com/v1/media/transcribe" \
  -H "x-api-key: tu_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "media_url": "https://ejemplo.com/media/archivo.mp3",
    "task": "transcribe",
    "include_text": true,
    "include_srt": true,
    "include_segments": true,
    "response_type": "cloud",
    "webhook_url": "https://tu-webhook.com/callback",
    "id": "trabajo-personalizado-123"
  }'
```

## Respuesta

### Respuesta Inmediata (202 Accepted)

Cuando se proporciona un `webhook_url`, la API devuelve un acuse de recibo inmediato:

```json
{
  "code": 202,
  "id": "trabajo-personalizado-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "processing",
  "pid": 12345,
  "queue_id": 67890,
  "max_queue_length": "unlimited",
  "queue_length": 1,
  "build_number": "1.0.0"
}
```

### Respuesta Exitosa (vía Webhook)

Para `response_type` directo:

```json
{
  "endpoint": "/v1/transcribe/media",
  "code": 200,
  "id": "trabajo-personalizado-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": {
    "text": "Contenido de la transcripción...",
    "srt": "Contenido en formato SRT...",
    "segments": [...],
    "text_url": null,
    "srt_url": null,
    "segments_url": null
  },
  "message": "success",
  "pid": 12345,
  "queue_id": 67890,
  "run_time": 5.234,
  "queue_time": 0.123,
  "total_time": 5.357,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

Para `response_type` en la nube:

```json
{
  "endpoint": "/v1/transcribe/media",
  "code": 200,
  "id": "trabajo-personalizado-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": {
    "text": null,
    "srt": null,
    "segments": null,
    "text_url": "https://almacenamiento.ejemplo.com/texto.txt",
    "srt_url": "https://almacenamiento.ejemplo.com/subtitulos.srt",
    "segments_url": "https://almacenamiento.ejemplo.com/segmentos.json"
  },
  "message": "success",
  "pid": 12345,
  "queue_id": 67890,
  "run_time": 5.234,
  "queue_time": 0.123,
  "total_time": 5.357,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Respuestas de Error

#### Cola Llena (429 Too Many Requests)

```json
{
  "code": 429,
  "id": "trabajo-personalizado-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "MAX_QUEUE_LENGTH (100) reached",
  "pid": 12345,
  "queue_id": 67890,
  "queue_length": 100,
  "build_number": "1.0.0"
}
```

#### Error del Servidor (500 Internal Server Error)

```json
{
  "endpoint": "/v1/transcribe/media",
  "code": 500,
  "id": "trabajo-personalizado-123",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": null,
  "message": "Detalles del mensaje de error",
  "pid": 12345,
  "queue_id": 67890,
  "run_time": 0.123,
  "queue_time": 0.056,
  "total_time": 0.179,
  "queue_length": 1,
  "build_number": "1.0.0"
}
```

## Manejo de Errores

### Errores Comunes
- **Clave API inválida:** 401 Unauthorized 🔐
- **Payload JSON inválido:** 400 Bad Request 📄
- **Faltan campos requeridos:** 400 Bad Request ⚠️
- **`media_url` inválida:** 400 Bad Request 🌐
- **Cola llena:** 429 Too Many Requests 🚦
- **Error en el procesamiento:** 500 Internal Server Error 🔥

### Errores de Validación
El endpoint valida estrictamente el payload usando JSON Schema. Entre los errores de validación más comunes se incluyen:
- Formato de URI inválido para `media_url` o `webhook_url`
- Valor de `task` inválido (debe ser "transcribe" o "translate")
- Valor de `response_type` inválido (debe ser "direct" o "cloud")
- Propiedades desconocidas en el cuerpo de la solicitud

## Notas de Uso

- **Procesamiento con Webhook**  
  - Cuando se proporciona `webhook_url`, la solicitud se procesa de forma asíncrona.
  - La API retorna un acuse de recibo inmediato (202) con un `job_id`.
  - Los resultados finales se envían a `webhook_url` al finalizar el procesamiento. 🔔

- **Gestión de la Cola**  
  - Las solicitudes con `webhook_url` se ponen en cola para su procesamiento.
  - La variable de entorno `MAX_QUEUE_LENGTH` controla el tamaño de la cola.
  - Establece `MAX_QUEUE_LENGTH` a 0 para una cola ilimitada. 📊

- **Gestión de Archivos**  
  - Para `response_type` en la nube, los archivos temporales se eliminan automáticamente.
  - Los resultados se suben a almacenamiento en la nube antes de su eliminación.
  - Las URLs en la respuesta ofrecen acceso a los archivos almacenados. ☁️

## Problemas Comunes

1. **Acceso a Medios**  
   - Verifica que `media_url` sea accesible públicamente.  
   - Asegúrate de que el formato del archivo multimedia sea soportado.  
   - Revisa que el archivo no esté corrupto. 📶

2. **Entrega de Webhook**  
   - Comprueba que `webhook_url` sea accesible públicamente.  
   - Implementa lógica de reintentos en el endpoint de webhook.  
   - Monitorea la disponibilidad del endpoint de webhook. 🔄

3. **Uso de Recursos**  
   - Archivos multimedia grandes pueden requerir un tiempo considerable de procesamiento.  
   - Monitorea la longitud de la cola en entornos de producción.  
   - Considera implementar límites de tamaño en las solicitudes. ⏳

## Buenas Prácticas

1. **Manejo de Solicitudes**  
   - Siempre proporciona un `id` único para el seguimiento del trabajo. 🆔  
   - Implementa lógica de reintentos para los webhooks fallidos. 🔁  
   - Almacena el `job_id` para correlacionar los resultados. 📋

2. **Gestión de Recursos**  
   - Monitorea la longitud de la cola en producción. 📈  
   - Implementa manejo de tiempos de espera adecuados. ⏲️  
   - Utiliza `response_type` en la nube para archivos grandes. ☁️

3. **Manejo de Errores**  
   - Implementa un manejo exhaustivo de errores para los webhooks. 🚨  
   - Registra el `job_id` en todas las operaciones relacionadas. 📝  
   - Monitorea los tiempos de procesamiento y las tasas de error. 📊

4. **Seguridad**  
   - Utiliza HTTPS para `media_url` y `webhook_url`. 🔒  
   - Implementa autenticación en el webhook. 🛡️  
   - Valida los tipos de archivos multimedia antes de procesarlos. ✅