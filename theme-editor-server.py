#!/usr/bin/env python3
"""Servidor local del editor de colores de Claudy Theme.

Sirve theme-editor.html y, en POST /save, reescribe themes/claudy-dark.json
aplicando el mapeo de colores recibido sobre una copia pristina del tema.
Idempotente: cada guardado parte siempre de la base original.

Uso:  python3 theme-editor-server.py   ->   http://localhost:7333/theme-editor.html
"""
import glob
import http.server
import json
import os
import re
import shutil
import socketserver

PORT = 7333
ROOT = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.join(ROOT, "themes", "claudy-dark.json")
BASE = os.path.join(ROOT, "themes", ".claudy-dark.base.json")

# Snapshot pristino la primera vez.
if not os.path.exists(BASE):
    shutil.copy(THEME, BASE)


def theme_targets():
    """Archivos de tema a reescribir: el del repo y el instalado en VSCode."""
    targets = [THEME]
    pattern = os.path.expanduser(
        "~/.vscode/extensions/*claudy-dark*/themes/claudy-dark.json")
    targets.extend(glob.glob(pattern))
    return targets


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_POST(self):
        if self.path != "/save":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            mapping = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self.send_error(400)
            return
        # normalizar a minuscula
        mapping = {k.lower(): v.lower() for k, v in mapping.items()}
        text = open(BASE, encoding="utf-8").read()
        if mapping:
            pattern = "(" + "|".join(re.escape(k) for k in mapping) + ")"
            text = re.sub(
                pattern,
                lambda m: mapping[m.group(0).lower()],
                text,
                flags=re.IGNORECASE,
            )
        written = 0
        for target in theme_targets():
            try:
                with open(target, "w", encoding="utf-8") as f:
                    f.write(text)
                written += 1
            except OSError:
                pass
        body = ('{"ok":true,"written":%d}' % written).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # silencioso


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as srv:
        print(f"Claudy theme editor -> http://localhost:{PORT}/theme-editor.html")
        srv.serve_forever()
