# Endpoint para Ejecutar Código Python

## 1. Visión General

El endpoint `/v1/code/execute/python` permite a los usuarios ejecutar código Python en el servidor.  
Está integrado en la versión 1.0 de la API definida en `app.py` y ofrece un entorno seguro y controlado para la ejecución de código, con:

- ✅ Validación de entrada  
- 📥 Captura de la salida (stdout y stderr)  
- ⏱️ Manejo de tiempos de espera  

## 2. Endpoint

- **Ruta URL:** `/v1/code/execute/python`  
- **Método HTTP:** `POST`

## 3. Solicitud

### Encabezados

- `x-api-key` (requerido): Clave API para autenticación.

### Parámetros en el Cuerpo

El cuerpo de la solicitud debe ser un objeto JSON con las siguientes propiedades:

- **`code`** (string, requerido): Código Python a ejecutar.  
- **`timeout`** (integer, opcional): Tiempo máximo de ejecución en segundos (entre 1 y 300). Valor predeterminado: 30 segundos.  
- **`webhook_url`** (string, opcional): URL para recibir el resultado de la ejecución mediante un webhook.  
- **`id`** (string, opcional): Identificador único para la solicitud.

El directivo `validate_payload` en la ruta aplica el siguiente esquema JSON:

```json
{
    "type": "object",
    "properties": {
        "code": {"type": "string"},
        "timeout": {"type": "integer", "minimum": 1, "maximum": 300},
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"}
    },
    "required": ["code"],
    "additionalProperties": False
}
```

### Ejemplo de Solicitud

**Payload:**

```json
{
    "code": "print('¡Hola, Mundo!')",
    "timeout": 10,
    "webhook_url": "https://ejemplo.com/webhook",
    "id": "identificador-unico-solicitud"
}
```

**Comando cURL:**

```bash
curl -X POST \
     -H "x-api-key: TU_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"code": "print(\'¡Hola, Mundo!\')", "timeout": 10, "webhook_url": "https://ejemplo.com/webhook", "id": "identificador-unico-solicitud"}' \
     http://tu-api-endpoint/v1/code/execute/python
```

## 4. Respuesta

### Respuesta Exitosa

La respuesta sigue el formato general definido en `app.py`. Ejemplo:

```json
{
    "endpoint": "/v1/code/execute/python",
    "code": 200,
    "id": "identificador-unico-solicitud",
    "job_id": "id-trabajo-generado",
    "response": {
        "result": null,
        "stdout": "¡Hola, Mundo!\n",
        "stderr": "",
        "exit_code": 0
    },
    "message": "success",
    "pid": 12345,
    "queue_id": 1234567890,
    "run_time": 0.123,
    "queue_time": 0.0,
    "total_time": 0.123,
    "queue_length": 0,
    "build_number": "1.0.0"
}
```

### Respuestas de Error

- **Parámetros Faltantes o Inválidos**  
  **Código:** 400 Bad Request

  ```json
  {
      "error": "Missing or invalid parameters",
      "stdout": "",
      "exit_code": 400
  }
  ```

- **Error de Ejecución**  
  **Código:** 400 Bad Request

  ```json
  {
      "error": "Error message from the executed code",
      "stdout": "Output from the executed code",
      "exit_code": 400
  }
  ```

- **Tiempo de Ejecución Excedido**  
  **Código:** 408 Request Timeout

  ```json
  {
      "error": "Execution timed out after 10 seconds"
  }
  ```

- **Error Interno del Servidor**  
  **Código:** 500 Internal Server Error

  ```json
  {
      "error": "An internal server error occurred",
      "stdout": "",
      "stderr": "",
      "exit_code": 500
  }
  ```

## 5. Manejo de Errores

El endpoint gestiona distintos tipos de errores:

- 🚫 Parámetros faltantes o inválidos (400)  
- ⚠️ Errores de ejecución, como sintaxis incorrecta o excepciones (400)  
- ⏰ Tiempo de ejecución excedido (408)  
- 🔥 Errores internos del servidor (500)

Además, `app.py` contempla el manejo de sobrecarga en la cola (429 Too Many Requests).

## 6. Notas de Uso

- 🔒 El código se ejecuta en un entorno aislado (sandbox) con acceso limitado a recursos.  
- ⏱️ La ejecución está limitada a un máximo de 300 segundos por defecto, ajustable con el parámetro `timeout`.  
- 📥 Se capturan y retornan la salida estándar (stdout), la salida de error (stderr) y el código de salida.  
- 🔗 Si se proporciona una `webhook_url`, el resultado también se envía a esa URL.

## 7. Problemas Comunes

- 🚫 Intentar ejecutar código que acceda a recursos restringidos o realice operaciones prohibidas puede generar errores de ejecución.  
- ⏳ Código muy largo o intensivo en recursos puede provocar el tiempo de espera.  
- 🔍 Una `webhook_url` inválida impedirá la entrega del resultado.

## 8. Buenas Prácticas

- 🛡️ Valida y sanitiza siempre la entrada para evitar ataques de inyección de código.  
- ⏲️ Ajusta el valor de `timeout` según el tiempo estimado de ejecución.  
- 📈 Monitorea los logs para detectar errores o comportamientos inesperados.  
- 🚀 Implementa medidas de seguridad adicionales (sandbox, listas blancas/negra, etc.).  
- ⚖️ Considera la gestión de la tasa de solicitudes o la administración de la cola para prevenir sobrecargas.