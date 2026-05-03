# -*- coding: utf-8 -*-
"""
Utility Functions
ฟังก์ชันช่วยเหลือต่างๆ เช่น พิมพ์เมนู และจัดการหน้าจอ
"""

import os
import platform
from config import ACTIVE_PROVIDER, MODEL_NAME

EXIT_COMMANDS = {"exit", "quit", "q", "ออก", "จบ"}

def print_banner() -> None:
    """พิมพ์ banner ของโปรแกรม"""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🔄 CLI Converter - เครื่องมือแปลงคำสั่ง 🔄           ║
║                                                              ║
║     แปลงคำสั่งระหว่าง PowerShell, CMD และ Linux (Bash)        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
  🔌 Connection : {ACTIVE_PROVIDER}
  🧠 Model      : {MODEL_NAME}
"""
    print(banner)

def print_help() -> None:
    """พิมพ์คำสั่งช่วยเหลือ"""
    help_text = """
📌 วิธีใช้งาน:
   - พิมพ์คำสั่ง CLI ที่ต้องการแปลง แล้วกด Enter
   - ระบบจะแสดงคำสั่งที่เทียบเท่าสำหรับทุก shell

📌 ตัวอย่างคำสั่ง:
   - ls -la
   - Get-ChildItem
   - dir /s

📌 คำสั่งพิเศษ:
   - help    : แสดงคำสั่งช่วยเหลือนี้
   - clear   : ล้างหน้าจอ
   - exit/quit : ออกจากโปรแกรม

⚠️  การออก: พิมพ์ 'exit', 'quit', 'q', 'ออก' หรือ 'จบ'
"""
    print(help_text)

def clear_screen() -> None:
    """ล้างหน้าจอ (cross-platform)"""
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def is_exit_command(command: str) -> bool:
    return command.strip().lower() in EXIT_COMMANDS
