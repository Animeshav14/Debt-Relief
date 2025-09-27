from datetime import datetime, timedelta
from .debt_info import DebtInfo

class MedicalDebtInfo(DebtInfo):
    """Represents medical debt with specific characteristics"""
    
    def __init__(self, name, balance, interest_rate, minimum_payment, 
                 debt_type='medical', provider_name=None, service_date=None, 
                 insurance_coverage=None, payment_plan_available=False, current_payment=None):
        super().__init__(name, balance, interest_rate, minimum_payment, debt_type)
        self.provider_name = provider_name
        self.service_date = service_date
        self.insurance_coverage = insurance_coverage  # Amount covered by insurance
        self.payment_plan_available = payment_plan_available
        self.original_balance = balance  # Track original amount before any payments
        self.current_payment = current_payment or minimum_payment  # Current monthly payment amount
    
    def get_insurance_discount(self):
        """Calculate potential insurance discount if not already applied"""
        if self.insurance_coverage and self.insurance_coverage > 0:
            return min(self.insurance_coverage, self.original_balance * 0.5)  # Max 50% discount
        return 0
    
    def get_payment_plan_benefits(self):
        """Calculate benefits of payment plan (usually 0% interest)"""
        if self.payment_plan_available:
            return {
                'interest_rate': 0.0,
                'monthly_payment': round(self.balance / 12, 2),  # 12-month plan
                'savings': round(self.calculate_interest_savings(), 2)
            }
        return None
    
    def calculate_interest_savings(self):
        """Calculate interest savings from payment plan"""
        if not self.payment_plan_available:
            return 0
        
        # Calculate what interest would be without payment plan
        monthly_rate = self.interest_rate / 100 / 12
        months = 12  # Payment plan duration
        interest_without_plan = self.balance * monthly_rate * months
        return interest_without_plan
    
    def validate_medical_specific(self):
        """Validate medical debt specific fields"""
        if self.service_date:
            try:
                datetime.strptime(self.service_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Service date must be in YYYY-MM-DD format')
        
        if self.insurance_coverage and self.insurance_coverage < 0:
            raise ValueError('Insurance coverage cannot be negative')
        
        return True
    
    def to_dict(self):
        """Convert to dictionary including medical-specific fields"""
        base_dict = super().to_dict()
        base_dict.update({
            'provider_name': self.provider_name,
            'service_date': self.service_date,
            'insurance_coverage': self.insurance_coverage,
            'payment_plan_available': self.payment_plan_available,
            'original_balance': self.original_balance,
            'current_payment': self.current_payment,
            'insurance_discount': self.get_insurance_discount(),
            'payment_plan_benefits': self.get_payment_plan_benefits()
        })
        return base_dict


class MedicalDebtGoal:
    """Represents user's debt payoff goals"""
    
    def __init__(self, target_payoff_months=24):
        self.target_payoff_months = target_payoff_months
    
    def validate(self):
        """Validate goal parameters"""
        if self.target_payoff_months <= 0:
            raise ValueError('Target payoff months must be positive')
        
        return True
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'target_payoff_months': self.target_payoff_months
        }
