# Purpose: Main application file for the Flask backend server.

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import routes
from routes.simulation import simulation_bp
from routes.medical_simulation import medical_simulation_bp

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Register blueprints (routes)
app.register_blueprint(simulation_bp, url_prefix='/api')
app.register_blueprint(medical_simulation_bp, url_prefix='/api')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'OK', 'message': 'Server is running'}, 200

# Error handler
@app.errorhandler(Exception)
def handle_error(error):
    return {'error': str(error)}, 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, port=port, host='0.0.0.0')