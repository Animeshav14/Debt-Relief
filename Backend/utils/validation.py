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


def validate_medical_simulation_request(data):
    """
    Validates the structure of a medical debt simulation request
    
    Args:
        data: Request data dictionary
    
    Returns:
        Dictionary with 'valid' boolean and optional 'error' message
    """
    
    # Check required top-level keys
    required_keys = ['financialData', 'medicalDebts', 'goals']
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
    
    # Validate medical debts array
    medical_debts = data['medicalDebts']
    if not isinstance(medical_debts, list) or len(medical_debts) == 0:
        return {
            'valid': False,
            'error': 'medicalDebts must be a non-empty array'
        }
    
    debt_required = ['name', 'balance', 'interest_rate', 'minimum_payment']
    for i, debt in enumerate(medical_debts):
        if not isinstance(debt, dict):
            return {
                'valid': False,
                'error': f'Medical debt {i} must be an object'
            }
        
        for field in debt_required:
            if field not in debt:
                return {
                    'valid': False,
                    'error': f'Missing debt field in medical debt {i}: {field}'
                }
            
            if field != 'name':
                try:
                    value = float(debt[field])
                    if value < 0:
                        return {
                            'valid': False,
                            'error': f'{field} in medical debt {i} cannot be negative'
                        }
                except (ValueError, TypeError):
                    return {
                        'valid': False,
                        'error': f'{field} in medical debt {i} must be a valid number'
                    }
        
        # Validate optional medical-specific fields
        if 'service_date' in debt and debt['service_date']:
            try:
                from datetime import datetime
                datetime.strptime(debt['service_date'], '%Y-%m-%d')
            except ValueError:
                return {
                    'valid': False,
                    'error': f'service_date in medical debt {i} must be in YYYY-MM-DD format'
                }
        
        if 'insurance_coverage' in debt:
            try:
                value = float(debt['insurance_coverage'])
                if value < 0:
                    return {
                        'valid': False,
                        'error': f'insurance_coverage in medical debt {i} cannot be negative'
                    }
            except (ValueError, TypeError):
                return {
                    'valid': False,
                    'error': f'insurance_coverage in medical debt {i} must be a valid number'
                }
    
    # Validate goals
    goals = data['goals']
    if not isinstance(goals, dict):
        return {
            'valid': False,
            'error': 'goals must be an object'
        }
    
    # Validate goal fields
    if 'target_payoff_months' in goals:
        try:
            months = int(goals['target_payoff_months'])
            if months <= 0:
                return {
                    'valid': False,
                    'error': 'target_payoff_months must be positive'
                }
        except (ValueError, TypeError):
            return {
                'valid': False,
                'error': 'target_payoff_months must be a valid integer'
            }
    
    # Validate current income sources if provided
    if 'currentIncomeSources' in data:
        income_sources = data['currentIncomeSources']
        if not isinstance(income_sources, list):
            return {
                'valid': False,
                'error': 'currentIncomeSources must be an array'
            }
        
        for i, source in enumerate(income_sources):
            if not isinstance(source, dict):
                return {
                    'valid': False,
                    'error': f'Income source {i} must be an object'
                }
            
            required_source_fields = ['source', 'amount', 'frequency']
            for field in required_source_fields:
                if field not in source:
                    return {
                        'valid': False,
                        'error': f'Missing field in income source {i}: {field}'
                    }
            
            try:
                amount = float(source['amount'])
                if amount < 0:
                    return {
                        'valid': False,
                        'error': f'amount in income source {i} cannot be negative'
                    }
            except (ValueError, TypeError):
                return {
                    'valid': False,
                    'error': f'amount in income source {i} must be a valid number'
                }
    
    # All validations passed
    return {'valid': True}