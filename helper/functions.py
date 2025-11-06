from django.core.exceptions import ValidationError

def validate_phone_number(value):
    # Ensure the number is a positive integer
    if value <= 0:
        raise ValidationError("Phone number must be a positive integer.")
    
    # Convert the value to a string to check its length
    phone_str = str(value)
    
    # Ensure the phone number has between 10 and 15 digits
    if len(phone_str) < 10:
        raise ValidationError("Phone number must have at least 10 digits.")
    if len(phone_str) > 15:
        raise ValidationError("Phone number cannot exceed 15 digits.")
