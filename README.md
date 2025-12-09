# Crypturity Wallet Risk API

API construida con FastAPI para verificar wallets contra un dataset consolidado de riesgo (OFAC, TRM Labs y Chainabuse). Ideal para escenarios de compliance AML/KYC o monitores de fraude.

## Características principales
- Verificación rápida de wallets con diagnóstico de riesgo numérico y categórico.
- Arquitectura modular por componentes (controllers, repositories, services, use cases, routes).
- Dataset JSON versionado bajo `app/repositories/data/` con script para regenerarlo.
- Middleware de logging (nivel INFO) y configuración via `.env`.
- Dashboard web responsivo en Vue 3 (Vite) con estética tipo Binance (negro/amarillo).
- Distribución lista para contenedores (docker/api.Dockerfile, docker/frontend.Dockerfile y docker-compose).

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
  api.Dockerfile
  frontend.Dockerfile
frontend/
  package.json
  tsconfig.json
  vite.config.ts
  src/
    components/
    services/
    store/
    views/
render.yaml
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

## Frontend (Vue 3 + Vite)
```bash
cd frontend
npm install
npm run dev
```
El dashboard queda disponible en `http://localhost:5173` y consume la API vía las variables `VITE_API_BASE_URL` y `VITE_API_PREFIX`.

## Docker
### Build & run
```bash
docker compose up --build
```
La API queda disponible en `http://localhost:8000` y el dashboard en `http://localhost:5173`.

### Variables de entorno
Configura `.env` (o provee variables en el hosting) con al menos:
```
APP_NAME="Crypturity Wallet Risk API"
API_PREFIX="/api/v1"
DATASET_PATH="app/repositories/data/wallet_risk_dataset.json"
LOG_LEVEL="INFO"
VITE_API_BASE_URL="http://localhost:8000"
VITE_API_PREFIX="/api/v1"
```

## Despliegue en Render (free tier)
Puedes reutilizar el blueprint incluido en `render.yaml` para aprovisionar dos servicios:

1. **API (FastAPI)** → Servicio web Docker.
  - Usa `docker/api.Dockerfile` como imagen.
  - Render expone la API en `https://crypturity-api.onrender.com` (ajusta el nombre si se encuentra ocupado).
2. **Frontend (Vue/Vite)** → Sitio estático.
  - Construye desde `frontend/` con `npm install && npm run build` y publica la carpeta `dist`.
  - Configura las variables `VITE_API_BASE_URL` y `VITE_API_PREFIX` apuntando a la URL pública de la API.

Pasos rápidos:
```bash
render blueprint deploy render.yaml
```
O bien crea los servicios manualmente desde el panel de Render importando el repositorio y aplicando las variables anteriores.

**Notas**
- El plan gratuito “duerme” tras unos minutos sin tráfico (primer request tarda unos segundos).
- Si cambias el nombre del servicio backend, actualiza `VITE_API_BASE_URL` en Render y/o en `render.yaml`.
- El frontend también intentará usar `window.location.origin` si no encuentra `VITE_API_BASE_URL`, lo que permite servir ambos desde el mismo dominio en otros proveedores.

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
