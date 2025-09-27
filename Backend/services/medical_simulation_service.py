from datetime import datetime, timedelta
from typing import List, Dict, Any
from models.medical_simulation_input import MedicalSimulationInput
from models.medical_debt_info import MedicalDebtInfo
from services.nessie_service import nessie_service

class MedicalSimulationService:
    """Handles medical debt payoff simulation with Nessie API integration"""
    
    def __init__(self):
        self.nessie = nessie_service
    
    def simulate_current_trajectory(self, simulation_input: MedicalSimulationInput) -> Dict[str, Any]:
        """
        Simulate current trajectory using Nessie API
        Creates virtual accounts and simulates payments
        """
        try:
            # Create customer in Nessie
            customer = self.nessie.create_customer(
                first_name="Medical",
                last_name="DebtUser"
            )
            customer_id = customer.get('_id')
            
            # Create accounts for each medical debt
            debt_accounts = []
            for i, debt in enumerate(simulation_input.medical_debts):
                account = self.nessie.create_account(
                    customer_id=customer_id,
                    account_type="Credit Card",  # Using credit card type for debt simulation
                    balance=debt.balance
                )
                debt_accounts.append({
                    'debt': debt,
                    'account_id': account.get('_id'),
                    'account': account
                })
            
            # Simulate current trajectory (using actual current payments)
            current_trajectory = self._simulate_payment_strategy(
                debt_accounts, 
                simulation_input, 
                strategy='current_trajectory',
                months=9999  # No practical limit - brutally honest calculation
            )
            
            return {
                'customer_id': customer_id,
                'debt_accounts': debt_accounts,
                'current_trajectory': current_trajectory,
                'success': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to simulate current trajectory: {str(e)}',
                'fallback_simulation': self._fallback_simulation(simulation_input)
            }
    
    def _simulate_payment_strategy(self, debt_accounts: List[Dict], 
                                 simulation_input: MedicalSimulationInput,
                                 strategy: str, months: int = 9999) -> Dict[str, Any]:
        """Simulate different payment strategies"""
        timeline = []
        total_interest_paid = 0
        total_principal_paid = 0
        
        for month in range(1, months + 1):
            month_data = {
                'month': month,
                'date': (datetime.now() + timedelta(days=month * 30)).strftime('%Y-%m-%d'),
                'debt_payments': [],
                'total_payment': 0,
                'total_interest': 0,
                'total_principal': 0
            }
            
            for debt_account in debt_accounts:
                debt = debt_account['debt']
                account_id = debt_account['account_id']
                
                # Calculate payment amount based on strategy
                payment_amount = self._calculate_payment_amount(
                    debt, simulation_input, strategy, month
                )
                
                if payment_amount > 0:
                    # Calculate interest
                    monthly_rate = debt.interest_rate / 100 / 12
                    interest_charge = debt.balance * monthly_rate
                    
                    # Apply payment
                    principal_payment = max(0, payment_amount - interest_charge)
                    debt.balance = max(0, debt.balance - principal_payment)
                    
                    # Record transaction in Nessie (simulate payment)
                    try:
                        self.nessie.make_purchase(
                            account_id=account_id,
                            amount=-payment_amount,  # Negative for payment
                            description=f"Medical debt payment - {debt.name}"
                        )
                    except:
                        pass  # Continue simulation even if Nessie fails
                    
                    month_data['debt_payments'].append({
                        'debt_name': debt.name,
                        'payment_amount': payment_amount,
                        'interest_charge': interest_charge,
                        'principal_payment': principal_payment,
                        'remaining_balance': debt.balance
                    })
                    
                    month_data['total_payment'] += payment_amount
                    month_data['total_interest'] += interest_charge
                    month_data['total_principal'] += principal_payment
                    
                    total_interest_paid += interest_charge
                    total_principal_paid += principal_payment
            
            timeline.append(month_data)
            
            # Check if all debts are paid off
            if all(debt['debt'].balance <= 0.01 for debt in debt_accounts):
                break
        
        return {
            'timeline': timeline,
            'total_interest_paid': round(total_interest_paid, 2),
            'total_principal_paid': round(total_principal_paid, 2),
            'months_to_payoff': len(timeline),
            'debt_free_date': self._calculate_debt_free_date(len(timeline))
        }
    
    def _calculate_payment_amount(self, debt: MedicalDebtInfo, 
                                simulation_input: MedicalSimulationInput,
                                strategy: str, month: int) -> float:
        """Calculate payment amount based on strategy"""
        if debt.balance <= 0.01:
            return 0
        
        if strategy == 'minimum_only':
            return debt.minimum_payment
        
        elif strategy == 'current_trajectory':
            # Use the current payment amount the user is actually making
            return debt.current_payment
        
        elif strategy == 'goal_based':
            if simulation_input.goals.monthly_payment_limit:
                # Distribute goal payment across debts
                total_minimum = simulation_input.total_minimum_payments
                if total_minimum > 0:
                    return (debt.minimum_payment / total_minimum) * simulation_input.goals.monthly_payment_limit
            return debt.current_payment
        
        elif strategy == 'aggressive':
            # Pay more towards high-interest debts
            if debt.interest_rate > 5.0:  # High interest
                return debt.current_payment * 2
            return debt.current_payment
        
        elif strategy == 'snowball':
            # Pay minimum on all except smallest debt
            smallest_debt = min(simulation_input.medical_debts, key=lambda d: d.balance)
            if debt.name == smallest_debt.name:
                return debt.current_payment * 3
            return debt.current_payment
        
        return debt.current_payment
    
    def calculate_required_earnings(self, simulation_input: MedicalSimulationInput, 
                                  target_months: int) -> Dict[str, Any]:
        """Calculate required earnings to meet goals"""
        total_debt = simulation_input.total_debt
        
        # Calculate required monthly payment to pay off in target months
        if target_months <= 0:
            target_months = 1
        
        # Use average interest rate for calculation
        avg_interest_rate = sum(debt.interest_rate for debt in simulation_input.medical_debts) / len(simulation_input.medical_debts)
        monthly_rate = avg_interest_rate / 100 / 12
        
        # Calculate required payment using loan payment formula
        if monthly_rate > 0:
            required_payment = total_debt * (monthly_rate * (1 + monthly_rate) ** target_months) / ((1 + monthly_rate) ** target_months - 1)
        else:
            required_payment = total_debt / target_months
        
        # Calculate additional income needed
        current_available = simulation_input.financial_data.monthly_income - simulation_input.financial_data.monthly_expenses
        additional_income_needed = max(0, required_payment - current_available)
        
        return {
            'required_monthly_payment': round(required_payment, 2),
            'current_available_income': round(current_available, 2),
            'additional_income_needed': round(additional_income_needed, 2),
            'target_months': target_months,
            'total_debt': round(total_debt, 2),
            'average_interest_rate': round(avg_interest_rate, 2)
        }
    
    def generate_payoff_plans(self, simulation_input: MedicalSimulationInput) -> Dict[str, Any]:
        """Generate three different payoff plans"""
        current_trajectory = self.simulate_current_trajectory(simulation_input)
        
        # Plan 1: Long-term easier plan (minimum payments + small increase)
        easy_plan = self._create_easy_plan(simulation_input)
        
        # Plan 2: Middle-ground plan (moderate increase in payments)
        middle_plan = self._create_middle_plan(simulation_input)
        
        # Plan 3: Hardcore earning plan (aggressive payments + income increase)
        hardcore_plan = self._create_hardcore_plan(simulation_input)
        
        return {
            'current_trajectory': current_trajectory,
            'easy_plan': easy_plan,
            'middle_plan': middle_plan,
            'hardcore_plan': hardcore_plan,
            'comparison': self._compare_plans(easy_plan, middle_plan, hardcore_plan, simulation_input)
        }
    
    def get_current_trajectory_only(self, simulation_input: MedicalSimulationInput) -> Dict[str, Any]:
        """Get only the current trajectory analysis"""
        return {
            'current_trajectory': self.simulate_current_trajectory(simulation_input),
            'debt_summary': simulation_input.get_debt_summary(),
            'insurance_opportunities': self._analyze_insurance_opportunities(simulation_input),
            'payment_plan_opportunities': self._analyze_payment_plan_opportunities(simulation_input)
        }
    
    def calculate_current_trajectory_timeline(self, simulation_input: MedicalSimulationInput) -> Dict[str, Any]:
        """Calculate detailed timeline for current payment trajectory"""
        timeline = []
        total_interest_paid = 0
        total_principal_paid = 0
        
        # Create copies of debts to avoid modifying originals
        debt_copies = []
        for debt in simulation_input.medical_debts:
            debt_copy = MedicalDebtInfo(
                name=debt.name,
                balance=debt.balance,
                interest_rate=debt.interest_rate,
                minimum_payment=debt.minimum_payment,
                debt_type=debt.debt_type,
                provider_name=debt.provider_name,
                service_date=debt.service_date,
                insurance_coverage=debt.insurance_coverage,
                payment_plan_available=debt.payment_plan_available,
                current_payment=debt.current_payment
            )
            debt_copies.append(debt_copy)
        
        month = 0
        while any(debt.balance > 0.01 for debt in debt_copies) and month < 9999:  # Cap at 9999 months (80+ years)
            month += 1
            month_data = {
                'month': month,
                'date': (datetime.now() + timedelta(days=month * 30)).strftime('%Y-%m-%d'),
                'debt_payments': [],
                'total_payment': 0,
                'total_interest': 0,
                'total_principal': 0,
                'total_remaining_balance': 0
            }
            
            for debt in debt_copies:
                if debt.balance <= 0.01:
                    continue
                
                # Calculate interest for this month
                monthly_rate = debt.interest_rate / 100 / 12
                interest_charge = debt.balance * monthly_rate
                
                # Apply current payment
                payment_amount = debt.current_payment
                principal_payment = max(0, payment_amount - interest_charge)
                debt.balance = max(0, debt.balance - principal_payment)
                
                month_data['debt_payments'].append({
                    'debt_name': debt.name,
                    'payment_amount': payment_amount,
                    'interest_charge': interest_charge,
                    'principal_payment': principal_payment,
                    'remaining_balance': debt.balance
                })
                
                month_data['total_payment'] += payment_amount
                month_data['total_interest'] += interest_charge
                month_data['total_principal'] += principal_payment
                month_data['total_remaining_balance'] += debt.balance
                
                total_interest_paid += interest_charge
                total_principal_paid += principal_payment
            
            timeline.append(month_data)
        
        return {
            'timeline': timeline,
            'total_interest_paid': round(total_interest_paid, 2),
            'total_principal_paid': round(total_principal_paid, 2),
            'months_to_payoff': month,
            'debt_free_date': self._calculate_debt_free_date(month),
            'total_amount_paid': round(simulation_input.total_debt + total_interest_paid, 2),
            'current_monthly_payment': simulation_input.total_current_payments,
            'vs_minimum_payment': round(simulation_input.total_current_payments - simulation_input.total_minimum_payments, 2)
        }
    
    def _analyze_insurance_opportunities(self, simulation_input: MedicalSimulationInput) -> Dict[str, Any]:
        """Analyze potential insurance savings"""
        total_insurance_savings = simulation_input.calculate_insurance_savings()
        debts_with_insurance = [debt for debt in simulation_input.medical_debts if debt.insurance_coverage > 0]
        
        return {
            'total_potential_savings': total_insurance_savings,
            'debts_with_insurance': len(debts_with_insurance),
            'recommendations': [
                'Review all medical bills for insurance coverage opportunities',
                'Contact providers to verify insurance claims were processed correctly',
                'Consider appealing denied insurance claims',
                'Look into financial assistance programs'
            ] if total_insurance_savings > 0 else ['No insurance coverage opportunities identified']
        }
    
    def _analyze_payment_plan_opportunities(self, simulation_input: MedicalSimulationInput) -> Dict[str, Any]:
        """Analyze payment plan opportunities"""
        payment_plan_debts = simulation_input.get_available_payment_plans()
        total_savings = sum(debt.calculate_interest_savings() for debt in payment_plan_debts)
        
        return {
            'available_plans': len(payment_plan_debts),
            'total_interest_savings': total_savings,
            'debt_details': [
                {
                    'name': debt.name,
                    'provider': debt.provider_name,
                    'monthly_payment': debt.get_payment_plan_benefits()['monthly_payment'] if debt.get_payment_plan_benefits() else None,
                    'interest_savings': debt.calculate_interest_savings()
                }
                for debt in payment_plan_debts
            ],
            'recommendations': [
                'Contact providers to set up interest-free payment plans',
                'Negotiate payment terms based on your financial situation',
                'Consider consolidating multiple debts into single payment plans'
            ] if payment_plan_debts else ['No payment plan opportunities available']
        }
    
    def _create_easy_plan(self, simulation_input: MedicalSimulationInput) -> Dict[str, Any]:
        """Create easy long-term plan with 30-year cap"""
        # Start with minimum payments + 20%
        base_payment = max(simulation_input.total_minimum_payments, simulation_input.total_minimum_payments * 1.2)
        
        # Calculate honest payoff time with current payment strategy
        estimated_months = self._estimate_payoff_months(simulation_input, base_payment, max_months=9999)
        
        available_income = simulation_input.financial_data.monthly_income - simulation_input.financial_data.monthly_expenses
        additional_income_needed = max(0, base_payment - available_income)
        
        # If we need additional income, adjust recommendations
        recommendations = [
            'Set up automatic payments',
            'Consider payment plans with providers',
            'Look for insurance coverage opportunities'
        ]
        
        if additional_income_needed > 0:
            recommendations.extend([
                f'Find additional income of ${additional_income_needed:.2f} per month',
                'Consider a part-time job or side hustle',
                'Cut discretionary spending to free up money'
            ])
        
        return {
            'name': 'Easy Long-term Plan',
            'description': 'Slightly increase payments above minimum for manageable progress',
            'monthly_payment': round(base_payment, 2),
            'additional_income_needed': round(additional_income_needed, 2),
            'estimated_months': estimated_months,
            'total_interest_savings': 0,  # Will be calculated
            'difficulty': 'Easy',
            'recommendations': recommendations
        }
    
    def _create_middle_plan(self, simulation_input: MedicalSimulationInput) -> Dict[str, Any]:
        """Create middle-ground plan"""
        # Ensure payment is at least minimum payments, then add 50%
        base_payment = max(simulation_input.total_minimum_payments, simulation_input.total_minimum_payments * 1.5)
        available_income = simulation_input.financial_data.monthly_income - simulation_input.financial_data.monthly_expenses
        additional_income_needed = max(0, base_payment - available_income)
        
        # If we need additional income, adjust recommendations
        recommendations = [
            'Cut discretionary spending by 20%',
            'Negotiate payment plans with providers',
            'Apply for financial assistance programs'
        ]
        
        if additional_income_needed > 0:
            recommendations.extend([
                f'Find additional income of ${additional_income_needed:.2f} per month',
                'Consider a part-time job or side hustle',
                'Look for higher-paying opportunities'
            ])
        else:
            recommendations.append('Consider a part-time job or side hustle for faster payoff')
        
        return {
            'name': 'Balanced Plan',
            'description': 'Moderate increase in payments with some lifestyle adjustments',
            'monthly_payment': round(base_payment, 2),
            'additional_income_needed': round(additional_income_needed, 2),
            'estimated_months': self._estimate_payoff_months(simulation_input, base_payment),
            'total_interest_savings': 0,  # Will be calculated
            'difficulty': 'Moderate',
            'recommendations': recommendations
        }
    
    def _create_hardcore_plan(self, simulation_input: MedicalSimulationInput) -> Dict[str, Any]:
        """Create hardcore earning plan"""
        # Target 2-year payoff, but ensure it's at least minimum payments
        target_months = 24
        required_payment = self.calculate_required_earnings(simulation_input, target_months)['required_monthly_payment']
        
        # Ensure payment meets minimum requirements
        final_payment = max(required_payment, simulation_input.total_minimum_payments)
        
        available_income = simulation_input.financial_data.monthly_income - simulation_input.financial_data.monthly_expenses
        additional_income_needed = max(0, final_payment - available_income)
        
        # Adjust target months if we had to increase payment above calculated requirement
        if final_payment > required_payment:
            target_months = self._estimate_payoff_months(simulation_input, final_payment)
        
        return {
            'name': 'Hardcore Earning Plan',
            'description': 'Aggressive payments with significant income increase for fast payoff',
            'monthly_payment': round(final_payment, 2),
            'additional_income_needed': round(additional_income_needed, 2),
            'estimated_months': target_months,
            'total_interest_savings': 0,  # Will be calculated
            'difficulty': 'Hard',
            'recommendations': [
                f'Find additional income of ${additional_income_needed:.2f} per month' if additional_income_needed > 0 else 'Current income is sufficient for this plan',
                'Take on additional work or side hustles',
                'Cut all non-essential expenses',
                'Consider debt consolidation loan',
                'Apply for all available financial assistance',
                'Negotiate settlements with providers',
                'Consider selling assets if necessary'
            ]
        }
    
    def _estimate_payoff_months(self, simulation_input: MedicalSimulationInput, monthly_payment: float, max_months: int = 9999) -> int:
        """Estimate months to payoff with given payment"""
        total_debt = simulation_input.total_debt
        avg_interest_rate = sum(debt.interest_rate for debt in simulation_input.medical_debts) / len(simulation_input.medical_debts)
        monthly_rate = avg_interest_rate / 100 / 12
        
        if monthly_rate > 0:
            # Use loan payoff formula: n = -log(1 - (P * r) / M) / log(1 + r)
            # Where P = principal, r = monthly rate, M = monthly payment
            if monthly_payment <= total_debt * monthly_rate:
                # Payment is too small to cover interest - debt will never be paid off
                return 9999  # Return 9999 to indicate "80+ years"
            else:
                import math
                # Correct formula: n = -log(1 - (P * r) / M) / log(1 + r)
                numerator = 1 - (total_debt * monthly_rate) / monthly_payment
                if numerator <= 0:
                    return 9999  # Will never be paid off
                months = -math.log(numerator) / math.log(1 + monthly_rate)
                return max(1, min(int(months), 9999))  # Cap at 9999 months
        else:
            # For 0% interest, simple division
            months = total_debt / monthly_payment
            return max(1, int(months))  # No cap - brutally honest
    
    def _compare_plans(self, easy_plan: Dict, middle_plan: Dict, hardcore_plan: Dict, simulation_input: MedicalSimulationInput) -> Dict[str, Any]:
        """Compare the three plans"""
        return {
            'monthly_payment_range': {
                'min': easy_plan['monthly_payment'],
                'max': hardcore_plan['monthly_payment']
            },
            'time_range': {
                'min_months': hardcore_plan['estimated_months'],
                'max_months': easy_plan['estimated_months']
            },
            'difficulty_levels': [easy_plan['difficulty'], middle_plan['difficulty'], hardcore_plan['difficulty']],
            'recommended_plan': self._recommend_plan(easy_plan, middle_plan, hardcore_plan, simulation_input)
        }
    
    def _recommend_plan(self, easy_plan: Dict, middle_plan: Dict, hardcore_plan: Dict, simulation_input: MedicalSimulationInput) -> str:
        """Recommend the best plan based on user's situation"""
        # Simple recommendation logic - can be enhanced
        if hardcore_plan['additional_income_needed'] < simulation_input.financial_data.monthly_income * 0.3:
            return 'hardcore_plan'
        elif middle_plan['additional_income_needed'] < simulation_input.financial_data.monthly_income * 0.15:
            return 'middle_plan'
        else:
            return 'easy_plan'
    
    def _calculate_debt_free_date(self, months: int) -> str:
        """Calculate debt-free date"""
        future_date = datetime.now() + timedelta(days=months * 30)
        return future_date.strftime('%B %Y')
    
    def _fallback_simulation(self, simulation_input: MedicalSimulationInput) -> Dict[str, Any]:
        """Fallback simulation if Nessie API fails"""
        # Simple calculation without API integration
        total_debt = simulation_input.total_debt
        avg_interest_rate = sum(debt.interest_rate for debt in simulation_input.medical_debts) / len(simulation_input.medical_debts)
        monthly_payment = simulation_input.total_minimum_payments
        
        # Simple payoff calculation
        monthly_rate = avg_interest_rate / 100 / 12
        if monthly_rate > 0:
            months = -1 * (1 / monthly_rate) * (1 - (total_debt * monthly_rate) / monthly_payment)
            months = max(1, int(months))
        else:
            months = int(total_debt / monthly_payment)
        
        return {
            'months_to_payoff': months,
            'total_interest_paid': round(total_debt * monthly_rate * months, 2),
            'debt_free_date': self._calculate_debt_free_date(months),
            'note': 'Fallback calculation - Nessie API unavailable'
        }

# Create singleton instance
medical_simulation_service = MedicalSimulationService()
