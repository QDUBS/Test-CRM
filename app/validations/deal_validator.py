from .base import Validator, ValidationError


class DealValidator(Validator):
    # Validator for deal operations

    @classmethod
    def validate_create_deal(cls, data):
        # Check required fields
        cls.validate_required(
            data, ["dealname", "amount", "dealstage", "email"])

        # Validate dealname
        cls.validate_length(data, "dealname", min_length=3, max_length=5000)

        # Validate amount (should be a valid number)
        cls.validate_is_number(data, "amount")
        # Optional: Ensure amount is not negative
        cls.validate_range(data, "amount", min_value=0)

        # Validate dealstage
        cls.validate_length(data, "dealstage", min_length=3, max_length=5000)

        # Validate email (basic format check)
        cls.validate_email(data, "email")

        return True
