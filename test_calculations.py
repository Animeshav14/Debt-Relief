#!/usr/bin/env python3
"""
Test script to verify frontend calculations match backend calculations
"""

import requests
import json

def test_calculation_accuracy():
    """Test that frontend calculations match backend exactly"""
    
    # Test data
    test_data = {
        "financialData": {
            "monthly_income": 5000,
            "current_balance": 2000,
            "monthly_expenses": 3000
        },
        "debt": {
            "name": "Credit Card",
            "balance": 5000,
            "interest_rate": 18.5,
            "minimum_payment": 150,
            "type": "credit_card"
        },
        "paymentAmount": 200
    }
    
    try:
        # Call the API
        response = requests.post('http://localhost:5001/api/simulate', 
                               json=test_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            
            print("✅ Backend API call successful")
            print(f"📊 Results Summary:")
            print(f"   Months to payoff: {data['months_to_payoff']}")
            print(f"   Total interest paid: ${data['total_interest_paid']:,.2f}")
            print(f"   Total amount paid: ${data['total_amount_paid']:,.2f}")
            print(f"   Debt-free date: {data['debt_free_date']}")
            
            # Verify calculations manually
            print(f"\n🧮 Manual Calculation Verification:")
            
            # Monthly rate calculation
            monthly_rate = 18.5 / 100 / 12
            print(f"   Monthly interest rate: {monthly_rate:.6f} ({monthly_rate * 100:.4f}%)")
            
            # First month calculation
            balance = 5000
            interest_charge = balance * monthly_rate
            new_balance = balance + interest_charge
            payment = min(200, new_balance)
            principal_paid = payment - interest_charge
            ending_balance = new_balance - payment
            
            print(f"   Month 1 calculation:")
            print(f"     Starting balance: ${balance:,.2f}")
            print(f"     Interest charge: ${balance:,.2f} × {monthly_rate:.6f} = ${interest_charge:.2f}")
            print(f"     New balance: ${balance:,.2f} + ${interest_charge:.2f} = ${new_balance:.2f}")
            print(f"     Payment made: min($200, ${new_balance:.2f}) = ${payment:.2f}")
            print(f"     Principal paid: ${payment:.2f} - ${interest_charge:.2f} = ${principal_paid:.2f}")
            print(f"     Ending balance: ${new_balance:.2f} - ${payment:.2f} = ${ending_balance:.2f}")
            
            # Check against API result
            first_month = data['timeline'][0]
            print(f"\n   API Result for Month 1:")
            print(f"     Interest charged: ${first_month['interest_charged']:.2f}")
            print(f"     Payment made: ${first_month['payment_made']:.2f}")
            print(f"     Principal paid: ${first_month['principal_paid']:.2f}")
            print(f"     Ending balance: ${first_month['balance']:.2f}")
            
            # Verify they match
            if abs(interest_charge - first_month['interest_charged']) < 0.01:
                print("   ✅ Interest calculation matches!")
            else:
                print("   ❌ Interest calculation mismatch!")
                
            if abs(principal_paid - first_month['principal_paid']) < 0.01:
                print("   ✅ Principal calculation matches!")
            else:
                print("   ❌ Principal calculation mismatch!")
            
            # Show timeline summary
            print(f"\n📅 Timeline Summary (first 5 months):")
            for i, month in enumerate(data['timeline'][:5]):
                print(f"   Month {month['month']}: Balance ${month['balance']:,.2f}, "
                      f"Interest ${month['interest_charged']:.2f}, "
                      f"Payment ${month['payment_made']:.2f}")
            
            print(f"\n🎯 Frontend Test Instructions:")
            print(f"   1. Open frontend.html in your browser")
            print(f"   2. Use the pre-filled values (or enter the test data above)")
            print(f"   3. Click 'Calculate Debt Payoff'")
            print(f"   4. Verify the calculations match the results shown above")
            print(f"   5. Check the month-by-month timeline for detailed math")
            
            return True
            
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 5001")
        print("   Run: cd Backend && python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Debt Relief Calculator Backend")
    print("=" * 50)
    test_calculation_accuracy()
