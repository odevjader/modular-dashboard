# conftest.py for pdf_processor_service tests
# Can be used for shared fixtures across multiple test files.

# Example (can be uncommented and used if needed):
# import pytest
#
# @pytest.fixture(scope="session")
# def db_engine():
#     # Setup for a test database engine, if integration tests need it
#     # from sqlalchemy import create_engine
#     # return create_engine("sqlite:///:memory:") # Or a test postgresql
#     pass
#
# @pytest.fixture(scope="function")
# def db_session(db_engine):
#     # if db_engine:
#     #     connection = db_engine.connect()
#     #     transaction = connection.begin()
#     #     session = Session(bind=connection)
#     #     yield session
#     #     session.close()
#     #     transaction.rollback()
#     #     connection.close()
#     # else:
#     # yield None # Or raise an error if db_engine is mandatory
#     pass
