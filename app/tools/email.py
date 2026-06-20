import httpx
from app.config import settings

async def send_email(to: str, subject: str, body: str) -> dict:
    if not settings.resend_api_key:
        return {"error": "Resend API key not configured"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.resend_api_key}"},
            json={
                "from": settings.email_from,
                "to": to,
                "subject": subject,
                "html": body
            }
        )
        return resp.json()