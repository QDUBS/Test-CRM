from app.services import HubSpotClient
import logging

logger = logging.getLogger(__name__)


class SupportTicketService(HubSpotClient):
    def create_ticket(self, data):
        """Create a new support ticket in HubSpot."""
        url = f"{self.base_url}/tickets/v1/ticket"

        # Validate that 'contact_id' and 'deal_ids' are available in the payload
        contact_id = data.get('contact_id')
        deal_ids = data.get('deal_ids', [])

        if not contact_id:
            logger.error("Missing contact ID for the support ticket.")
            return {"error": "Missing contact ID."}

        ticket_data = {
            "subject": data.get("subject"),
            "description": data.get("description"),
            "category": data.get("category"),
            "pipeline": data.get("pipeline"),
            "hs_ticket_priority": data.get("hs_ticket_priority"),
            "hs_pipeline_stage": data.get("hs_pipeline_stage"),
            "associations": {
                "associatedVids": [contact_id],  # Links the ticket to a contact
                "associatedDealIds": deal_ids   # Links the ticket to the provided deals
            }
        }

        # Create new ticket
        response = self._make_request('POST', url, ticket_data)

        if response.status_code == 200:
            logger.info(f"Ticket created successfully: {data['subject']}")
            return response.json()
        else:
            logger.error(f"Failed to create ticket: {response.text}")
            return {'error': 'Ticket creation failed'}

    def get_recent_tickets(self, page, page_size):
        """Retrieve recently created tickets."""
        url = f"{self.base_url}/tickets/v1/ticket/recent"
        params = {
            'count': page_size,
            'vidOffset': page * page_size,
        }
        response = self._make_request('GET', url)
        return response.json()
