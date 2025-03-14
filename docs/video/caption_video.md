# Endpoint de Subtitulación de Video (v1)

## 1. Visión General

El endpoint `/v1/video/caption` forma parte de la API de Video y se encarga de agregar subtítulos a un archivo de video.  
- Recibe la URL del video, el texto de los subtítulos y diversas opciones de estilo.  
- Utiliza el servicio `process_captioning_v1` para generar el video subtitulado, el cual se sube a la nube y se retorna su URL. 🎥💬

## 2. Endpoint

- **URL:** `/v1/video/caption`  
- **Método:** `POST`

## 3. Solicitud

### Encabezados

- **`x-api-key`** (requerido): Clave API para autenticación. 🔑

### Parámetros en el Cuerpo

El cuerpo de la solicitud debe ser un objeto JSON con las siguientes propiedades:

- **`video_url`** (string, requerido): URL del archivo de video a subtitular.
- **`captions`** (string, opcional): Texto de los subtítulos a agregar al video.
- **`settings`** (object, opcional): Objeto con opciones de estilo para los subtítulos.  
  - Ejemplo de opciones:
    - `line_color`: Color de la línea.
    - `word_color`: Color de las palabras.
    - `outline_color`: Color del contorno.
    - `all_caps`: Booleano para mostrar en mayúsculas.
    - `max_words_per_line`: Número máximo de palabras por línea.
    - `x` y `y`: Posiciones en píxeles.
    - `position`: Posiciones permitidas: "bottom_left", "bottom_center", "bottom_right", "middle_left", "middle_center", "middle_right", "top_left", "top_center", "top_right".
    - `alignment`: Alineación ("left", "center", "right").
    - `font_family`: Familia tipográfica.
    - `font_size`: Tamaño de fuente.
    - `bold`, `italic`, `underline`, `strikeout`: Estilos de texto (booleanos).
    - `style`: Estilo de subtítulos ("classic", "karaoke", "highlight", "underline", "word_by_word").
    - `outline_width`: Ancho del contorno.
    - `spacing`: Espaciado.
    - `angle`: Ángulo de inclinación.
    - `shadow_offset`: Desplazamiento de la sombra.
- **`replace`** (array, opcional): Array de objetos con propiedades `find` y `replace` para realizar reemplazos de texto en los subtítulos.
- **`webhook_url`** (string, opcional): URL para recibir una notificación vía webhook al finalizar el proceso.
- **`id`** (string, opcional): Identificador para la solicitud.
- **`language`** (string, opcional): Código de idioma para los subtítulos (por ejemplo, "en", "es"). Por defecto se detecta automáticamente.

#### Ejemplo de Esquema para `settings`

```json
{
    "type": "object",
    "properties": {
        "line_color": {"type": "string"},
        "word_color": {"type": "string"},
        "outline_color": {"type": "string"},
        "all_caps": {"type": "boolean"},
        "max_words_per_line": {"type": "integer"},
        "x": {"type": "integer"},
        "y": {"type": "integer"},
        "position": {
            "type": "string",
            "enum": [
                "bottom_left", "bottom_center", "bottom_right",
                "middle_left", "middle_center", "middle_right",
                "top_left", "top_center", "top_right"
            ]
        },
        "alignment": {
            "type": "string",
            "enum": ["left", "center", "right"]
        },
        "font_family": {"type": "string"},
        "font_size": {"type": "integer"},
        "bold": {"type": "boolean"},
        "italic": {"type": "boolean"},
        "underline": {"type": "boolean"},
        "strikeout": {"type": "boolean"},
        "style": {
            "type": "string",
            "enum": ["classic", "karaoke", "highlight", "underline", "word_by_word"]
        },
        "outline_width": {"type": "integer"},
        "spacing": {"type": "integer"},
        "angle": {"type": "integer"},
        "shadow_offset": {"type": "integer"}
    },
    "additionalProperties": false
}
```

### Ejemplo de Solicitud

```json
{
    "video_url": "https://example.com/video.mp4",
    "captions": "Este es un texto de subtítulos de ejemplo.",
    "settings": {
        "line_color": "#FFFFFF",
        "word_color": "#000000",
        "outline_color": "#000000",
        "all_caps": false,
        "max_words_per_line": 10,
        "x": 20,
        "y": 40,
        "position": "bottom_left",
        "alignment": "left",
        "font_family": "Arial",
        "font_size": 24,
        "bold": false,
        "italic": false,
        "underline": false,
        "strikeout": false,
        "style": "classic",
        "outline_width": 2,
        "spacing": 2,
        "angle": 0,
        "shadow_offset": 2
    },
    "replace": [
        {
            "find": "sample",
            "replace": "example"
        }
    ],
    "webhook_url": "https://example.com/webhook",
    "id": "request-123",
    "language": "en"
}
```

