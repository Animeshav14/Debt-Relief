from .user_financial_data import UserFinancialData
from .debt_info import DebtInfo

class SimulationInput:
    """Combines all input data for a simulation"""
    
    def __init__(self, financial_data, debt, payment_amount):
        self.financial_data = UserFinancialData(
            financial_data['monthly_income'],
            financial_data['current_balance'],
            financial_data['monthly_expenses']
        )
        
        self.debt = DebtInfo(
            debt['name'],
            debt['balance'],
            debt['interest_rate'],
            debt['minimum_payment'],
            debt.get('type', 'credit_card')
        )
        
        self.payment_amount = float(payment_amount)
    
    def validate(self):
        """Validates all input data"""
        # Validate individual components
        self.financial_data.validate()
        self.debt.validate()
        
        # Validate payment amount
        if self.payment_amount < self.debt.minimum_payment:
            raise ValueError(
                f'Payment amount (${self.payment_amount}) must be at least '
                f'the minimum payment (${self.debt.minimum_payment})'
            )
        
        if self.payment_amount > self.financial_data.monthly_income:
            raise ValueError(
                'Payment amount cannot exceed monthly income'
            )
        
        return True
    
    def to_dict(self):
        """Converts to dictionary for JSON response"""
        return {
            'financial_data': self.financial_data.to_dict(),
            'debt': self.debt.to_dict(),
            'payment_amount': self.payment_amount
        }