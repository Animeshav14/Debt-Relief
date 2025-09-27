from .user_financial_data import UserFinancialData
from .medical_debt_info import MedicalDebtInfo, MedicalDebtGoal

class MedicalSimulationInput:
    """Combines all input data for a medical debt simulation"""
    
    def __init__(self, financial_data, medical_debts, goals, current_income_sources=None):
        self.financial_data = UserFinancialData(
            financial_data['monthly_income'],
            financial_data['current_balance'],
            financial_data['monthly_expenses']
        )
        
        # Handle multiple medical debts
        self.medical_debts = []
        for debt_data in medical_debts:
            medical_debt = MedicalDebtInfo(
                name=debt_data['name'],
                balance=debt_data['balance'],
                interest_rate=debt_data['interest_rate'],
                minimum_payment=debt_data['minimum_payment'],
                debt_type='medical',
                provider_name=debt_data.get('provider_name'),
                service_date=debt_data.get('service_date'),
                insurance_coverage=debt_data.get('insurance_coverage', 0),
                payment_plan_available=debt_data.get('payment_plan_available', False),
                current_payment=debt_data.get('current_payment')
            )
            self.medical_debts.append(medical_debt)
        
        # Create goal object
        self.goals = MedicalDebtGoal(
            target_payoff_months=goals.get('target_payoff_months', 24)
        )
        
        # Additional income sources for earning plans
        self.current_income_sources = current_income_sources or []
        
        # Calculate total debt
        self.total_debt = sum(debt.balance for debt in self.medical_debts)
        self.total_minimum_payments = sum(debt.minimum_payment for debt in self.medical_debts)
        self.total_current_payments = sum(debt.current_payment for debt in self.medical_debts)
    
    def validate(self):
        """Validates all input data"""
        # Validate financial data
        self.financial_data.validate()
        
        # Validate each medical debt
        for debt in self.medical_debts:
            debt.validate()
            debt.validate_medical_specific()
        
        # Validate goals
        self.goals.validate()
        
        # Validate total debt vs income
        if self.total_minimum_payments > self.financial_data.monthly_income * 0.5:
            raise ValueError(
                'Total minimum payments cannot exceed 50% of monthly income. '
                f'Current: ${self.total_minimum_payments:.2f}, '
                f'50% of income: ${self.financial_data.monthly_income * 0.5:.2f}'
            )
        
        
        return True
    
    def get_debt_summary(self):
        """Get summary of all medical debts"""
        return {
            'total_debt': self.total_debt,
            'total_minimum_payments': self.total_minimum_payments,
            'total_current_payments': self.total_current_payments,
            'debt_count': len(self.medical_debts),
            'debt_details': [debt.to_dict() for debt in self.medical_debts]
        }
    
    def get_available_payment_plans(self):
        """Get debts that offer payment plans"""
        return [debt for debt in self.medical_debts if debt.payment_plan_available]
    
    def get_high_interest_debts(self, threshold=5.0):
        """Get debts with interest rate above threshold"""
        return [debt for debt in self.medical_debts if debt.interest_rate > threshold]
    
    def calculate_insurance_savings(self):
        """Calculate total potential insurance savings"""
        return sum(debt.get_insurance_discount() for debt in self.medical_debts)
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'financial_data': self.financial_data.to_dict(),
            'medical_debts': [debt.to_dict() for debt in self.medical_debts],
            'goals': self.goals.to_dict(),
            'current_income_sources': self.current_income_sources,
            'debt_summary': self.get_debt_summary(),
            'available_payment_plans': len(self.get_available_payment_plans()),
            'insurance_savings': self.calculate_insurance_savings()
        }
