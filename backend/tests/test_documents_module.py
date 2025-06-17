from fastapi.testclient import TestClient
from app.main import app # Import the main FastAPI application

client = TestClient(app)

def test_import_document_schemas():
    from app.modules.documents import schemas as doc_schemas
    assert hasattr(doc_schemas, 'DocumentBase')
    assert hasattr(doc_schemas, 'DocumentCreate')
    assert hasattr(doc_schemas, 'Document')
    print("Document schemas imported successfully.")

def test_import_document_v1_schemas():
    from app.modules.documents.v1 import schemas as v1_doc_schemas
    assert hasattr(v1_doc_schemas, 'PingResponse')
    print("Document v1 schemas imported successfully.")

def test_import_document_services():
    from app.modules.documents import services as doc_services
    assert hasattr(doc_services, 'example_service_function')
    print("Document services imported successfully.")

def test_documents_module_router_integration():
    response = client.get("/api/openapi.json") # The global prefix is /api
    assert response.status_code == 200
    openapi_schema = response.json()
    paths = openapi_schema.get("paths", {})

    # Check for the module's root and v1 ping endpoint
    # The module_loader uses the prefix from modules.yaml directly under /api
    assert "/api/documents/" in paths, "Document module root path not found in OpenAPI spec."
    assert "/api/documents/v1/ping" in paths, "Document module v1 ping path not found in OpenAPI spec."
    print("Documents module routes found in OpenAPI schema.")

def test_documents_v1_ping_endpoint():
    response = client.get("/api/documents/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Pong from Documents v1"}
    print("Documents v1 ping endpoint responded correctly.")

def test_documents_root_endpoint():
    response = client.get("/api/documents/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Documents Module"}
    print("Documents module root endpoint responded correctly.")
