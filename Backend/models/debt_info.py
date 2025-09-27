class DebtInfo:
    """Represents a debt account"""
    
    def __init__(self, name, balance, interest_rate, minimum_payment, debt_type='credit_card'):
        self.name = name
        self.balance = float(balance)
        self.interest_rate = float(interest_rate)  # APR as percentage
        self.minimum_payment = float(minimum_payment)
        self.debt_type = debt_type
    
    def validate(self):
        """Validates debt information"""
        if self.balance <= 0:
            raise ValueError('Debt balance must be positive')
        
        if self.interest_rate < 0:
            raise ValueError('Interest rate cannot be negative')
        
        if self.minimum_payment <= 0:
            raise ValueError('Minimum payment must be positive')
        
        if self.minimum_payment > self.balance:
            raise ValueError('Minimum payment cannot exceed balance')
        
        return True
    
    def get_monthly_rate(self):
        """Converts APR to monthly rate"""
        return self.interest_rate / 100 / 12
    
    def to_dict(self):
        """Converts to dictionary for JSON response"""
        return {
            'name': self.name,
            'balance': self.balance,
            'interest_rate': self.interest_rate,
            'minimum_payment': self.minimum_payment,
            'debt_type': self.debt_type
        }