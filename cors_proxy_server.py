#!/usr/bin/env python3
import http.server
import socketserver
import urllib.request
import urllib.parse
import json
from urllib.error import HTTPError

class CORSProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            # AWS Lambda Function URL
            lambda_url = 'https://j6yvi5zbotytcme3bldgzpsvmm0mvusb.lambda-url.us-east-1.on.aws/'
            
            # 요청 본문 읽기
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Lambda에 요청 전달
                req = urllib.request.Request(
                    lambda_url,
                    data=post_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req) as response:
                    response_data = response.read()
                
                # CORS 헤더와 함께 응답
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write(response_data)
                
            except HTTPError as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {'error': f'Lambda error: {e}'}
                self.wfile.write(json.dumps(error_response).encode())
                
        else:
            # 일반 파일 서빙
            super().do_GET()
    
    def do_OPTIONS(self):
        # CORS preflight 처리
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        # 일반 파일 서빙
        super().do_GET()

PORT = 8000
Handler = CORSProxyHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"CORS Proxy Server running at http://localhost:{PORT}/")
    print("웹앱: http://localhost:8000/ai-chat-webapp.html")
    httpd.serve_forever()
