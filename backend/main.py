from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
import media_manager.extract_frames as extract_frames
import media_manager.extract_audio as extract_audio
import ocr
import email_service
import llm_calling
# Global variable to store the submitted email
submitted_email = None

# Save the uploaded file in the specified folder
UPLOAD_FOLDER = './uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        """Sets CORS headers to allow cross-origin requests."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        """Handle preflight requests."""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path == '/submit-email':
            # Handle email submission
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                global submitted_email
                submitted_email = post_data.decode('utf-8')  # Save the email
                print(f"Email received: {submitted_email}")
                self.send_response(200)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b'Email received successfully')
            except Exception as e:
                self.send_response(500)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(f'Error processing email: {str(e)}'.encode('utf-8'))

        elif self.path == '/upload':
            # Handle file upload
            content_type, pdict = cgi.parse_header(self.headers['content-type'])
            if content_type != 'multipart/form-data':
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid content type')
                return

            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = int(self.headers['content-length'])
            fields = cgi.parse_multipart(self.rfile, pdict)

            # Get the video file
            if 'video' not in fields:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No video file provided')
                return

            video_data = fields['video'][0]
            video_filename = 'recording.webm'  # Use .webm as the extension
            video_path = os.path.join(UPLOAD_FOLDER, video_filename)

            # Save the file
            try:
                with open(video_path, 'wb') as f:
                    f.write(video_data)

                # Log the file name and the associated email
                print(f"File received and saved: {video_filename}")
                print(f"Associated email: {submitted_email if submitted_email else 'No email submitted'}")

                # Respond with success and include CORS headers
                self.send_response(200)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b'File uploaded successfully')

                handle_video_processing()

            except Exception as e:
                self.send_response(500)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(f'Error saving the file: {str(e)}'.encode('utf-8'))
        else:
            self.send_response(404)
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(b'Endpoint not found')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}...')
    httpd.serve_forever()


def handle_video_processing():
    print("Extracting frames...")
    extract_frames.get_frames('./uploads/recording.webm', 'outputs/unique_frames')  # Pass video path to the function

    print("Extracting audio...")
    extract_audio.get_audio('./uploads/recording.webm', './outputs/output_audio.mp3')  

    # print("Sending email...")
    # email_service.send_email(submitted_email, '../OCR/result.md')
    #  narazie nie działa bo import trzeba naprawić
    
if __name__ == '__main__':
    run()
