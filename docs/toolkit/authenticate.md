# Endpoint de Autenticación

## 1. Visión General

El endpoint `/v1/toolkit/authenticate` forma parte del blueprint `v1_toolkit_auth` dentro de la estructura de la API.  
Su función es autenticar las solicitudes verificando la API key proporcionada contra un valor predefinido, actuando como guardián para asegurar que solo los clientes autorizados accedan a los recursos de la API. 🔐

## 2. Endpoint

- **Ruta URL:** `/v1/toolkit/authenticate`
- **Método HTTP:** `GET`

## 3. Solicitud

### Encabezados

- **`X-API-Key`** (requerido): Clave API para autenticación. 🔑

### Parámetros en el Cuerpo

Este endpoint no requiere parámetros en el cuerpo de la solicitud.

### Ejemplo de Solicitud

```bash
curl -X GET -H "X-API-Key: TU_API_KEY" http://localhost:8080/v1/toolkit/authenticate
```

## 4. Respuesta

### Respuesta Exitosa

Si la API key proporcionada coincide con el valor predefinido, se retornará un código 200 OK con la siguiente respuesta:

```json
{
  "code": 200,
  "endpoint": "/authenticate",
  "id": null,
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "message": "success",
  "pid": 12345,
  "queue_id": 1234567890,
  "queue_length": 0,
  "response": "Authorized",
  "run_time": 0.001,
  "total_time": 0.001,
  "queue_time": 0,
  "build_number": "1.0.0"
}
```

### Respuesta de Error

Si la API key es inválida o está ausente, se retornará un código 401 Unauthorized con la siguiente respuesta:

```json
{
  "code": 401,
  "endpoint": "/authenticate",
  "id": null,
  "job_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "message": "Unauthorized",
  "pid": 12345,
  "queue_id": 1234567890,
  "queue_length": 0,
  "response": null,
  "run_time": 0.001,
  "total_time": 0.001,
  "queue_time": 0,
  "build_number": "1.0.0"
}
```

## 5. Manejo de Errores

- Si la API key es inválida o falta, el endpoint retornará un error 401 Unauthorized con un mensaje descriptivo. 🚫

## 6. Notas de Uso

- Este endpoint se utiliza como puerta de entrada para la API, garantizando que solo los clientes autorizados puedan acceder a sus recursos.
- La API key debe mantenerse segura y no compartirse con terceros no autorizados. 🔒

## 7. Problemas Comunes

- Olvidar incluir el encabezado `X-API-Key` en la solicitud.
- Utilizar una API key inválida o caducada.

## 8. Buenas Prácticas

- Rotar las API keys periódicamente para mejorar la seguridad. 🔄
- Almacenar las API keys de forma segura y evitar incluirlas en sistemas de control de versiones. 📁
- Considerar la implementación de medidas de seguridad adicionales, como limitación de tasa o listas blancas de IP, para proteger aún más la API. 🛡️