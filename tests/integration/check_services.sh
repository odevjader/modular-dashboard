#!/bin/bash
# set -e # Exit immediately if a command exits with a non-zero status. Let's report all failures.

RED=\$'\033[0;31m'
GREEN=\$'\033[0;32m'
NC=\$'\033[0m' # No Color

FAILED_TESTS=0

echo_pass() {
    echo -e "${GREEN}PASS: $1${NC}"
}

echo_fail() {
    echo -e "${RED}FAIL: $1${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
}

echo "--- Checking Docker Compose services ---"
if ! docker-compose ps | grep "Up\|running"; then # Check for "Up" or "running"
    echo_fail "Not all services are up or running!"
    docker-compose ps
else
    echo_pass "All services appear to be running."
    docker-compose ps
fi
echo ""

echo "--- Checking API (backend) Health (http://localhost:8000/api/healthcheck) ---"
API_HEALTH_STATUS=$(docker-compose exec -T api curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/healthcheck || echo "Error")
if [ "$API_HEALTH_STATUS" -eq 200 ]; then
    echo_pass "API healthcheck successful (HTTP 200)."
else
    echo_fail "API healthcheck FAILED. Status code: $API_HEALTH_STATUS"
    docker-compose logs --tail=20 api
fi
echo ""

echo "--- Checking API to Redis Connectivity ---"
# Use the service name 'redis' as defined in docker-compose.yml
API_REDIS_PING=$(docker-compose exec -T api python -c "import redis; r = redis.Redis(host='redis', port=6379, db=0); print(r.ping())" || echo "Error")
if [ "$API_REDIS_PING" = "True" ]; then
    echo_pass "API to Redis connection successful."
else
    echo_fail "API to Redis connection FAILED. Output: $API_REDIS_PING"
    docker-compose logs --tail=20 api
    docker-compose logs --tail=20 redis
fi
echo ""

echo "--- Checking API to PostgreSQL DB Connectivity ---"
API_DB_CONNECT=$(docker-compose exec -T api python -c "import os, sqlalchemy; db_url = f'postgresql://{os.getenv(\"DB_USER\", \"appuser\")}:{os.getenv(\"DB_PASSWORD\", \"apppassword\")}@db:{os.getenv(\"DB_PORT\", 5432)}/{os.getenv(\"DB_NAME\", \"appdb\")}'; engine = sqlalchemy.create_engine(db_url); conn = engine.connect(); conn.close(); print('DB Connected')" || echo "Error")
if [ "$API_DB_CONNECT" = "DB Connected" ]; then
    echo_pass "API to PostgreSQL connection successful."
else
    echo_fail "API to PostgreSQL connection FAILED. Output: $API_DB_CONNECT"
    docker-compose logs --tail=20 api
    docker-compose logs --tail=20 db
fi
echo ""

echo "--- Checking API Alembic Migrations (Example: users table) ---"
# This checks if a 'users' table exists. Adjust table name as needed.
API_DB_TABLE_CHECK=$(docker-compose exec -T db psql -U appuser -d appdb -tAc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'users');" || echo "Error")
if [ "$API_DB_TABLE_CHECK" = "t" ]; then
    echo_pass "API 'users' table exists in database."
elif [ "$API_DB_TABLE_CHECK" = "f" ]; then
    echo_fail "API 'users' table does NOT exist. Migrations might not have run or are incomplete."
else
    echo_fail "Could not check for API 'users' table. psql output: $API_DB_TABLE_CHECK"
fi
echo ""

echo "--- Checking transcritor_pdf_worker to Redis Connectivity ---"
WORKER_REDIS_PING=$(docker-compose exec -T transcritor_pdf_worker python -c "from celery import Celery; import os; app = Celery(broker=os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')); conn = app.broker_connection(); conn.ensure_connection(max_retries=1); conn.close(); print('Worker connected to broker')" || echo "Error")
if [ "$WORKER_REDIS_PING" = "Worker connected to broker" ]; then
    echo_pass "transcritor_pdf_worker to Redis connection successful."
else
    echo_fail "transcritor_pdf_worker to Redis connection FAILED. Output: $WORKER_REDIS_PING"
    docker-compose logs --tail=20 transcritor_pdf_worker
    docker-compose logs --tail=20 redis
