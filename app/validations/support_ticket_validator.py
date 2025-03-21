from .base import Validator, ValidationError


class SupportTicketValidator(Validator):
    # Validator for support-ticket operations

    @classmethod
    def validate_create_support_ticket(cls, data):

        # Check required fields
        cls.validate_required(
            data, [
                    "subject", 
                    "description", 
                    "category", 
                    "pipeline", 
                    "hs_ticket_priority", 
                    "hs_pipeline_stage"])

        # Validate dealname
        cls.validate_length(
            data, "dealname", min_length=3, max_length=5000
        )

        # Validate amount
        cls.validate_length(
            data, "amount", min_length=3, max_length=5000
        )

        # Validate dealstage
        cls.validate_length(
            data, "dealstage", min_length=3, max_length=5000
        )

        return True
