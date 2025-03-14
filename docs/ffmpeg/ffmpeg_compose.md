# Endpoint de Composición con FFmpeg

## 1. Visión General

El endpoint `/v1/ffmpeg/compose` es una API flexible y potente que permite a los usuarios componer comandos complejos de FFmpeg proporcionando archivos de entrada, filtros y opciones de salida.  
Este endpoint forma parte de la versión 1.0 de la API definida en `app.py` y está diseñado para gestionar tareas de procesamiento multimedia, como:  
- 🎥 Manipulación de video y audio  
- 🔄 Transcodificación  
- ✂️ Concatenación y filtrado  

## 2. Endpoint

- **Ruta URL:** `/v1/ffmpeg/compose`  
- **Método HTTP:** `POST`

## 3. Solicitud

### Encabezados

- `x-api-key` (requerido): Clave API para autenticación.

### Parámetros en el Cuerpo

El cuerpo de la solicitud debe ser un objeto JSON con las siguientes propiedades:

- **`inputs`** (requerido, array): Lista de objetos de archivo de entrada, donde cada objeto incluye:  
  - `file_url` (requerido, string): URL del archivo de entrada.  
  - `options` (opcional, array): Lista de objetos con:  
    - `option` (requerido, string): Opción de FFmpeg.  
    - `argument` (opcional, string, number o null): Argumento para la opción.
- **`filters`** (opcional, array): Lista de objetos de filtro, donde cada objeto incluye:  
  - `filter` (requerido, string): Filtro de FFmpeg.
- **`outputs`** (requerido, array): Lista de objetos de opciones de salida, donde cada objeto contiene:  
  - `options` (requerido, array): Lista de objetos con:  
    - `option` (requerido, string): Opción de FFmpeg.  
    - `argument` (opcional, string, number o null): Argumento para la opción.
- **`global_options`** (opcional, array): Lista de objetos de opciones globales, donde cada objeto contiene:  
  - `option` (requerido, string): Opción global de FFmpeg.  
  - `argument` (opcional, string, number o null): Argumento para la opción.
- **`metadata`** (opcional, object): Objeto para especificar qué metadata incluir en la respuesta, con las siguientes propiedades:  
  - `thumbnail` (opcional, boolean): Incluir miniatura del archivo de salida.  
  - `filesize` (opcional, boolean): Incluir tamaño del archivo.  
  - `duration` (opcional, boolean): Incluir duración del archivo.  
  - `bitrate` (opcional, boolean): Incluir tasa de bits.  
  - `encoder` (opcional, boolean): Incluir encoder utilizado.
- **`webhook_url`** (requerido, string): URL a la que se enviará el resultado mediante webhook.  
- **`id`** (requerido, string): Identificador único para la solicitud.

### Ejemplo de Solicitud

```json
{
  "inputs": [
    {
      "file_url": "https://ejemplo.com/video1.mp4",
      "options": [
        {
          "option": "-ss",
          "argument": 10
        },
        {
          "option": "-t",
          "argument": 20
        }
      ]
    },
    {
      "file_url": "https://ejemplo.com/video2.mp4"
    }
  ],
  "filters": [
    {
      "filter": "hflip"
    }
  ],
  "outputs": [
    {
      "options": [
        {
          "option": "-c:v",
          "argument": "libx264"
        },
        {
          "option": "-crf",
          "argument": 23
        }
      ]
    }
  ],
  "global_options": [
    {
      "option": "-y"
    }
  ],
  "metadata": {
    "thumbnail": true,
    "filesize": true,
    "duration": true,
    "bitrate": true,
    "encoder": true
  },
  "webhook_url": "https://ejemplo.com/webhook",
  "id": "identificador-unico"
}
```

```bash
curl -X POST \
  https://api.ejemplo.com/v1/ffmpeg/compose \
  -H 'x-api-key: TU_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "inputs": [
      {
        "file_url": "https://ejemplo.com/video1.mp4",
        "options": [
          {
            "option": "-ss",
            "argument": 10
          },
          {
            "option": "-t",
            "argument": 20
          }
        ]
      },
      {
        "file_url": "https://ejemplo.com/video2.mp4"
      }
    ],
    "filters": [
      {
        "filter": "hflip"
      }
    ],
    "outputs": [
      {
        "options": [
          {
            "option": "-c:v",
            "argument": "libx264"
          },
          {
            "option": "-crf",
            "argument": 23
          }
        ]
      }
    ],
    "global_options": [
      {
        "option": "-y"
      }
    ],
    "metadata": {
      "thumbnail": true,
      "filesize": true,
      "duration": true,
      "bitrate": true,
      "encoder": true
    },
    "webhook_url": "https://ejemplo.com/webhook",
    "id": "identificador-unico"
  }'
```

