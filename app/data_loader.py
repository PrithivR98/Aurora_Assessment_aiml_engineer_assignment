import requests

class DataLoader:
    API_URL = "https://november7-730026606190.europe-west1.run.app/messages"

    def load_messages(self):
        """
        Fetches paginated messages and returns a flat list of message dicts.
        API response format:
        {
            "total": 123,
            "items": [ {...}, {...} ]
        }
        """
        response = requests.get(self.API_URL)
        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict) and "items" in data:
            return data["items"]

        raise ValueError(f"Unexpected API format: {data}")
