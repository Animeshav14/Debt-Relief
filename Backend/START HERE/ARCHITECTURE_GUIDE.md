# 🏗️ Debt Relief Project - Technical Architecture Guide

This guide explains the technical architecture of the Debt Relief project in detail. It's designed to help developers understand how all the pieces fit together.

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Frontend Architecture](#frontend-architecture)
3. [Backend Architecture](#backend-architecture)
4. [Data Flow](#data-flow)
5. [API Design](#api-design)
6. [File Organization](#file-organization)
7. [Key Design Patterns](#key-design-patterns)
8. [Integration Points](#integration-points)

---

## 🎯 System Overview

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                     │
├─────────────────┬─────────────────┬─────────────────────────────┤
│  Basic Debt     │  Medical Debt   │  Typeform Questionnaire     │
│  Calculator     │  Simulator      │  Interface                  │
│  (frontend.html)│  (medical_*.html)│  (typeform_*.html)          │
└─────────────────┴─────────────────┴─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API LAYER                                │
├─────────────────┬───────────────────────────────────────────────┤
│  Basic Debt     │  Medical Debt                                 │
│  Routes         │  Routes                                       │
│  (/api/simulate)│  (/api/medical/*)                            │
└─────────────────┴───────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                       │
├─────────────────┬─────────────────┬─────────────────────────────┤
│  Simulation     │  Medical        │  Validation                 │
│  Service        │  Simulation     │  Utils                      │
│                 │  Service        │                             │
└─────────────────┴─────────────────┴─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
├─────────────────┬─────────────────┬─────────────────────────────┤
│  Data Models    │  External APIs  │  Configuration              │
│  (Pydantic)     │  (Nessie)       │  (Environment)              │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

---

## 🖥️ Frontend Architecture

### Technology Stack
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with flexbox/grid
- **Vanilla JavaScript**: No frameworks for simplicity
- **Fetch API**: For backend communication

### Frontend Components

#### 1. Basic Debt Calculator (`frontend.html`)
```html
<!-- Structure -->
<div class="container">
  <div class="header">          <!-- Title and description -->
  <div class="form-section">    <!-- Input form -->
  <div class="results-section"> <!-- Results display -->
</div>
```

**Key Features:**
- Single debt input form
- Real-time calculation display
- Step-by-step calculation breakdown
- Responsive design

#### 2. Medical Debt Simulator (`medical_debt_frontend.html`)
```html
<!-- Structure -->
<div class="container">
  <div class="header">                    <!-- Title -->
  <div class="input-sections">            <!-- Multiple input forms -->
    <div class="financial-info">         <!-- User financial data -->
    <div class="medical-debts">          <!-- Multiple debt entries -->
    <div class="goals">                  <!-- User goals -->
  </div>
  <div class="results-section">          <!-- Three strategy results -->
</div>
```

**Key Features:**
- Dynamic debt entry (add/remove debts)
- Three strategy comparison
- Visual timeline display
- Advanced recommendations

#### 3. Typeform Interface (`typeform_frontend.html`)
```html
<!-- Structure -->
<div class="typeform-container">
  <div class="progress-bar">     <!-- Step indicator -->
  <div class="question-section"> <!-- Current question -->
  <div class="navigation">       <!-- Next/Previous buttons -->
</div>
```

**Key Features:**
- Step-by-step questionnaire
- Progress tracking
- Conditional logic
- Mobile-optimized

### Frontend Design Patterns

#### 1. **Component-Based Structure**
Each major section is a self-contained component:
```javascript
// Example: Results display component
function displayResults(data) {
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = `
    <h3>Debt Payoff Results</h3>
    <p>Months to payoff: ${data.months_to_payoff}</p>
    <p>Total interest: $${data.total_interest_paid}</p>
  `;
}
```

#### 2. **Event-Driven Architecture**
User interactions trigger specific functions:
```javascript
// Example: Form submission
document.getElementById('calculate-btn').addEventListener('click', function() {
  const formData = collectFormData();
  sendToBackend(formData);
});
```

#### 3. **Progressive Enhancement**
Basic functionality works without JavaScript, enhanced with JS:
```html
<!-- Basic form works without JS -->
<form action="/api/simulate" method="POST">
  <!-- Enhanced with JavaScript for better UX -->
</form>
```

---

## 🐍 Backend Architecture

### Technology Stack
- **Python 3.8+**: Core language
- **Flask**: Web framework
- **Pydantic**: Data validation
- **Requests**: HTTP client for external APIs

### Backend Structure

#### 1. **Application Entry Point** (`app.py`)
```python
# Main Flask application
app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Register blueprints (route modules)
app.register_blueprint(simulation_bp, url_prefix='/api')
app.register_blueprint(medical_simulation_bp, url_prefix='/api')
```

**Responsibilities:**
- Initialize Flask application
- Configure CORS for frontend communication
- Register route blueprints
- Handle global error responses

#### 2. **Route Layer** (`routes/`)
```python
# Example: Basic simulation route
@simulation_bp.route('/simulate', methods=['POST'])
def simulate_debt():
    try:
        # Validate input
        data = request.get_json()
        simulation_input = SimulationInput(**data)
        
        # Call service
        result = simulation_service.run_simulation(simulation_input)
        
        # Return response
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

**Responsibilities:**
- Handle HTTP requests/responses
- Validate input data
- Call appropriate services
- Return JSON responses
- Handle errors gracefully

#### 3. **Service Layer** (`services/`)
```python
# Example: Simulation service
class SimulationService:
    def simulate_debt_payoff(self, initial_balance, apr, monthly_payment):
        timeline = []
        balance = initial_balance
        
        while balance > 0:
            # Calculate interest
            interest = self.calculate_monthly_interest(balance, apr)
            balance += interest
            
            # Apply payment
            payment = min(monthly_payment, balance)
            balance -= payment
            
            # Record month data
            timeline.append({
                'month': month,
                'balance': balance,
                'interest_charged': interest,
                'payment_made': payment
            })
        
        return {'timeline': timeline, 'months_to_payoff': len(timeline)}
```

**Responsibilities:**
- Implement business logic
- Perform calculations
- Integrate with external services
- Return structured data

#### 4. **Data Models** (`models/`)
```python
# Example: Debt information model
class DebtInfo(BaseModel):
    name: str
    balance: float
    interest_rate: float
    minimum_payment: float
    
    @validator('balance')
    def balance_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Balance must be positive')
        return v
```

**Responsibilities:**
- Define data structure
- Validate input data
- Provide type safety
- Generate clear error messages

---

## 🔄 Data Flow

### 1. **User Input Flow**
```
User Types Data → Frontend Validation → HTTP Request → 
Backend Validation → Data Model Creation → Service Processing
```

### 2. **Calculation Flow**
```
Input Data → Service Layer → Business Logic → 
External API (if needed) → Results Processing → Response
```

### 3. **Error Handling Flow**
```
Error Occurs → Try/Catch Block → Error Classification → 
User-Friendly Message → Frontend Display
```

### 4. **Complete Request Flow**
```
1. User fills form in frontend
2. JavaScript collects form data
3. Fetch API sends POST request to backend
4. Flask receives request in route handler
5. Route validates data using Pydantic models
6. Route calls appropriate service method
7. Service performs calculations
8. Service returns structured results
9. Route returns JSON response
10. Frontend receives response and updates UI
```

---

## 🌐 API Design

### RESTful API Principles
- **GET**: Retrieve data (health checks, test endpoints)
- **POST**: Create/process data (simulations, calculations)
- **Consistent URL structure**: `/api/{feature}/{action}`
- **JSON request/response format**
- **HTTP status codes**: 200 (success), 400 (bad request), 500 (server error)

### API Endpoints

#### Basic Debt Simulation
```
POST /api/simulate
- Input: {debt: {...}, payment_amount: number}
- Output: {months_to_payoff, total_interest_paid, timeline: [...]}

GET /api/health
- Output: {status: "OK", message: "Server is running"}
```

#### Medical Debt Simulation
```
POST /api/medical/simulate
- Input: {financialData: {...}, medicalDebts: [...], goals: {...}}
- Output: {current_trajectory: {...}, plans: {...}, recommendations: [...]}

POST /api/medical/current-trajectory
- Input: Same as above
- Output: {current_trajectory: {...}}

POST /api/medical/calculate-earnings
- Input: Same as above
- Output: {required_earnings: {...}}
```

### API Response Format
```json
{
  "success": true,
  "data": {
    // Actual response data
  },
  "error": null,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 📁 File Organization

### Directory Structure Principles
1. **Separation of Concerns**: Each directory has a specific purpose
2. **Logical Grouping**: Related files are grouped together
3. **Scalability**: Easy to add new features without restructuring
4. **Clarity**: Directory names clearly indicate contents

### File Naming Conventions
- **Snake_case**: For Python files (`simulation_service.py`)
- **Kebab-case**: For HTML files (`medical-debt-frontend.html`)
- **Descriptive names**: File names explain their purpose
- **Consistent patterns**: Similar files follow same naming

### Import Organization
```python
# Standard library imports
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Third-party imports
from flask import Flask, request, jsonify
from pydantic import BaseModel, validator

# Local imports
from models.debt_info import DebtInfo
from services.simulation_service import simulation_service
```

---

## 🎨 Key Design Patterns

### 1. **MVC (Model-View-Controller)**
- **Model**: Data models in `models/` directory
- **View**: Frontend HTML files
- **Controller**: Route handlers in `routes/` directory

### 2. **Service Layer Pattern**
- Business logic separated from route handlers
- Services can be tested independently
- Easy to modify business rules without changing API

### 3. **Repository Pattern** (for external APIs)
- `nessie_service.py` abstracts external API calls
- Easy to mock for testing
- Can switch APIs without changing business logic

### 4. **Factory Pattern** (for simulations)
- Different simulation strategies created by factory
- Easy to add new simulation types
- Consistent interface for all simulations

### 5. **Validation Pattern**
- Input validation at multiple layers
- Pydantic models for data validation
- Custom validators for business rules

---

## 🔌 Integration Points

### 1. **Frontend ↔ Backend**
- **Protocol**: HTTP/HTTPS
- **Format**: JSON
- **Method**: RESTful API calls
- **Error Handling**: Try/catch with user-friendly messages

### 2. **Backend ↔ External APIs**
- **Nessie API**: Banking simulation
- **Protocol**: HTTPS
- **Authentication**: API key
- **Fallback**: Mathematical calculations when API unavailable

### 3. **Data Validation**
- **Frontend**: Basic validation (required fields, number ranges)
- **Backend**: Comprehensive validation (business rules, data types)
- **Models**: Type safety and constraint validation

---

## 🚀 Scalability Considerations

### Current Architecture Strengths
- **Stateless**: No server-side session storage
- **Modular**: Easy to add new features
- **Testable**: Clear separation of concerns
- **Simple**: Easy for new developers to understand

### Future Scalability Options
- **Database**: Add PostgreSQL for data persistence
- **Caching**: Redis for frequently accessed calculations
- **Load Balancing**: Multiple server instances
- **Microservices**: Split into separate services
- **API Gateway**: Centralized API management

---

## 🔧 Development Guidelines

### Code Organization
1. **One responsibility per file**
2. **Clear function and variable names**
3. **Comprehensive comments for complex logic**
4. **Consistent formatting and style**

### Error Handling
1. **Validate input at every layer**
2. **Provide meaningful error messages**
3. **Log errors for debugging**
4. **Graceful degradation when possible**

### Testing Strategy
1. **Unit tests for business logic**
2. **Integration tests for API endpoints**
3. **Frontend testing for user interactions**
4. **End-to-end testing for complete workflows**

This architecture provides a solid foundation for the Debt Relief project while remaining simple enough for new developers to understand and contribute to effectively.
