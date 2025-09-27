# Debt Relief Calculator - Frontend Test Interface

This is a barebones frontend interface for testing the debt relief calculation backend. It provides a comprehensive view of all calculations and mathematical processes.

## Features

### Input Forms
- **Financial Data**: Monthly income, current bank balance, monthly expenses
- **Debt Information**: Debt name, balance, interest rate (APR), minimum payment
- **Payment Amount**: Your proposed monthly payment amount

### Detailed Calculations Display
- **Step-by-step math**: Shows exactly how each calculation is performed
- **Monthly interest rate calculation**: APR ÷ 100 ÷ 12
- **Monthly process breakdown**: Interest charge, payment application, principal calculation
- **Summary metrics**: Total interest, total amount paid, payoff timeline

### Month-by-Month Timeline
- **Complete timeline table**: Shows every month of the payoff process
- **Detailed calculations**: For each month, shows:
  - Starting balance
  - Interest charged (with formula)
  - Payment made
  - Principal paid
  - Ending balance
  - Step-by-step math for that month

### Visual Features
- **Summary cards**: Key metrics at a glance
- **Color-coded timeline**: Final month highlighted
- **Responsive design**: Works on desktop and mobile
- **Error handling**: Clear error messages for validation issues

## How to Use

1. **Start the Backend**: Make sure the Flask backend is running on port 5001
   ```bash
   cd Backend
   python app.py
   ```

2. **Open the Frontend**: Open `frontend.html` in your web browser

3. **Enter Test Data**: The form comes pre-filled with sample data:
   - Monthly Income: $5,000
   - Current Balance: $2,000
   - Monthly Expenses: $3,000
   - Debt Balance: $5,000
   - Interest Rate: 18.5% APR
   - Minimum Payment: $150
   - Your Payment: $200

4. **Click Calculate**: The interface will show:
   - Summary results
   - Detailed calculation steps
   - Complete month-by-month timeline

## What You'll See

### Calculation Details Section
- Monthly interest rate calculation
- Simulation overview
- Monthly calculation process explanation
- Summary results with interest savings

### Timeline Table
Each row shows:
- Month number
- Starting balance
- Interest charged (with exact formula)
- Payment made
- Principal paid
- Ending balance
- Step-by-step math for that month

## Testing Different Scenarios

Try these test cases to see different calculations:

1. **High Interest, Low Payment**:
   - Balance: $10,000
   - Interest: 25%
   - Payment: $200

2. **Low Interest, High Payment**:
   - Balance: $5,000
   - Interest: 5%
   - Payment: $500

3. **Minimum Payment Only**:
   - Use the minimum payment as your payment amount

4. **Edge Case - Payment = Balance**:
   - Set payment amount equal to debt balance

## Backend Integration

The frontend calls the `/api/simulate` endpoint with this structure:
```json
{
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
```

## Error Handling

The interface handles:
- Backend connection errors
- Validation errors from the API
- Network timeouts
- Invalid input data

All errors are displayed clearly to help with debugging.
