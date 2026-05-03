#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Converter - เครื่องมือแปลงคำสั่ง CLI ข้ามแพลตฟอร์ม
(Main Entry Point)
"""

from config import API_KEY, BASE_URL, MODEL_NAME
from core import CLIConverter, MiniMaxAPIError
from utils import print_banner, print_help, clear_screen, is_exit_command

def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    print_banner()
    print_help()
    print("-" * 60)
    print()

    converter = CLIConverter(
        api_key=API_KEY,
        base_url=BASE_URL,
        model=MODEL_NAME
    )

    while True:
        try:
            user_input = input("🔧 พิมพ์คำสั่งที่ต้องการแปลง: ").strip()

            if is_exit_command(user_input):
                print("\n👋 ขอบคุณที่ใช้งาน CLI Converter! สวัสดีครับ/ค่ะ 👋\n")
                break

            if user_input.lower() == "help":
                print_help()
                continue
            elif user_input.lower() == "clear":
                clear_screen()
                print_banner()
                continue

            if not user_input:
                print("⚠️  กรุณาพิมพ์คำสั่งที่ต้องการแปลง\n")
                continue

            print("\n⏳ กำลังแปลงคำสั่ง...\n")
            result = converter.convert(user_input)
            print(result)
            print("\n" + "-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n\n👋 ขอบคุณที่ใช้งาน CLI Converter! สวัสดีครับ/ค่ะ 👋\n")
            break
        except (EOFError, IOError) as e:
            print("\n\n👋 ขอบคุณที่ใช้งาน CLI Converter! สวัสดีครับ/ค่ะ 👋\n")
            break
        except MiniMaxAPIError as e:
            print(f"\n{e}\n")
            print("💡 แนะนำ: ตรวจสอบการเชื่อมต่ออินเทอร์เน็ตแล้วลองใหม่\n")
            print("-" * 60 + "\n")
        except Exception as e:
            print(f"\n❌ เกิดข้อผิดพลาดที่ไม่คาดคิด: {str(e)}\n")
            print("💡 แนะนำ: รีสตาร์ทโปรแกรมแล้วลองใหม่\n")
            print("-" * 60 + "\n")

if __name__ == "__main__":
    main()