fi
echo ""

echo "--- Checking transcritor_pdf_worker to PostgreSQL DB Connectivity (if applicable) ---"
# This assumes the worker might need DB access and uses env vars DB_USER_TRANSCRITOR, DB_PASSWORD_TRANSCRITOR, DB_NAME_TRANSCRITOR, DB_HOST_TRANSCRITOR, DB_PORT_TRANSCRITOR
# If these are not set, it will try the api's db credentials as a fallback.
WORKER_DB_USER=\${DB_USER_TRANSCRITOR:-appuser}
WORKER_DB_PASSWORD=\${DB_PASSWORD_TRANSCRITOR:-apppassword}
WORKER_DB_NAME=\${DB_NAME_TRANSCRITOR:-appdb} # Assuming it might use the same DB or a different one
WORKER_DB_HOST=\${DB_HOST_TRANSCRITOR:-db}

# Note: The following command will be executed inside the transcritor_pdf_worker container.
# It needs access to these environment variables or the defaults will be used.
WORKER_DB_CONNECT_COMMAND="import os, sqlalchemy; db_url = f'postgresql://{os.getenv(\"DB_USER_TRANSCRITOR\", \"appuser\")}:{os.getenv(\"DB_PASSWORD_TRANSCRITOR\", \"apppassword\")}@{os.getenv(\"DB_HOST_TRANSCRITOR\", \"db\")}:{os.getenv(\"DB_PORT_TRANSCRITOR\", 5432)}/{os.getenv(\"DB_NAME_TRANSCRITOR\", \"appdb\")}'; engine = sqlalchemy.create_engine(db_url); conn = engine.connect(); conn.close(); print('DB Connected')"

WORKER_DB_CONNECT=$(docker-compose exec -T transcritor_pdf_worker python -c "$WORKER_DB_CONNECT_COMMAND" || echo "Error")
if [ "$WORKER_DB_CONNECT" = "DB Connected" ]; then
    echo_pass "transcritor_pdf_worker to PostgreSQL connection successful."
else
    echo_fail "transcritor_pdf_worker to PostgreSQL connection FAILED. Output: $WORKER_DB_CONNECT"
    echo "Note: This test assumes the worker needs direct DB access. Check worker's .env if this fails."
    docker-compose logs --tail=20 transcritor_pdf_worker
fi
echo ""

echo "--- Running Celery Integration Test (transcritor_pdf_worker) ---"
# This script needs to be executable and have python3 in its path
# It will be run from the host, connecting to Redis as configured by env vars.
# Ensure the test script is executable: chmod +x tests/integration/test_celery_transcritor.py
# Ensure python3 and celery client are installed in the environment running this script,
# or run it inside a container that has these (e.g., the api container if it has celery client).

# For simplicity, running from host. This might require `pip install celery redis` on the host.
if python3 tests/integration/test_celery_transcritor.py; then
    echo_pass "Celery integration test for transcritor_pdf_worker PASSED."
else
    echo_fail "Celery integration test for transcritor_pdf_worker FAILED."
    # Potentially show worker logs if celery test fails
    docker-compose logs --tail=50 transcritor_pdf_worker
fi
echo ""

echo "--- Frontend Connectivity (Basic Check) ---"
# This is a very basic check. More comprehensive frontend tests are separate.
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 || echo "Error") # Assuming default Vite port
if [ "$FRONTEND_STATUS" -eq 200 ] || [ "$FRONTEND_STATUS" -eq 304 ]; then # 304 Not Modified is also OK
    echo_pass "Frontend is accessible (HTTP $FRONTEND_STATUS)."
else
    echo_fail "Frontend is NOT accessible. Status code: $FRONTEND_STATUS"
    docker-compose logs --tail=20 frontend
fi
echo ""

echo "--- Test Summary ---"
if [ "$FAILED_TESTS" -eq 0 ]; then
    echo -e "${GREEN}All Phase 1 infrastructure tests PASSED.${NC}"
    exit 0
else
    echo -e "${RED}${FAILED_TESTS} test(s) FAILED.${NC}"
    exit 1
fi
