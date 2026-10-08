#!/bin/bash
# Sensible vars read from macOS Keychain — never touch disk
export OPENAI_API_KEY=$(security find-generic-password -a openai -s freelingo -w 2>/dev/null)
export POSTGRES_PASSWORD=$(security find-generic-password -a postgres -s freelingo -w 2>/dev/null)
export REDIS_PASSWORD=$(security find-generic-password -a redis -s freelingo -w 2>/dev/null)
export SECRET_KEY=$(security find-generic-password -a secretkey -s freelingo -w 2>/dev/null)

missing=false
for var in OPENAI_API_KEY POSTGRES_PASSWORD REDIS_PASSWORD SECRET_KEY; do
  eval "val=\$$var"
  if [ -z "$val" ]; then
    echo "MISSING: $var not found in Keychain."
    missing=true
  fi
done

if [ "$missing" = true ]; then
  echo ""
  echo "Save them first:"
  echo "  security add-generic-password -a openai    -s freelingo -w \"sk-tu-key\""
  echo "  security add-generic-password -a postgres  -s freelingo -w \"devpass\""
  echo "  security add-generic-password -a redis     -s freelingo -w \"devpass\""
  echo "  security add-generic-password -a secretkey -s freelingo -w \"\$(openssl rand -hex 32)\""
  exit 1
fi

# Rebuild images and refresh anonymous dependency volumes from the new images.
# Persistent application data uses bind mounts under DATA_PATH.
docker compose -f docker-compose.dev.yml --env-file .env.dev up -d --build --force-recreate --renew-anon-volumes
