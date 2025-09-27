from flask import Blueprint, request, jsonify
from models.medical_simulation_input import MedicalSimulationInput
from services.medical_simulation_service import medical_simulation_service
from utils.validation import validate_medical_simulation_request

# Create blueprint
medical_simulation_bp = Blueprint('medical_simulation', __name__)

@medical_simulation_bp.route('/medical/simulate', methods=['POST'])
def simulate_medical_debt():
    """
    POST /api/medical/simulate
    
    Runs a comprehensive medical debt payoff simulation
    
    Expected JSON body:
    {
        "financialData": {
            "monthly_income": 5000,
            "current_balance": 2000,
            "monthly_expenses": 3000
        },
        "medicalDebts": [
            {
                "name": "Hospital Bill - Emergency Room",
                "balance": 5000,
                "interest_rate": 0,
                "minimum_payment": 200,
                "provider_name": "General Hospital",
                "service_date": "2024-01-15",
                "insurance_coverage": 0,
                "payment_plan_available": true
            }
        ],
        "goals": {
            "target_payoff_date": "2025-12-31",
            "target_payoff_months": 24,
            "monthly_payment_limit": 500,
            "priority_level": "high"
        },
        "currentIncomeSources": [
            {
                "source": "Primary Job",
                "amount": 4000,
                "frequency": "monthly"
            }
        ]
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate request structure
        validation = validate_medical_simulation_request(data)
        if not validation['valid']:
            return jsonify({'error': validation['error']}), 400
        
        # Create simulation input object
        simulation_input = MedicalSimulationInput(
            financial_data=data['financialData'],
            medical_debts=data['medicalDebts'],
            goals=data['goals'],
            current_income_sources=data.get('currentIncomeSources', [])
        )
        
        # Validate business rules
        simulation_input.validate()
        
        # Run the comprehensive simulation
        results = medical_simulation_service.generate_payoff_plans(simulation_input)
        
        # Add input summary to results
        results['input_summary'] = simulation_input.to_dict()
        
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
        print(f"Medical simulation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred during simulation'
        }), 500

@medical_simulation_bp.route('/medical/current-trajectory', methods=['POST'])
def simulate_current_trajectory():
    """
    POST /api/medical/current-trajectory
    
    Simulates current trajectory using Nessie API with detailed analysis
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create simulation input
        simulation_input = MedicalSimulationInput(
            financial_data=data['financialData'],
            medical_debts=data['medicalDebts'],
            goals=data.get('goals', {}),
            current_income_sources=data.get('currentIncomeSources', [])
        )
        
        # Validate
        simulation_input.validate()
        
        # Get detailed current trajectory timeline
        trajectory_data = medical_simulation_service.calculate_current_trajectory_timeline(simulation_input)
        
        # Get additional analysis
        additional_analysis = medical_simulation_service.get_current_trajectory_only(simulation_input)
        
        # Combine results
        results = {
            'trajectory_timeline': trajectory_data,
            'debt_summary': simulation_input.get_debt_summary(),
            'insurance_opportunities': additional_analysis['insurance_opportunities'],
            'payment_plan_opportunities': additional_analysis['payment_plan_opportunities']
        }
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@medical_simulation_bp.route('/medical/calculate-earnings', methods=['POST'])
def calculate_required_earnings():
    """
    POST /api/medical/calculate-earnings
    
    Calculates required earnings to meet goals
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        simulation_input = MedicalSimulationInput(
            financial_data=data['financialData'],
            medical_debts=data['medicalDebts'],
            goals=data['goals'],
            current_income_sources=data.get('currentIncomeSources', [])
        )
        
        simulation_input.validate()
        
        target_months = data.get('target_months', 24)
        results = medical_simulation_service.calculate_required_earnings(simulation_input, target_months)
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@medical_simulation_bp.route('/medical/test', methods=['GET'])
def test_medical():
    """Test endpoint to verify medical simulation routes are working"""
    return jsonify({
        'message': 'Medical simulation routes are working!',
        'endpoints': {
            'simulate': '/api/medical/simulate (POST)',
            'current_trajectory': '/api/medical/current-trajectory (POST)',
            'calculate_earnings': '/api/medical/calculate-earnings (POST)'
        }
    }), 200
