# -*- coding: utf-8 -*-
"""
Configuration Management
รับผิดชอบการจัดการ Environment Variables และ Smart Routing
"""

import os
from typing import Dict

# โหลด .env
_env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_file):
    with open(_env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

def get_best_config() -> Dict[str, str]:
    """เลือก Provider ที่พร้อมใช้งานอัตโนมัติ (OpenRouter > MiniMax)"""
    if "PYTEST_CURRENT_TEST" in os.environ:
        return {"api_key": "test_key", "base_url": "http://test", "model": "test", "provider": "Pytest Mock"}

    or_key = os.environ.get("OPENROUTER_API_KEY", "")
    if or_key:
        return {
            "api_key": or_key,
            "base_url": os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions"),
            "model": os.environ.get("OPENROUTER_MODEL", "poolside/laguna-xs.2:free"),
            "provider": "🚀 OpenRouter (AI Gateway)"
        }
        
    mm_key = os.environ.get("MINIMAX_API_KEY", "")
    if mm_key and mm_key != "your_minimax_direct_key_if_any":
        return {
            "api_key": mm_key,
            "base_url": os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1/chat/completions"),
            "model": os.environ.get("MINIMAX_MODEL", "MiniMax-Text-01"),
            "provider": "☁️  MiniMax (Direct Cloud)"
        }
        
    raise EnvironmentError(
        "❌ ไม่สามารถเชื่อมต่อกับ Gateway หรือ API ใดๆ ได้เลย\n"
        "💡 แนะนำ: กรุณาใส่ OPENROUTER_API_KEY หรือ MINIMAX_API_KEY ในไฟล์ .env"
    )

config = get_best_config()
API_KEY = config["api_key"]
BASE_URL = config["base_url"]
MODEL_NAME = config["model"]
ACTIVE_PROVIDER = config["provider"]

# Timeout
API_TIMEOUT = int(os.environ.get("MINIMAX_API_TIMEOUT", "30"))
CONNECTION_TIMEOUT = int(os.environ.get("MINIMAX_CONNECTION_TIMEOUT", "10"))
