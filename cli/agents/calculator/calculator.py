import asyncio
import math
from typing import Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

# ===== CẤU HÌNH =====
AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzZjQxOWRhMC0zMmNjLTQ4ODgtOWM1NS1hMjI4OGMwMTZmODciLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjUzYjI0YTQxLWE4MjUtNDI1Ni1hN2Y1LTYzYWRmODhlMzhmYSJ9.HEW9uBkgYiNrlMRxLaA0Yr78wPOf7FKB1Enihq3FoDw" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)

# ===== LOGIC TÍNH TOÁN =====

@session.bind(
    name="calculator",
    description="Thực hiện các phép tính toán học: cộng, trừ, nhân, chia, lũy thừa, căn bậc hai, phần trăm, chia lấy dư."
)
async def calculator(
    agent_context: GenAIContext,
    operation: Annotated[
        str,
        "Loại phép tính cần thực hiện. Các giá trị hợp lệ: 'add' (cộng), 'subtract' (trừ), 'multiply' (nhân), 'divide' (chia), 'power' (lũy thừa), 'sqrt' (căn bậc 2), 'percentage' (tính phần trăm), 'modulo' (chia lấy dư).",
    ],
    x: Annotated[
        float, 
        "Số thứ nhất (hoặc số cần tính căn bậc 2)."
    ],
    y: Annotated[
        float, 
        "Số thứ hai (Mặc định là 0 nếu tính căn bậc 2)."
    ] = 0.0,
) -> str:
    """Hàm xử lý logic tính toán"""
    
    print(f"-> AI đang tính: {x} {operation} {y}")
    
    try:
        result = 0.0
        
        # 1. Phép cộng
        if operation == "add":
            result = x + y
            
        # 2. Phép trừ
        elif operation == "subtract":
            result = x - y
            
        # 3. Phép nhân
        elif operation == "multiply":
            result = x * y
            
        # 4. Phép chia
        elif operation == "divide":
            if y == 0:
                return "Lỗi: Không thể chia cho 0."
            result = x / y
            
        # 5. Lũy thừa (x mũ y)
        elif operation == "power":
            result = math.pow(x, y)
            
        # 6. Căn bậc hai (của x)
        elif operation == "sqrt":
            if x < 0:
                return "Lỗi: Không thể tính căn bậc hai của số âm."
            result = math.sqrt(x)
            return f"Căn bậc hai của {x} là {result}"

        # 7. Phần trăm (x phần trăm của y)
        # Ví dụ: 20 percentage 500 -> 20% của 500 = 100
        elif operation == "percentage":
            result = (x / 100) * y
            return f"{x}% của {y} là {result}"

        # 8. Modulo (Chia lấy dư)
        elif operation == "modulo":
            if y == 0:
                return "Lỗi: Không thể chia lấy dư cho 0."
            result = x % y

        else:
            return f"Lỗi: Phép tính '{operation}' không được hỗ trợ."

        return f"Kết quả của phép {operation} giữa {x} và {y} là: {result}"

    except Exception as e:
        return f"Gặp lỗi khi tính toán: {str(e)}"


# ===== CHẠY AGENT =====

async def main():
    print(f"Calculator Agent đang chạy...")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())