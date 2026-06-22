#!/usr/bin/env python3
"""
Docker entry point for MOSS-TTS-Nano with optional HTTP Basic Auth.
If WEB_USER and WEB_PASSWORD environment variables are set,
all web requests (except /health) will require authentication.
If not set, the app runs without authentication (original behavior).
"""
import os
import uvicorn as _uvicorn

_original_uvicorn_run = _uvicorn.run


def _patched_run(app, **kwargs):
    """Patched uvicorn.run that adds auth middleware if credentials are configured."""
    web_user = os.getenv("WEB_USER", "")
    web_password = os.getenv("WEB_PASSWORD", "")

    if web_user and web_password:
        import base64
        import secrets
        from starlette.middleware.base import BaseHTTPMiddleware
        from starlette.responses import Response as StarletteResponse

        class BasicAuthMiddleware(BaseHTTPMiddleware):
            async def dispatch(self, request, call_next):
                # Allow health checks without auth (for container monitoring)
                if request.url.path == "/health":
                    return await call_next(request)

                auth_header = request.headers.get("authorization", "")
                if auth_header:
                    try:
                        scheme, credentials = auth_header.split(" ", 1)
                        if scheme.lower() == "basic":
                            decoded = base64.b64decode(credentials).decode("utf-8")
                            username, _, password = decoded.partition(":")
                            if (secrets.compare_digest(username, web_user) and
                                    secrets.compare_digest(password, web_password)):
                                return await call_next(request)
                    except Exception:
                        pass

                return StarletteResponse(
                    status_code=401,
                    headers={"WWW-Authenticate": 'Basic realm="MOSS-TTS-Nano"'},
                    content="Authentication required",
                )

        app.add_middleware(BasicAuthMiddleware)
        print(f"[Docker] Web authentication enabled: user={web_user}")
    else:
        print("[Docker] No WEB_USER/WEB_PASSWORD set, running without authentication")

    _original_uvicorn_run(app, **kwargs)


_uvicorn.run = _patched_run

# Run the original app (app_onnx.py main)
from app_onnx import main
main()
