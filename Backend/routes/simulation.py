from flask import Blueprint, request, jsonify
from models.simulation_input import SimulationInput
from services.simulation_service import simulation_service
from utils.validation import validate_simulation_request

# Create blueprint
simulation_bp = Blueprint('simulation', __name__)

@simulation_bp.route('/simulate', methods=['POST'])
def simulate():
    """
    POST /api/simulate
    
    Runs a debt payoff simulation
    
    Expected JSON body:
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
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate request structure
        validation = validate_simulation_request(data)
        if not validation['valid']:
            return jsonify({'error': validation['error']}), 400
        
        # Create simulation input object
        simulation_input = SimulationInput(
            financial_data=data['financialData'],
            debt=data['debt'],
            payment_amount=data['paymentAmount']
        )
        
        # Validate business rules
        simulation_input.validate()
        
        # Run the simulation
        results = simulation_service.run_simulation(simulation_input)
        
        # Return results
        return jsonify({
            'success': True,
            'data': results
        }), 200
    
    except ValueError as e:
        # Validation errors
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        # Unexpected errors
        print(f"Simulation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred'
        }), 500

@simulation_bp.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify routes are working"""
    return jsonify({
        'message': 'Simulation route is working!',
        'endpoints': {
            'simulate': '/api/simulate (POST)'
        }
    }), 200