```bash
curl -X POST \
     -H "x-api-key: TU_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
        "video_url": "https://example.com/video.mp4",
        "captions": "Este es un texto de subtítulos de ejemplo.",
        "settings": {
            "line_color": "#FFFFFF",
            "word_color": "#000000",
            "outline_color": "#000000",
            "all_caps": false,
            "max_words_per_line": 10,
            "x": 20,
            "y": 40,
            "position": "bottom_left",
            "alignment": "left",
            "font_family": "Arial",
            "font_size": 24,
            "bold": false,
            "italic": false,
            "underline": false,
            "strikeout": false,
            "style": "classic",
            "outline_width": 2,
            "spacing": 2,
            "angle": 0,
            "shadow_offset": 2
        },
        "replace": [
            {
                "find": "sample",
                "replace": "example"
            }
        ],
        "webhook_url": "https://example.com/webhook",
        "id": "request-123",
        "language": "en"
    }' \
    https://your-api-endpoint.com/v1/video/caption
```

## 4. Respuesta

### Respuesta Exitosa

La respuesta es un objeto JSON con las siguientes propiedades:

- **`code`** (integer): Código HTTP (200 para éxito).
- **`id`** (string): Identificador de la solicitud, si se proporcionó.
- **`job_id`** (string): Identificador único del trabajo.
- **`response`** (string): URL en la nube del video subtitulado.
- **`message`** (string): Mensaje de éxito.
- **`pid`** (integer): ID del proceso del worker que procesó la solicitud.
- **`queue_id`** (integer): ID de la cola utilizada.
- **`run_time`** (float): Tiempo de procesamiento en segundos.
- **`queue_time`** (float): Tiempo que la solicitud pasó en la cola en segundos.
- **`total_time`** (float): Tiempo total de procesamiento en segundos.
- **`queue_length`** (integer): Longitud actual de la cola.
- **`build_number`** (string): Número de build de la aplicación.

Ejemplo:

```json
{
    "code": 200,
    "id": "request-123",
    "job_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
    "response": "https://cloud.example.com/captioned-video.mp4",
    "message": "success",
    "pid": 12345,
    "queue_id": 140682639937472,
    "run_time": 5.234,
    "queue_time": 0.012,
    "total_time": 5.246,
    "queue_length": 0,
    "build_number": "1.0.0"
}
```

### Respuestas de Error

#### Parámetros Faltantes o Inválidos

**Código:** 400 Bad Request

```json
{
    "code": 400,
    "id": "request-123",
    "job_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
    "message": "Missing or invalid parameters",
    "pid": 12345,
    "queue_id": 140682639937472,
    "queue_length": 0,
    "build_number": "1.0.0"
}
```

#### Error de Fuente

**Código:** 400 Bad Request

```json
{
    "code": 400,
    "error": "The requested font 'InvalidFont' is not available. Please choose from the available fonts.",
    "available_fonts": ["Arial", "Times New Roman", "Courier New", ...],
    "pid": 12345,
    "queue_id": 140682639937472,
    "queue_length": 0,
    "build_number": "1.0.0"
}
```

#### Error Interno del Servidor

**Código:** 500 Internal Server Error

```json
{
    "code": 500,
    "id": "request-123",
    "job_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
    "error": "An unexpected error occurred during the captioning process.",
    "pid": 12345,
    "queue_id": 140682639937472,
    "queue_length": 0,
    "build_number": "1.0.0"
}
```

## 5. Manejo de Errores

El endpoint gestiona los siguientes errores comunes:
- **Parámetros faltantes o inválidos:** Se retorna un error 400 con un mensaje descriptivo. ❌
- **Error de Fuente:** Si la fuente solicitada no está disponible, se retorna un error 400 con la lista de fuentes disponibles. 🔠
- **Error Interno del Servidor:** Cualquier error inesperado en el proceso de subtitulado retorna un error 500. 🔥

Además, `app.py` incluye manejo de errores para la sobrecarga de la cola (429 Too Many Requests) si se alcanza el límite máximo.

## 6. Notas de Uso

- **`video_url`** debe ser una URL válida que apunte a un archivo de video. 📹
- **`captions`** es opcional; si no se proporciona, el video se retornará sin subtítulos.
- **`settings`** permite personalizar la apariencia y el comportamiento de los subtítulos.
- **`replace`** se puede usar para realizar reemplazos de texto en los subtítulos.
- **`webhook_url`** es opcional y se utiliza para recibir notificaciones cuando finaliza el proceso.
- **`id`** es opcional y se puede usar para identificar la solicitud.
- **`language`** es opcional y permite especificar el código del idioma (por defecto se detecta automáticamente). 🌐

## 7. Problemas Comunes

- 🚫 Proporcionar una `video_url` inválida o inaccesible.
- ⚠️ Solicitar una fuente no disponible en el objeto `settings`.
- 🚦 Exceder el límite máximo de la cola, generando un error 429 Too Many Requests.

## 8. Buenas Prácticas

- 🔍 Valida que la `video_url` sea accesible y válida antes de enviar la solicitud.
- 🔔 Usa el parámetro `webhook_url` para recibir notificaciones en lugar de hacer polling continuo.
- 🆔 Proporciona identificadores descriptivos en el parámetro `id` para facilitar el seguimiento.
- ✂️ Utiliza el parámetro `replace` con cuidado para evitar reemplazos no deseados.
- 📦 Considera cachear los videos subtitulados para solicitudes frecuentes y mejorar el rendimiento.