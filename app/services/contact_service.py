import requests
import json
import time
from app.services import HubSpotClient
import logging

logger = logging.getLogger(__name__)


class ContactService(HubSpotClient):
    def create_or_update_contact(self, data):
        """Create or update a contact in HubSpot."""
        email = data['email']

        # First check if the contact already exists
        existing_contact = self._get_contact_by_email(email)

        if existing_contact:
            # If contact exists, update
            logger.info(
                f"Contact with email {email} exists. Updating contact.")
            url = f"{self.base_url}/contacts/v1/contact/vid/{existing_contact['vid']}/profile"
            response = self._make_request('POST', url, data)
        else:
            # If contact does not exist, create new one
            logger.info(
                f"Contact with email {email} does not exist. Creating a new contact.")
            url = f"{self.base_url}/contacts/v1/contact/email/{email}/profile"
            response = self._make_request('POST', url, data)

        if response.status_code == 200:
            logger.info(f"Successfully processed contact with email {email}")
        else:
            logger.error(
                f"Failed to process contact with email {email}. Status code: {response.status_code}, Response: {response.text}")

        return response.json()

    def _get_contact_by_email(self, email):
        """Check if the contact exists by email and return the contact if found."""
        url = f"{self.base_url}/contacts/v1/contact/email/{email}/profile"
        response = self._make_request('GET', url)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            # Log error if there is an issue
            logger.error(
                f"Error fetching contact by email {email}. Status code: {response.status_code}, Response: {response.text}")
            return None

    def get_recent_contacts(self, page, page_size):
        """Retrieve recently created contacts."""
        url = f"{self.base_url}/contacts/v1/lists/all/contacts/recent"
        params = {
            'count': page_size,
            'vidOffset': page * page_size,
        }
        response = self._make_request('GET', url)
        return response.json()

    def handle_rate_limit(self, response):
        """Handle rate limits using exponential backoff."""
        retries = 3

        if response.status_code == 429:
            # Get retry-after time from headers
            retry_after = int(response.headers.get("Retry-After", 1))
            wait_time = retry_after * (2 ** retries)
            logger.warning(
                f"Rate limit exceeded. Retrying after {wait_time} seconds.")
            time.sleep(retry_after)

            # Retry after waiting
            return True
        return False