## 4. Respuesta

### Respuesta Exitosa

La respuesta se enviará a la `webhook_url` especificada como un objeto JSON que incluye:

- **`endpoint`** (string): La ruta del endpoint (`/v1/ffmpeg/compose`).  
- **`code`** (number): Código HTTP (200 en caso de éxito).  
- **`id`** (string): Identificador único de la solicitud.  
- **`job_id`** (string): Identificador único asignado al trabajo.  
- **`response`** (array): Lista de objetos de archivo de salida, donde cada objeto puede incluir:  
  - `file_url` (string): URL del archivo subido.  
  - `thumbnail_url` (string, opcional): URL de la miniatura, si se solicitó.  
  - `filesize` (number, opcional): Tamaño del archivo.  
  - `duration` (number, opcional): Duración del archivo.  
  - `bitrate` (number, opcional): Tasa de bits del archivo.  
  - `encoder` (string, opcional): Encoder utilizado.
- **`message`** (string): Mensaje de éxito ("success").  
- **`pid`** (number): ID del proceso del worker que procesó la solicitud.  
- **`queue_id`** (number): ID de la cola utilizada.  
- **`run_time`** (number): Tiempo de ejecución (en segundos).  
- **`queue_time`** (number): Tiempo en la cola (en segundos).  
- **`total_time`** (number): Tiempo total de procesamiento (en segundos).  
- **`queue_length`** (number): Longitud actual de la cola.  
- **`build_number`** (string): Número de build de la aplicación.

### Respuestas de Error

- **400 Bad Request**: El payload es inválido o faltan parámetros requeridos.  
- **401 Unauthorized**: API key inválida o ausente.  
- **429 Too Many Requests**: Se alcanzó el límite máximo de la cola.  
- **500 Internal Server Error**: Error inesperado durante el procesamiento.

Ejemplo de respuesta de error:

```json
{
  "code": 400,
  "id": "identificador-unico",
  "job_id": "job-id",
  "message": "Payload inválido: 'inputs' es una propiedad requerida",
  "pid": 123,
  "queue_id": 456,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

## 5. Manejo de Errores

La API gestiona distintos tipos de errores, tales como:  
- ❌ Parámetros faltantes o inválidos (400).  
- 🔒 Fallos de autenticación (401).  
- ⏱️ Límite de cola alcanzado (429).  
- 🔥 Errores internos inesperados (500).  

El manejo de errores en `app.py` también contempla situaciones de sobrecarga en la cola.

## 6. Notas de Uso

- 📌 El array `inputs` debe contener al menos un objeto de archivo de entrada.  
- 📌 El array `outputs` debe tener al menos un objeto de opciones de salida.  
- ⚙️ El array `filters` es opcional y se utiliza para aplicar filtros de FFmpeg a los archivos de entrada.  
- ⚙️ El array `global_options` es opcional para especificar opciones globales de FFmpeg.  
- 🔗 El parámetro `webhook_url` es obligatorio y define la URL para recibir la respuesta.  
- 🆔 El parámetro `id` es obligatorio y debe ser único.

## 7. Problemas Comunes

- 🚫 URLs de archivos de entrada inválidas o mal formadas.  
- ⚠️ Opciones o filtros de FFmpeg no soportados o mal especificados.  
- ⏳ Exceso en la longitud de la cola, generando un error 429.  
- 🌐 Problemas de conectividad que impidan la entrega del webhook.

## 8. Buenas Prácticas

- 🔍 Valida las URLs de los archivos de entrada para confirmar su accesibilidad.  
- ✅ Prueba tus comandos de FFmpeg localmente antes de enviarlos a la API.  
- 📈 Monitorea la longitud de la cola y ajusta el límite máximo según la demanda.  
- 🔄 Implementa mecanismos de reintento para webhook fallidos.  
- 🆔 Utiliza identificadores únicos y descriptivos para cada solicitud, facilitando la resolución de problemas.