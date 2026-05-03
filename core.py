# -*- coding: utf-8 -*-
"""
Core Logic
รับผิดชอบการเชื่อมต่อ API และการประมวลผลหลัก
"""

import json
import requests
from typing import Dict, Any

from prompt import SYSTEM_PROMPT
from config import CONNECTION_TIMEOUT, API_TIMEOUT

class MiniMaxAPIError(Exception):
    """Custom exception สำหรับข้อผิดพลาดของ API"""
    pass

class CLIConverter:
    """คลาสหลักสำหรับ CLI Converter จัดการการเชื่อมต่อกับ AI API"""

    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _validate_command(self, command: str) -> bool:
        if not command or not command.strip():
            return False
        if len(command.strip()) < 2:
            return False
        return True

    def _build_payload(self, user_command: str) -> Dict[str, Any]:
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"แปลงคำสั่งนี้: {user_command}"}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }

    def convert(self, command: str) -> str:
        if not self._validate_command(command):
            return "❌ คำสั่งไม่ถูกต้อง กรุณาป้อนคำสั่งที่ถูกต้อง"

        payload = self._build_payload(command)

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=(CONNECTION_TIMEOUT, API_TIMEOUT)
            )
            response.raise_for_status()
            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "❌ ไม่สามารถรับผลลัพธ์จาก API ได้"

        except requests.exceptions.ConnectionError:
            raise MiniMaxAPIError("❌ ไม่สามารถเชื่อมต่อกับ API ได้ กรุณาตรวจสอบการเชื่อมต่ออินเทอร์เน็ต")
        except requests.exceptions.Timeout:
            raise MiniMaxAPIError("❌ การเชื่อมต่อกับ API เกินเวลา กรุณาลองใหม่ภายหลัง")
        except requests.exceptions.HTTPError as e:
            raise MiniMaxAPIError(f"❌ เกิดข้อผิดพลาด HTTP: {e}")
        except json.JSONDecodeError:
            raise MiniMaxAPIError("❌ ไม่สามารถอ่านผลลัพธ์จาก API ได้")
        except Exception as e:
            raise MiniMaxAPIError(f"❌ เกิดข้อผิดพลาดที่ไม่คาดคิด: {str(e)}")
