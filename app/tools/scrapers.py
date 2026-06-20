import asyncio
from typing import List, Dict, Any

async def scrape_linkedin() -> List[Dict[str, Any]]:
    await asyncio.sleep(0.2)
    return [
        {
            "company_name": "TechStart Inc.",
            "contact_name": "John Doe",
            "email": "john@techstart.com",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "source_platform": "linkedin"
        }
    ]

async def scrape_upwork() -> List[Dict[str, Any]]:
    await asyncio.sleep(0.2)
    return [
        {
            "company_name": "Upwork Client",
            "contact_name": "Sarah",
            "email": "sarah@example.com",
            "source_platform": "upwork"
        }
    ]

async def scrape_google_maps() -> List[Dict[str, Any]]:
    await asyncio.sleep(0.2)
    return []

async def scrape_all_platforms() -> List[Dict[str, Any]]:
    linkedin = await scrape_linkedin()
    upwork = await scrape_upwork()
    maps = await scrape_google_maps()
    return linkedin + upwork + maps