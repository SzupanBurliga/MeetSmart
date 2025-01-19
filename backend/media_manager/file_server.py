from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi

# Save the uploaded file in the current directory
UPLOAD_FOLDER = './uploads/'  # Set the current directory
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
        if self.path == '/upload':
            # Parse the form data posted
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

                # Log the file name to the console
                print(f"File received and saved: {video_filename}")

                # Respond with success and include CORS headers
                self.send_response(200)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b'File uploaded successfully')
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

if __name__ == '__main__':
    run()
