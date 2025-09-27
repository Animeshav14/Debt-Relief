def validate_simulation_request(data):
    """
    Validates the structure of a simulation request
    
    Args:
        data: Request data dictionary
    
    Returns:
        Dictionary with 'valid' boolean and optional 'error' message
    """
    
    # Check required top-level keys
    required_keys = ['financialData', 'debt', 'paymentAmount']
    for key in required_keys:
        if key not in data:
            return {
                'valid': False,
                'error': f'Missing required field: {key}'
            }
    
    # Validate financial data
    financial_data = data['financialData']
    financial_required = ['monthly_income', 'current_balance', 'monthly_expenses']
    
    for field in financial_required:
        if field not in financial_data:
            return {
                'valid': False,
                'error': f'Missing financial data field: {field}'
            }
        
        # Check if it's a valid number
        try:
            value = float(financial_data[field])
            if value < 0:
                return {
                    'valid': False,
                    'error': f'{field} cannot be negative'
                }
        except (ValueError, TypeError):
            return {
                'valid': False,
                'error': f'{field} must be a valid number'
            }
    
    # Validate debt data
    debt = data['debt']
    debt_required = ['name', 'balance', 'interest_rate', 'minimum_payment']
    
    for field in debt_required:
        if field not in debt:
            return {
                'valid': False,
                'error': f'Missing debt field: {field}'
            }
        
        # Check numeric fields
        if field != 'name':
            try:
                value = float(debt[field])
                if value < 0:
                    return {
                        'valid': False,
                        'error': f'{field} cannot be negative'
                    }
            except (ValueError, TypeError):
                return {
                    'valid': False,
                    'error': f'{field} must be a valid number'
                }
    
    # Validate payment amount
    try:
        payment = float(data['paymentAmount'])
        if payment <= 0:
            return {
                'valid': False,
                'error': 'Payment amount must be positive'
            }
    except (ValueError, TypeError):
        return {
            'valid': False,
            'error': 'Payment amount must be a valid number'
            }
    
    # All validations passed
    return {'valid': True}