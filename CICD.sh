#!/bin/bash
set -e   # Stop immediately if a step fails

# ─────────────────────────────────────────
#  VARIABLES
# ─────────────────────────────────────────
APP_NAME="flask-mysql-app"
VERSION=$(git rev-parse --short HEAD 2>/dev/null || echo "local")
IMAGE="$APP_NAME:$VERSION"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   Pipeline DevSecOps — $IMAGE"
echo "╚══════════════════════════════════════╝"

# ─────────────────────────────────────────
#  ÉTAPE 1 — LINT
#  Validate Dockerfile best practices
# ─────────────────────────────────────────
echo ""
echo "▶ [1/5] Lint du Dockerfile (hadolint)..."
hadolint Dockerfile
echo "  ✅ Dockerfile valide"

# ─────────────────────────────────────────
#  ÉTAPE 2 — SECRET SCAN
#  Search for passwords / tokens in code
# ─────────────────────────────────────────
echo ""
echo "▶ [2/5] Scan de secrets (gitleaks)..."
gitleaks detect --source . --no-git --redact
echo "  ✅ Aucun secret détecté"

# ─────────────────────────────────────────
#  ÉTAPE 3 — BUILD
#  Build Docker image
# ─────────────────────────────────────────
echo ""
echo "▶ [3/5] Build de l'image Docker..."
docker build -t "$IMAGE" .
echo "  ✅ Image construite : $IMAGE"

# ─────────────────────────────────────────
#  ÉTAPE 4 — SCAN CVE
#  Search for known vulnerabilities in image
#  --exit-code 1 = BLOCKS pipeline if CRITICAL CVE found
# ─────────────────────────────────────────
echo ""
echo "▶ [4/5] Scan CVE (trivy)..."
trivy image \
  --exit-code 1 \
  --severity CRITICAL \
  --no-progress \
  "$IMAGE"
echo "  ✅ Aucune vulnérabilité critique"

# ─────────────────────────────────────────
#  ÉTAPE 5 — DEPLOY + HEALTH CHECK
#  Launch containers with docker-compose
# ─────────────────────────────────────────
echo ""
echo "▶ [5/5] Déploiement..."

# Kill any process on ports 3306 and 9002
for port in 3306 9002; do
  fuser -k $port/tcp 2>/dev/null || true
done
sleep 1

# Aggressive container cleanup
docker kill $(docker ps -q) 2>/dev/null || true
docker system prune -f --volumes 2>/dev/null || true
sleep 2

# Build and start services
docker compose up -d

echo "  En attente du démarrage (8s)..."
sleep 8

# Verify app is responding
if curl -sf http://localhost:9002/api/health > /dev/null; then
  echo "  ✅ Application en ligne !"
else
  echo "  ❌ L'application ne répond pas — rollback"
  docker compose down
  exit 1
fi

# ─────────────────────────────────────────
#  RÉSUMÉ FINAL
# ─────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════╗"
echo "║   ✅ Pipeline réussi !               ║"
echo "║   Image   : $IMAGE"
echo "║   URL     : http://localhost:9002    ║"
echo "║   Logs    : docker-compose logs      ║"
echo "╚══════════════════════════════════════╝"
