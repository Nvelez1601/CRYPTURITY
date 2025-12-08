# Crypturity Wallet Risk API

API construida con FastAPI para verificar wallets contra un dataset consolidado de riesgo (OFAC, TRM Labs y Chainabuse). Ideal para escenarios de compliance AML/KYC o monitores de fraude.

## Características principales
- Verificación rápida de wallets con diagnóstico de riesgo numérico y categórico.
- Arquitectura modular por componentes (controllers, repositories, services, use cases, routes).
- Dataset JSON versionado bajo `app/repositories/data/` con script para regenerarlo.
- Middleware de logging (nivel INFO) y configuración via `.env`.
- Distribución lista para contenedores (Dockerfile y docker-compose).

## Estructura del proyecto
```
app/
  bases/                # Clases base reutilizables (p.ej. repositorios)
  components/
    wallet_checker/     # Componente principal del verificador
      routes/
      services/
      usecases/
        dto/
  config/               # Settings, logging y helpers
  controllers/          # Controladores para formatear respuestas API
  middlewares/          # Middlewares transversales
  repositories/
    data/               # Dataset JSON (wallet_risk_dataset.json)
    wallet_repository.py
scripts/
  generate_wallet_dataset.py  # Reconstruye el dataset desde Data2.txt
  test_wallet_flow.py         # Prueba de flujo con wallets de muestra
docker/
  Dockerfile
  docker-compose.yml
README.md
.env / .env.example
pyproject.toml
```

## Dataset
- Fuente original: `Data2.txt` en la raíz del repositorio.
- Dataset normalizado: `app/repositories/data/wallet_risk_dataset.json`.
- Regeneración: `poetry run python scripts/generate_wallet_dataset.py` (o usando la venv manual).

## Requisitos
- Python 3.12+
- Poetry 1.8+
- Docker 24+ (opcional para despliegue contenedorizado)

### Instalación de dependencias (Poetry)
```bash
poetry install
```

### Ejecución local (Poetry)
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Uso con venv manual (WSL)
```bash
python -m venv venv
source venv/bin/activate
pip install poetry
poetry install
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker
### Build & run
```bash
docker compose -f docker/docker-compose.yml up --build
```
La API queda disponible en `http://localhost:8000`.

### Variables de entorno
Configura `.env` (o provee variables en el hosting) con al menos:
```
APP_NAME="Crypturity Wallet Risk API"
API_PREFIX="/api/v1"
DATASET_PATH="app/repositories/data/wallet_risk_dataset.json"
LOG_LEVEL="INFO"
```

## API
- `POST /api/v1/wallets/verify`
  - Payload: `{ "address": "<wallet>" }`
  - Respuesta: estructura `status/message/data` con el resumen del riesgo.
- `GET /api/v1/wallets/metadata`
  - Devuelve metadata del dataset cargado.

Ejemplo (curl):
```bash
curl -X POST http://localhost:8000/api/v1/wallets/verify \
  -H "Content-Type: application/json" \
  -d '{"address":"0x47ce0c6ac56edb84e2ad330bec0b500ad6e71bee"}'
```

## Scripts útiles
- `python scripts/generate_wallet_dataset.py`: actualiza el dataset normalizado.
- `python scripts/test_wallet_flow.py`: imprime diagnóstico para wallets de ejemplo (2 maliciosas, 2 benignas).

## Testing
```bash
poetry run pytest
```

## Despliegue (Render u otro hosting)
1. Construye la imagen con el Dockerfile incluido.
2. Define las variables de entorno del `.env` en el servicio de hosting.
3. Expón el puerto `8000`.
4. Opcional: monta un volumen sobre `app/repositories/data` para actualizar el dataset sin reconstruir.

## Próximos pasos sugeridos
- Añadir almacenamiento persistente (DB) en lugar de JSON.
- Implementar autenticación/ratelimiting.
- Añadir pruebas unitarias y de integración más completas.
