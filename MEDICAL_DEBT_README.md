# Medical Debt Relief Simulator

A comprehensive medical debt simulation system built with Capitol One's Nessie API integration, designed to help users understand their current debt trajectory and explore different payoff strategies.

## 🏥 Features

### 1. **Comprehensive Input System**
- **Financial Information**: Monthly income, current savings, monthly expenses
- **Medical Debt Details**: Multiple medical debts with provider information, service dates, insurance coverage
- **Goal Setting**: Target payoff dates, monthly payment limits, priority levels
- **Income Sources**: Track multiple income streams for earning plans

### 2. **Current Trajectory Simulation**
- Uses Capitol One's Nessie API to create virtual accounts and simulate payments
- Fallback calculation system when API is unavailable
- Month-by-month breakdown of payments, interest, and remaining balance
- Visual timeline of debt payoff progress

### 3. **Three Personalized Payoff Plans**

#### 🐌 **Easy Long-term Plan**
- 20% increase above minimum payments
- Manageable lifestyle impact
- Recommendations for automatic payments and payment plans

#### ⚖️ **Balanced Plan**
- 50% increase above minimum payments
- Moderate lifestyle adjustments
- Suggestions for side hustles and expense reduction

#### 🚀 **Hardcore Earning Plan**
- Aggressive payments targeting 2-year payoff
- Significant income increase requirements
- Comprehensive recommendations for debt elimination

### 4. **Smart Recommendations**
- Payment plan opportunities with providers
- Insurance coverage optimization
- Financial assistance program applications
- Debt consolidation and settlement strategies
- Side hustle and income increase suggestions

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Flask
- Capitol One Nessie API key (optional - system works with fallback calculations)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Debt-Relief
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   NESSIE_API_KEY=your_nessie_api_key_here
   PORT=5001
   ```

4. **Start the backend server**
   ```bash
   cd Backend
   python app.py
   ```

5. **Open the frontend**
   - Open `medical_debt_frontend.html` in your browser
   - Or serve it through a local web server

## 📊 API Endpoints

### Medical Debt Simulation
- **POST** `/api/medical/simulate` - Complete simulation with all three plans
- **POST** `/api/medical/current-trajectory` - Current trajectory only
- **POST** `/api/medical/calculate-earnings` - Required earnings calculation
- **GET** `/api/medical/test` - Health check

### Example Request
```json
{
  "financialData": {
    "monthly_income": 5000,
    "current_balance": 2000,
    "monthly_expenses": 3500
  },
  "medicalDebts": [
    {
      "name": "Hospital Bill - Emergency Room",
      "balance": 8000,
      "interest_rate": 0,
      "minimum_payment": 200,
      "provider_name": "General Hospital",
      "service_date": "2024-01-15",
      "insurance_coverage": 0,
      "payment_plan_available": true
    }
  ],
  "goals": {
    "target_payoff_months": 24,
    "monthly_payment_limit": 600,
    "priority_level": "medium"
  }
}
```

## 🏗️ Architecture

### Backend Structure
```
Backend/
├── models/
│   ├── medical_debt_info.py      # Medical debt specific models
│   ├── medical_simulation_input.py # Input validation and processing
│   └── user_financial_data.py    # Financial data models
├── services/
│   ├── medical_simulation_service.py # Core simulation logic
│   └── nessie_service.py         # Nessie API integration
├── routes/
│   └── medical_simulation.py     # API endpoints
└── utils/
    └── validation.py             # Input validation
```

### Key Components

#### MedicalDebtInfo
- Extends base debt model with medical-specific fields
- Tracks provider information, service dates, insurance coverage
- Calculates payment plan benefits and insurance discounts

#### MedicalSimulationService
- Integrates with Nessie API for realistic simulations
- Generates three different payoff strategies
- Provides fallback calculations when API unavailable
- Calculates required earnings and income increases

#### Frontend Interface
- Responsive design with modern UI
- Dynamic debt entry forms
- Real-time plan comparison
- Visual timeline and metrics display

## 🔧 Configuration

### Nessie API Integration
The system integrates with Capitol One's Nessie API for realistic debt simulations:

1. **Create Customer**: Virtual customer in Nessie system
2. **Create Accounts**: One account per medical debt
3. **Simulate Payments**: Track payments and interest over time
4. **Fallback Mode**: Mathematical calculations when API unavailable

### Environment Variables
```bash
NESSIE_API_KEY=your_api_key_here  # Get from https://api.nessieisreal.com/
PORT=5001                         # Backend server port
FLASK_ENV=development             # Flask environment
```

## 📈 Sample Results

The system provides comprehensive analysis including:

- **Current Trajectory**: Months to payoff with minimum payments
- **Plan Comparison**: Side-by-side comparison of all three plans
- **Required Earnings**: Additional income needed for each plan
- **Interest Savings**: Potential savings from different strategies
- **Recommendations**: Actionable steps for debt elimination

## 🛠️ Development

### Adding New Features
1. **New Debt Types**: Extend `MedicalDebtInfo` class
2. **Additional Plans**: Add methods to `MedicalSimulationService`
3. **New Calculations**: Extend simulation logic in service layer
4. **Frontend Updates**: Modify `medical_debt_frontend.html`

### Testing
```bash
# Test individual components
python -c "from Backend.services.medical_simulation_service import medical_simulation_service; print('Import successful')"

# Test API endpoints
curl -X GET http://localhost:5001/api/medical/test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the API documentation
2. Review the example requests
3. Test with the provided sample data
4. Check server logs for detailed error messages

## 🔮 Future Enhancements

- **Debt Consolidation Calculator**: Compare consolidation options
- **Insurance Optimization**: Find best insurance coverage strategies
- **Payment Plan Negotiation**: Tools for negotiating with providers
- **Financial Assistance**: Integration with assistance program databases
- **Mobile App**: Native mobile application
- **Advanced Analytics**: Detailed financial health metrics

