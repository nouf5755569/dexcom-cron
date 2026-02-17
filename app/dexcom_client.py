import os
import logging
import requests
from typing import List, Dict, Any

class DexcomClient:
    def __init__(self):
        self.log = logging.getLogger("dexcom")
        self.base_url = os.getenv("DEXCOM_BASE_URL", "https://sandbox-api.dexcom.com").rstrip("/")
        self.access_token = os.getenv("DEXCOM_ACCESS_TOKEN", "").strip()

        if not self.access_token:
            self.log.warning("DEXCOM_ACCESS_TOKEN is empty. Add it in Render Environment variables.")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }

    def fetch_latest_glucose(self, max_count: int = 36) -> List[Dict[str, Any]]:
        """
        ملاحظة:
        Endpoint الحقيقي يعتمد على Dexcom API اللي عندك (Sandbox/Prod).
        إذا ارسلتي لي endpoint اللي تستخدمينه حاليًا، أعدله لك مباشرة.
        """
        # مثال شائع (قد يحتاج تعديل حسب حسابك/الـ scope):
        # /v2/users/self/egvs?startDate=...&endDate=...
        # هنا بنحاول endpoint "egvs" مع فترة زمنية بسيطة.
        url = f"{self.base_url}/v2/users/self/egvs"

        # Dexcom يحتاج startDate/endDate بصيغة ISO. نتركه الآن بسيط، وإذا رفض نضبطه حسب وثيقتك.
        params = {
            "startDate": "2026-01-01T00:00:00",
            "endDate": "2026-12-31T00:00:00",
        }

        r = requests.get(url, headers=self._headers(), params=params, timeout=30)

        if r.status_code != 200:
            self.log.error("Dexcom API error %s: %s", r.status_code, r.text[:500])
            return []

        data = r.json()

        # نتوقع شكل:
        # {"records":[{"systemTime":"...","value":123,...}, ...]}
        records = data.get("records", []) or data.get("egvs", []) or []

        # خذي آخر max_count
        return records[-max_count:]
