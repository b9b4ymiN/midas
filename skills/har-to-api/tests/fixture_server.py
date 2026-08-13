# Local fixture server mimicking a SvelteKit __data.json route + an auth-gated route.
import json, http.server, socketserver, threading
SVELTE = {"type":"data","nodes":[
  {"type":"data","data":{"theme":"light"}},
  {"type":"data","data":{"s":"TU","n":"Thai Union Group PCL","e":"BKK"}},
  {"type":"data","data":{
     "asOf":"2026-03-31","currency":"THB",
     "revenueTotal":[134984000000,132719000000,138433000000],
     "netIncomeCommon":[4703000000,4609000000,4985000000],
     "operatingMargin":[4.71,4.59,5.18]}}]}
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def do_GET(self):
        if self.path.startswith("/quote/bkk/TU/financials/__data.json"):
            if "x-sveltekit-trailing-slash=1" not in self.path:
                # exactly what the real framework does: serves the HTML page
                self.send_response(200); self.send_header("Content-Type","text/html"); self.end_headers()
                self.wfile.write(b"<!DOCTYPE html><html><head><title>TU</title>"); return
            b=json.dumps(SVELTE).encode()
            self.send_response(200); self.send_header("Content-Type","application/json")
            self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b); return
        if self.path.startswith("/gated"):
            self.send_response(401); self.end_headers(); self.wfile.write(b'{"error":"unauthorized"}'); return
        self.send_response(404); self.end_headers(); self.wfile.write(b'{}')
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.TCPServer(("127.0.0.1",8899),H)
threading.Thread(target=srv.serve_forever,daemon=True).start()
print("fixture server on :8899")
import time; time.sleep(3600)  # keep alive for the test run
