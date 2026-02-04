set -e

CAMOUFOX_CACHE="/root/.cache/camoufox"
VERSION_FILE="$CAMOUFOX_CACHE/version.json"

echo "Checking Camoufox cache..."

if [ ! -f "$VERSION_FILE" ]; then
  echo "Camoufox cache not found, fetching..."
  camoufox fetch
else
  echo "Camoufox cache found, skipping fetch"
fi

echo "Starting application..."
exec "$@"
