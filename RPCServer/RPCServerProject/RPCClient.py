from xmlrpc.client import ServerProxy
import base64
import os

def send_docx_and_receive_pdf(docx_filename):
    docx_path = os.path.join(os.getcwd(), docx_filename)
    print("Sending DOCX file:", docx_path)

    with open(docx_path, 'rb') as docx_file:
        docx_content = docx_file.read()

    with ServerProxy("http://localhost:8000/RPC2") as proxy:
        # Print the file path before sending to the server
        print("Client: Sending DOCX file to the server:", docx_path)

        # Convert the content to base64 before passing to the server
        docx_content_base64 = base64.b64encode(docx_content).decode('utf-8')

        # Convert the string back to bytes before receiving from the server
        pdf_content = proxy.convert_docx_to_pdf(docx_content_base64, docx_filename)

    # Save the received PDF content to a file
    output_pdf_filename = f"{os.path.splitext(docx_filename)[0]}.pdf"
    with open(output_pdf_filename, 'wb') as pdf_file:
        pdf_file.write(pdf_content)

if __name__ == "__main__":
    send_docx_and_receive_pdf("C:/Users/Nomad2467/Desktop/TestRpcServer.docx")
    # send_docx_and_receive_pdf("TestRpcServer.docx")
    # É possível utilizar o server com paths absolutos ou relativos
