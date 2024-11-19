import requests
import time

# Base API URL and Candidate ID
API_URL = "https://challenge.crossmint.io/api/"
CANDIDATE_ID = "52d73a9a-4484-4722-bb44-cf33d1c603a2"

class MegaverseAPI:
    """Handles communication with the Megaverse API."""

    @staticmethod
    def get_goal_map():
        """Fetch the goal map."""
        url = f"{API_URL}/map/{CANDIDATE_ID}/goal"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch goal map: {response.status_code} - {response.text}")
            return None

    @staticmethod
    def create_polyanet(row, column):
        """Create a Polyanet at a given position."""
        url = f"{API_URL}polyanets"
        payload = {
            "candidateId": CANDIDATE_ID,
            "row": row,
            "column": column,
        }
        headers = {"Content-Type": "application/json"}
        return MegaverseAPI._make_request("POST", url, json=payload, headers=headers)

    @staticmethod
    def create_soloon(row, column, color):
        """Create a Soloon at the specified position."""
        url = f"{API_URL}/soloons"
        payload = {"row": row, "column": column, "color": color, "candidateId": CANDIDATE_ID}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200

    @staticmethod
    def create_cometh(row, column, direction):
        """Create a Cometh at the specified position."""
        url = f"{API_URL}/comeths"
        payload = {"row": row, "column": column, "direction": direction, "candidateId": CANDIDATE_ID}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200

    @staticmethod
    def delete_polyanet(row, column):
        """Delete a Polyanet at a given position."""
        url = f"{API_URL}polyanets"
        payload = {
            "candidateId": CANDIDATE_ID,
            "row": row,
            "column": column,
        }
        headers = {"Content-Type": "application/json"}
        return MegaverseAPI._make_request("DELETE", url, json=payload, headers=headers)

    @staticmethod
    def _make_request(method, url, **kwargs):
        """Handles rate-limiting and retries for API requests."""
        while True:
            try:
                response = requests.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    print("Rate limit reached. Retrying after a delay...")
                    time.sleep(2)  # Adjust delay as needed
                else:
                    print(f"HTTP error: {e}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                return None
