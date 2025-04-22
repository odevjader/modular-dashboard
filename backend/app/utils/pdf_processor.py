# # backend/app/utils/pdf_processor.py
# import os
# import tempfile
# from typing import List
# from fastapi import UploadFile
# from langchain_docling import DoclingLoader
#
# # --- IMPORT CORRIGIDO ---
# from app.core.config import logger # Import logger using absolute path from app package
# # --- FIM IMPORT CORRIGIDO ---
#
# async def processar_pdfs_upload(files: List[UploadFile]) -> str:
#     """
#     Processes a list of uploaded PDF files using DoclingLoader.
#     Ensures all file handles are closed.
#     """
#     combined_pdf_text = ""
#     temp_file_paths = []
#
#     logger.info(f"Starting processing for {len(files)} uploaded file(s).")
#
#     try:
#         for file in files:
#             try:
#                 if file.content_type != "application/pdf":
#                     logger.warning(f"Skipping non-PDF file: {file.filename} ({file.content_type})")
#                     continue
#
#                 temp_pdf_path = None
#                 try:
#                     # Create a temporary file
#                     # Ensure tempfile uses await if needed, check library specific reqs
#                     # Using standard tempfile which is sync I/O, might block event loop slightly
#                     # but often acceptable for temp file creation/writing compared to network I/O.
#                     # Consider threads or async file libraries if this becomes a bottleneck.
#                     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
#                         content = await file.read()
#                         if not content:
#                             logger.warning(f"Skipping empty file: {file.filename}")
#                             continue
#
#                         temp_pdf.write(content)
#                         temp_pdf_path = temp_pdf.name
#                         temp_file_paths.append(temp_pdf_path)
#                         logger.debug(f"PDF saved temporarily to {temp_pdf_path} for file {file.filename}")
#
#                     # Use DoclingLoader on the temporary file path
#                     logger.debug(f"Processing PDF with DoclingLoader: {temp_pdf_path}")
#                     # Assuming DoclingLoader.load() is synchronous I/O bound
#                     # Run potentially blocking I/O in a thread pool if it causes issues
#                     # For now, calling directly. Consider asyncio.to_thread if needed.
#                     loader = DoclingLoader(file_path=temp_pdf_path)
#                     docs = loader.load() # This might block!
#                     logger.debug(f"DoclingLoader finished. Found {len(docs)} sections for {file.filename}.")
#
#                     if docs:
#                         extracted_text = "\n\n".join([doc.page_content for doc in docs if doc.page_content])
#                         if extracted_text.strip():
#                             combined_pdf_text += f"\n\n--- CONTEÚDO DO ARQUIVO: {file.filename} ---\n\n" + extracted_text
#                             logger.debug(f"Added {len(extracted_text)} chars from {file.filename}")
#                         else:
#                             logger.warning(f"DoclingLoader extracted no text content from {file.filename}")
#                     else:
#                         logger.warning(f"DoclingLoader returned no document sections for {file.filename}")
#
#                 except Exception as load_err:
#                     logger.error(f"Error processing file {file.filename} with DoclingLoader (Path: {temp_pdf_path}): {load_err}", exc_info=True)
#                     # Continue to next file after logging error
#
#             finally:
#                 # Ensure UploadFile is closed after processing attempt or skip
#                 if file:
#                     await file.close()
#                     logger.debug(f"Closed UploadFile handle for: {file.filename}")
#
#         if combined_pdf_text.strip():
#               logger.info(f"Texto completo extraído de {len(files)} arquivo(s) processados.")
#               # logger.debug(f"Full text extracted:\n{combined_pdf_text}") # Optional full log
#         else:
#               logger.warning("Nenhum texto foi extraído dos arquivos PDF fornecidos.")
#
#         return combined_pdf_text.strip()
#
#     finally:
#         # Clean up all temporary files created
#         logger.debug(f"Cleaning up {len(temp_file_paths)} temporary file(s)...")
#         for path in temp_file_paths:
#             if path and os.path.exists(path):
#                 try:
#                     os.remove(path)
#                     logger.debug(f"Deleted temporary file: {path}")
#                 except Exception as e_del:
#                     logger.error(f"Error deleting temporary file {path}: {e_del}")