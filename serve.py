# 폰에서 카메라 테스트용 https 서버 (카메라는 https 에서만 열림).
# 실행: python3 serve.py  → 같은 와이파이의 폰에서 화면에 뜨는 주소로 접속. 인증서 경고는 "계속/방문"으로 넘기면 됨.
import http.server, os, socket, ssl, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists('cert.pem'):
    subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', 'cert.pem', '-out', 'cert.pem',
                    '-days', '365', '-subj', '/CN=ai-persona'], check=True, capture_output=True)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); ip = s.getsockname()[0]; s.close()
srv = http.server.HTTPServer(('0.0.0.0', 8443), http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER); ctx.load_cert_chain('cert.pem')
srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
print(f'폰에서 접속:  https://{ip}:8443   (끝내려면 Ctrl+C)', flush=True)
srv.serve_forever()
