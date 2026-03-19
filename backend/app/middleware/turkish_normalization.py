"""
Turkish Character Normalization Middleware
VUC-2026 Ultimate Dev++ Standards
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.turkish_normalizer import apply_turkish_standards
import json
import logging

class TurkishNormalizationMiddleware(BaseHTTPMiddleware):
    """Türkçe karakter normalizasyon middleware'i"""
    
    async def dispatch(self, request: Request, call_next):
        # Process request
        response = await call_next(request)
        
        # Only process JSON responses
        if response.headers.get("content-type", "").startswith("application/json"):
            try:
                # Get response body
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                
                # Parse and normalize JSON
                if body:
                    data = json.loads(body.decode())
                    normalized_data = apply_turkish_standards(data)
                    
                    # Return normalized response
                    return JSONResponse(
                        content=normalized_data,
                        status_code=response.status_code,
                        headers=dict(response.headers)
                    )
                    
            except Exception as e:
                logging.error(f"Turkish normalization error: {e}")
                # Return original response if normalization fails
                pass
        
        return response
