from app.services import HubSpotClient
import logging

logger = logging.getLogger(__name__)


class DealService(HubSpotClient):
    def create_or_update_deal(self, data):
        """Create or update a deal in HubSpot."""
        
        # Check if the deal already exists
        existing_deals = self.search_deals(data['dealname'])

        if existing_deals:
            # If a deal exists, update
            deal_id = existing_deals[0]['dealId']
            url = f"{self.base_url}/deals/v1/deal/{deal_id}"
            response = self._make_request('POST', url, data)
            logger.info(f"Deal updated: {deal_id}")
            return response.json()
        else:
            # If no deal exists, create new one
            url = f"{self.base_url}/deals/v1/deal"
            response = self._make_request('POST', url, data)
            logger.info(f"Deal created successfully")
            return response.json()

    def search_deals(self, deal_name):
        """Search for an existing deal by name to check if it already exists."""
        url = f"{self.base_url}/deals/v1/deal/associated/contact/email/{deal_name}/paged"
        response = self._make_request('GET', url)
        if response.status_code == 200:
            data = response.json()
            # Check if any deal exists with the same name or related info
            if data.get('deals'):
                return data['deals']
        return []

    def get_recent_deals(self, page, page_size):
        """Retrieve recently created deals."""
        url = f"{self.base_url}/deals/v1/deal/recent"
        params = {
            'count': page_size,
            'vidOffset': page * page_size,
        }
        response = self._make_request('GET', url)
        return response.json()
