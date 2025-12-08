#!/usr/bin/env bash
# Prepare local environment: install dependencies, refresh dataset and optionally run docker.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

log_info() {
  printf '[INFO] %s\n' "$1"
}

if ! command -v poetry >/dev/null 2>&1; then
  printf '[ERROR] Poetry no está instalado. Visita https://python-poetry.org/docs/#installation\n' >&2
  exit 1
fi

log_info "Instalando dependencias con Poetry"
poetry install --no-root

log_info "Regenerando dataset de riesgo"
poetry run python scripts/generate_wallet_dataset.py

if [[ "${1:-}" == "--docker" ]]; then
  if ! command -v docker >/dev/null 2>&1; then
    printf '[ERROR] Docker no está disponible en el sistema.\n' >&2
    exit 1
  fi
  if ! docker compose version >/dev/null 2>&1; then
    printf '[ERROR] docker compose no está disponible.\n' >&2
    exit 1
  fi
  log_info "Levantando stack docker (Ctrl+C para detener)"
  docker compose up --build
fi

log_info "Setup completado."
