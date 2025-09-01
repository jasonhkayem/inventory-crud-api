from marshmallow import ValidationError

def validate_input(schema_class, data, partial=False):
    """
    Validate input data against a Marshmallow schema.
    ---
    Args:
        schema_class (Schema): A Marshmallow Schema class to validate against.
        data (dict): The input data to validate.
        partial (bool): Whether to allow partial validation (e.g., for PATCH/PUT updates).

    Returns:
        tuple: A tuple (valid_data, errors) where:
            - valid_data (dict or None): The deserialized and validated data if no errors.
            - errors (dict or None): Validation error messages if validation fails.

    Example:
        # Full validation (POST)
        valid_data, errors = validate_input(ProductSchema, request.get_json())

        # Partial validation (PUT)
        valid_data, errors = validate_input(ProductSchema, request.get_json(), partial=True)
    """
    schema = schema_class()
    try:
        return schema.load(data, partial=partial), None
    except ValidationError as err:
        return None, err.messages

