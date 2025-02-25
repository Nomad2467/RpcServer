# server.py
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from docx2pdf import convert
import os
import base64

# Restrict to a particular path for security reasons.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    def convert_docx_to_pdf(docx_content_base64, docx_filename):
        try:
            # Convert the content from base64 to bytes
            docx_content = base64.b64decode(docx_content_base64)

            # Construct the absolute path to save the DOCX file
            docx_path = os.path.join(os.getcwd(), docx_filename)

            # Save the DOCX content to the file
            with open(docx_path, 'wb') as docx_file:
                docx_file.write(docx_content)

            try:
                # Convert the saved DOCX file to PDF
                pdf_path = convert(docx_path)

                # Read the PDF content
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()

                return pdf_content

            finally:
                # Clean up temporary files
                os.remove(docx_path)
                os.remove(pdf_path)

        except Exception as e:
            print("Error in convert_docx_to_pdf:", e)
            raise

    server.register_function(convert_docx_to_pdf, 'convert_docx_to_pdf')

    # Run the server's main loop
    print("Server is listening on port 8000...")
    server.serve_forever()