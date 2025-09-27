from datetime import datetime, timedelta

class SimulationService:
    """Handles debt payoff simulation calculations"""
    
    def calculate_monthly_interest(self, balance, apr):
        """Calculates interest charge for one month"""
        monthly_rate = apr / 100 / 12
        return balance * monthly_rate
    
    def simulate_debt_payoff(self, initial_balance, apr, monthly_payment, max_months=360):
        """
        Simulates month-by-month debt payoff
        
        Args:
            initial_balance: Starting debt balance
            apr: Annual Percentage Rate
            monthly_payment: Amount paid each month
            max_months: Maximum months to simulate (default 30 years)
        
        Returns:
            Dictionary with simulation results and timeline
        """
        timeline = []
        balance = initial_balance
        total_interest_paid = 0
        month = 0
        
        while balance > 0 and month < max_months:
            month += 1
            
            # Calculate interest for this month
            interest_charge = self.calculate_monthly_interest(balance, apr)
            
            # Add interest to balance
            balance += interest_charge
            
            # Apply payment (but not more than the balance)
            payment = min(monthly_payment, balance)
            balance -= payment
            
            total_interest_paid += interest_charge
            
            # Record this month's data
            timeline.append({
                'month': month,
                'balance': round(max(0, balance), 2),
                'interest_charged': round(interest_charge, 2),
                'payment_made': round(payment, 2),
                'principal_paid': round(payment - interest_charge, 2)
            })
            
            # If balance is essentially zero, break
            if balance < 0.01:
                balance = 0
                break
        
        return {
            'months_to_payoff': month,
            'total_interest_paid': round(total_interest_paid, 2),
            'total_amount_paid': round(initial_balance + total_interest_paid, 2),
            'timeline': timeline,
            'debt_free_date': self.calculate_debt_free_date(month)
        }
    
    def calculate_debt_free_date(self, months_from_now):
        """Calculates the debt-free date"""
        future_date = datetime.now() + timedelta(days=months_from_now * 30)
        return future_date.strftime('%B %Y')
    
    def run_simulation(self, simulation_input):
        """
        Main entry point for running a simulation
        
        Args:
            simulation_input: SimulationInput object with all data
        
        Returns:
            Simulation results dictionary
        """
        debt = simulation_input.debt
        payment_amount = simulation_input.payment_amount
        
        return self.simulate_debt_payoff(
            initial_balance=debt.balance,
            apr=debt.interest_rate,
            monthly_payment=payment_amount
        )

# Create a singleton instance
simulation_service = SimulationService()