import asyncio
import requests
from typing import Annotated, Any, Dict
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYjQ4OWNlZC00ZWRkLTRkNWQtOGVkNi0zODc2NDUzZWU1NzEiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6IjUzYjI0YTQxLWE4MjUtNDI1Ni1hN2Y1LTYzYWRmODhlMzhmYSJ9.j4s2H44yL9nViosxgG53bAk513gndRQjbHwWA-CIzfo" # noqa: E501
WEATHER_API_KEY = "f6c488309ebf49eeb0941626252611"
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="get_current_weather",
    description="Lấy thông tin thời tiết hiện tại cho một thành phố cụ thể."
)
async def weather(
    agent_context: GenAIContext,
    location: Annotated[
        str,
        "Tên thành phố hoặc địa điểm muốn xem thời tiết (ví dụ: Hanoi, Tokyo, Ho Chi Minh City).", 
    ],
) -> str:
    """Hàm này gọi WeatherAPI để lấy dữ liệu thực tế."""
    
    print(f"-> AI đang yêu cầu thời tiết cho: {location}")

    if not location:
        return "Lỗi: Không xác định được địa điểm."

    url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": WEATHER_API_KEY, "q": location, "aqi": "no"}

    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            loc = data["location"]
            cur = data["current"]
            
            result_text = (
                f"Dữ liệu thời tiết tại {loc['name']}, {loc['country']}:\n"
                f"- Nhiệt độ: {cur['temp_c']}°C (Cảm giác như: {cur['feelslike_c']}°C)\n"
                f"- Tình trạng: {cur['condition']['text']}\n"
                f"- Độ ẩm: {cur['humidity']}%\n"
                f"- Gió: {cur['wind_kph']} km/h\n"
                f"- Giờ địa phương: {loc['localtime']}"
            )
            return result_text
        else:
            return f"Lỗi từ WeatherAPI: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Gặp lỗi khi gọi API: {str(e)}"


async def main():
    print(f"Weather Agent đang chạy với token... (JWT)")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())