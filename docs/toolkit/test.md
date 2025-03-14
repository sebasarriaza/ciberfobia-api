# Endpoint de Prueba de Ciberfobia-api

## 1. Visión General

El endpoint `/v1/toolkit/test` es parte de la API de Ciberfobia-api y está diseñado para comprobar la configuración de la API.  
Realiza las siguientes operaciones:
- Crea un archivo temporal.
- Sube el archivo a almacenamiento en la nube.
- Retorna la URL del archivo subido.

Este endpoint sirve como prueba básica para verificar que la API esté correctamente configurada y pueda realizar operaciones de archivos y de almacenamiento en la nube. 🚀

## 2. Endpoint

- **Ruta URL:** `/v1/toolkit/test`  
- **Método HTTP:** `GET`

## 3. Solicitud

### Encabezados

- **`x-api-key`** (requerido): Clave API para autenticación. 🔑

### Parámetros en el Cuerpo

- Este endpoint **no requiere** parámetros en el cuerpo de la solicitud.

### Ejemplo de Solicitud

```bash
curl -X GET \
  https://tu-api-url.com/v1/toolkit/test \
  -H 'x-api-key: tu-api-key'
```

## 4. Respuesta

### Respuesta Exitosa

```json
{
  "endpoint": "/v1/toolkit/test",
  "code": 200,
  "id": null,
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "response": "https://almacenamiento-cloud.com/exito.txt",
  "message": "success",
  "pid": 12345,
  "queue_id": 67890,
  "run_time": 0.123,
  "queue_time": 0.0,
  "total_time": 0.123,
  "queue_length": 0,
  "build_number": "1.0.0"
}
```

### Respuestas de Error

- **401 Unauthorized**  
  Si la API key es inválida o está ausente, se retorna:

```json
{
  "code": 401,
  "message": "Unauthorized: API key inválida o ausente"
}
```

- **500 Internal Server Error**  
  Si ocurre un error durante la creación o subida del archivo:

```json
{
  "code": 500,
  "message": "Ocurrió un error durante el procesamiento de la solicitud"
}
```

## 5. Manejo de Errores

- **Clave API inválida o faltante (401 Unauthorized):**  
  Si no se incluye una API key válida, se retorna un error 401. 🚫

- **Error Interno (500 Internal Server Error):**  
  Si ocurre un error inesperado durante la creación o subida del archivo, se retorna un error 500 con un mensaje descriptivo. 🔥

## 6. Notas de Uso

- Este endpoint se utiliza principalmente para pruebas y para verificar que la API esté funcionando correctamente.
- No requiere parámetros en el cuerpo, lo que simplifica su uso durante la integración inicial. ✅

## 7. Problemas Comunes

- **Clave API incorrecta o faltante:**  
  Asegúrate de incluir el encabezado `x-api-key` con una API key válida.
- **Problemas en la creación o subida del archivo:**  
  Si hay inconvenientes al generar o subir el archivo temporal, se retornará un error 500.

## 8. Buenas Prácticas

- Utiliza este endpoint durante la configuración inicial para confirmar que la API está operativa.
- Realiza pruebas periódicas para detectar posibles cambios o problemas en la configuración.
- Registra y monitorea los resultados del endpoint para facilitar la detección y resolución de incidencias. 📊