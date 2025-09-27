class UserFinancialData:
    """Represents user's financial profile"""
    
    def __init__(self, monthly_income, current_balance, monthly_expenses):
        self.monthly_income = float(monthly_income)
        self.current_balance = float(current_balance)
        self.monthly_expenses = float(monthly_expenses)
    
    def validate(self):
        """Validates financial data"""
        if self.monthly_income <= 0:
            raise ValueError('Monthly income must be positive')
        
        if self.current_balance < 0:
            raise ValueError('Balance cannot be negative')
        
        if self.monthly_expenses < 0:
            raise ValueError('Expenses cannot be negative')
        
        return True
    
    def to_dict(self):
        """Converts to dictionary for JSON response"""
        return {
            'monthly_income': self.monthly_income,
            'current_balance': self.current_balance,
            'monthly_expenses': self.monthly_expenses
        }