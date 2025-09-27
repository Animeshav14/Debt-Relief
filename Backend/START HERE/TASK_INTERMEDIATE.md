# 🎯 Intermediate Developer Tasks - Debt Relief Project

**Welcome to the intermediate level!** These tasks are designed for developers who have some programming experience and want to work on more complex features. You'll be working with both frontend and backend code.

## 📋 Your Mission
Complete these tasks to add significant new features to the project. Each task builds your understanding of the full-stack architecture.

---

## 🚀 Task 1: Add a Debt Comparison Tool

**Difficulty**: ⭐⭐⭐ (Medium)  
**Time**: 2-3 hours  
**Files to modify**: `frontend.html`, `Backend/routes/simulation.py`, `Backend/services/simulation_service.py`

### What You'll Do
Create a feature that lets users compare two different debt payoff strategies side-by-side.

### Step-by-Step Instructions

#### Frontend Changes (`frontend.html`)

1. **Add comparison section** after the main form:
   ```html
   <div class="comparison-section">
       <h2>Compare Two Strategies</h2>
       <div class="comparison-form">
           <div class="strategy-a">
               <h3>Strategy A</h3>
               <input type="number" id="strategy-a-payment" placeholder="Monthly Payment A">
           </div>
           <div class="strategy-b">
               <h3>Strategy B</h3>
               <input type="number" id="strategy-b-payment" placeholder="Monthly Payment B">
           </div>
           <button onclick="compareStrategies()" class="compare-btn">Compare Strategies</button>
       </div>
       <div id="comparison-results" class="comparison-results"></div>
   </div>
   ```

2. **Add CSS styling**:
   ```css
   .comparison-section {
       background: white;
       padding: 30px;
       border-radius: 10px;
       margin: 20px 0;
       box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
   }
   
   .comparison-form {
       display: flex;
       gap: 20px;
       margin: 20px 0;
   }
   
   .strategy-a, .strategy-b {
       flex: 1;
       padding: 20px;
       border: 2px solid #e9ecef;
       border-radius: 8px;
   }
   
   .compare-btn {
       background: #17a2b8;
       color: white;
       border: none;
       padding: 15px 30px;
       border-radius: 5px;
       cursor: pointer;
       font-size: 16px;
   }
   
   .comparison-results {
       display: grid;
       grid-template-columns: 1fr 1fr;
       gap: 20px;
       margin-top: 20px;
   }
   ```

3. **Add JavaScript function**:
   ```javascript
   async function compareStrategies() {
       const debtAmount = parseFloat(document.getElementById('debt-amount').value);
       const interestRate = parseFloat(document.getElementById('interest-rate').value);
       const paymentA = parseFloat(document.getElementById('strategy-a-payment').value);
       const paymentB = parseFloat(document.getElementById('strategy-b-payment').value);
       
       if (!validateComparisonInputs(debtAmount, interestRate, paymentA, paymentB)) {
           return;
       }
       
       try {
           const [resultA, resultB] = await Promise.all([
               calculateStrategy(debtAmount, interestRate, paymentA),
               calculateStrategy(debtAmount, interestRate, paymentB)
           ]);
           
           displayComparisonResults(resultA, resultB);
       } catch (error) {
           alert('Error comparing strategies: ' + error.message);
       }
   }
   
   async function calculateStrategy(debtAmount, interestRate, monthlyPayment) {
       const response = await fetch('/api/simulate', {
           method: 'POST',
           headers: {
               'Content-Type': 'application/json',
           },
           body: JSON.stringify({
               debt: {
                   name: 'Debt',
                   balance: debtAmount,
                   interest_rate: interestRate,
                   minimum_payment: monthlyPayment
               },
               payment_amount: monthlyPayment
           })
       });
       
       if (!response.ok) {
           throw new Error('Failed to calculate strategy');
       }
       
       return await response.json();
   }
   
   function displayComparisonResults(resultA, resultB) {
       const resultsDiv = document.getElementById('comparison-results');
       resultsDiv.innerHTML = `
           <div class="strategy-result">
               <h3>Strategy A Results</h3>
               <div class="result-stats">
                   <div class="stat">
                       <span class="label">Months to Payoff:</span>
                       <span class="value">${resultA.months_to_payoff}</span>
                   </div>
                   <div class="stat">
                       <span class="label">Total Interest:</span>
                       <span class="value">$${resultA.total_interest_paid.toLocaleString()}</span>
                   </div>
                   <div class="stat">
                       <span class="label">Total Paid:</span>
                       <span class="value">$${resultA.total_amount_paid.toLocaleString()}</span>
                   </div>
               </div>
           </div>
           <div class="strategy-result">
               <h3>Strategy B Results</h3>
               <div class="result-stats">
                   <div class="stat">
                       <span class="label">Months to Payoff:</span>
                       <span class="value">${resultB.months_to_payoff}</span>
                   </div>
                   <div class="stat">
                       <span class="label">Total Interest:</span>
                       <span class="value">$${resultB.total_interest_paid.toLocaleString()}</span>
                   </div>
                   <div class="stat">
                       <span class="label">Total Paid:</span>
                       <span class="value">$${resultB.total_amount_paid.toLocaleString()}</span>
                   </div>
               </div>
           </div>
       `;
   }
   ```

#### Backend Changes

4. **Update the simulation service** (`Backend/services/simulation_service.py`):
   ```python
   def compare_strategies(self, debt_info, payment_a, payment_b):
       """Compare two different payment strategies"""
       strategy_a = self.simulate_debt_payoff(
           initial_balance=debt_info.balance,
           apr=debt_info.interest_rate,
           monthly_payment=payment_a
       )
       
       strategy_b = self.simulate_debt_payoff(
           initial_balance=debt_info.balance,
           apr=debt_info.interest_rate,
           monthly_payment=payment_b
       )
       
       return {
           'strategy_a': strategy_a,
           'strategy_b': strategy_b,
           'savings': {
               'months_saved': strategy_a['months_to_payoff'] - strategy_b['months_to_payoff'],
               'interest_saved': strategy_a['total_interest_paid'] - strategy_b['total_interest_paid']
           }
       }
   ```

5. **Add new API endpoint** (`Backend/routes/simulation.py`):
   ```python
   @simulation_bp.route('/compare', methods=['POST'])
   def compare_strategies():
       try:
           data = request.get_json()
           debt = DebtInfo(**data['debt'])
           payment_a = data['payment_a']
           payment_b = data['payment_b']
           
           result = simulation_service.compare_strategies(debt, payment_a, payment_b)
           return jsonify(result), 200
           
       except Exception as e:
           return jsonify({'error': str(e)}), 400
   ```

### Success Criteria
- [ ] Users can enter two different payment amounts
- [ ] Comparison shows side-by-side results
- [ ] Backend API endpoint works correctly
- [ ] Results are clearly formatted and easy to understand
- [ ] Error handling works for invalid inputs

---

## 🎨 Task 2: Create a Visual Timeline Chart

**Difficulty**: ⭐⭐⭐⭐ (Hard)  
**Time**: 3-4 hours  
**Files to modify**: `frontend.html`

### What You'll Do
Add an interactive chart that shows the debt payoff progress over time using Chart.js.

### Step-by-Step Instructions

1. **Add Chart.js library** to the HTML head:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
   ```

2. **Add chart container** to the results section:
   ```html
   <div class="chart-container">
       <h3>Debt Payoff Timeline</h3>
       <canvas id="debtChart" width="400" height="200"></canvas>
   </div>
   ```

3. **Add CSS for the chart**:
   ```css
   .chart-container {
       background: white;
       padding: 20px;
       border-radius: 10px;
       margin: 20px 0;
       box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
   }
   
   #debtChart {
       max-width: 100%;
       height: 400px;
   }
   ```

4. **Add JavaScript function** to create the chart:
   ```javascript
   let debtChart = null;
   
   function createDebtChart(timeline) {
       const ctx = document.getElementById('debtChart').getContext('2d');
       
       // Destroy existing chart if it exists
       if (debtChart) {
           debtChart.destroy();
       }
       
       const months = timeline.map(month => `Month ${month.month}`);
       const balances = timeline.map(month => month.balance);
       const interestPaid = timeline.map(month => month.interest_charged);
       
       debtChart = new Chart(ctx, {
           type: 'line',
           data: {
               labels: months,
               datasets: [{
                   label: 'Remaining Balance',
                   data: balances,
                   borderColor: '#667eea',
                   backgroundColor: 'rgba(102, 126, 234, 0.1)',
                   tension: 0.4,
                   fill: true
               }, {
                   label: 'Interest Paid (Cumulative)',
                   data: interestPaid,
                   borderColor: '#ff6b6b',
                   backgroundColor: 'rgba(255, 107, 107, 0.1)',
                   tension: 0.4,
                   yAxisID: 'y1'
               }]
           },
           options: {
               responsive: true,
               maintainAspectRatio: false,
               scales: {
                   y: {
                       beginAtZero: true,
                       title: {
                           display: true,
                           text: 'Balance ($)'
                       }
                   },
                   y1: {
                       type: 'linear',
                       display: true,
                       position: 'right',
                       title: {
                           display: true,
                           text: 'Interest Paid ($)'
                       },
                       grid: {
                           drawOnChartArea: false,
                       },
                   }
               },
               plugins: {
                   title: {
                       display: true,
                       text: 'Debt Payoff Progress Over Time'
                   },
                   legend: {
                       display: true,
                       position: 'top'
                   }
               }
           }
       });
   }
   ```

5. **Update the results display** to include the chart:
   ```javascript
   function displayResults(data) {
       // ... existing results display code ...
       
       // Add chart
       if (data.timeline && data.timeline.length > 0) {
           createDebtChart(data.timeline);
       }
   }
   ```

### Success Criteria
- [ ] Chart displays debt balance over time
- [ ] Chart shows cumulative interest paid
- [ ] Chart is interactive (zoom, hover, etc.)
- [ ] Chart updates when new calculations are made
- [ ] Chart is responsive and looks good on different screen sizes

---

## 🔧 Task 3: Add Export Functionality

**Difficulty**: ⭐⭐⭐ (Medium)  
**Time**: 2-3 hours  
**Files to modify**: `frontend.html`

### What You'll Do
Allow users to export their debt payoff plan as a PDF or CSV file.

### Step-by-Step Instructions

1. **Add export buttons** to the results section:
   ```html
   <div class="export-controls">
       <h3>Export Your Plan</h3>
       <button onclick="exportToPDF()" class="export-btn pdf-btn">📄 Export as PDF</button>
       <button onclick="exportToCSV()" class="export-btn csv-btn">📊 Export as CSV</button>
   </div>
   ```

2. **Add CSS for export buttons**:
   ```css
   .export-controls {
       margin: 20px 0;
       text-align: center;
   }
   
   .export-btn {
       background: #28a745;
       color: white;
       border: none;
       padding: 12px 24px;
       margin: 5px;
       border-radius: 5px;
       cursor: pointer;
       font-size: 14px;
   }
   
   .pdf-btn {
       background: #dc3545;
   }
   
   .csv-btn {
       background: #17a2b8;
   }
   ```

3. **Add JavaScript functions** for export:
   ```javascript
   function exportToPDF() {
       if (!window.lastCalculationResults) {
           alert('No results to export. Please run a calculation first.');
           return;
       }
       
       const data = window.lastCalculationResults;
       const content = generatePDFContent(data);
       
       // Create a new window with the content
       const printWindow = window.open('', '_blank');
       printWindow.document.write(content);
       printWindow.document.close();
       printWindow.print();
   }
   
   function generatePDFContent(data) {
       return `
           <!DOCTYPE html>
           <html>
           <head>
               <title>Debt Payoff Plan</title>
               <style>
                   body { font-family: Arial, sans-serif; margin: 20px; }
                   .header { text-align: center; margin-bottom: 30px; }
                   .summary { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }
                   .timeline { margin: 20px 0; }
                   table { width: 100%; border-collapse: collapse; margin: 10px 0; }
                   th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                   th { background-color: #f2f2f2; }
               </style>
           </head>
           <body>
               <div class="header">
                   <h1>Debt Payoff Plan</h1>
                   <p>Generated on ${new Date().toLocaleDateString()}</p>
               </div>
               
               <div class="summary">
                   <h2>Summary</h2>
                   <p><strong>Months to Payoff:</strong> ${data.months_to_payoff}</p>
                   <p><strong>Total Interest Paid:</strong> $${data.total_interest_paid.toLocaleString()}</p>
                   <p><strong>Total Amount Paid:</strong> $${data.total_amount_paid.toLocaleString()}</p>
                   <p><strong>Debt-Free Date:</strong> ${data.debt_free_date}</p>
               </div>
               
               <div class="timeline">
                   <h2>Monthly Breakdown</h2>
                   <table>
                       <tr>
                           <th>Month</th>
                           <th>Balance</th>
                           <th>Interest Charged</th>
                           <th>Payment Made</th>
                           <th>Principal Paid</th>
                       </tr>
                       ${data.timeline.map(month => `
                           <tr>
                               <td>${month.month}</td>
                               <td>$${month.balance.toFixed(2)}</td>
                               <td>$${month.interest_charged.toFixed(2)}</td>
                               <td>$${month.payment_made.toFixed(2)}</td>
                               <td>$${month.principal_paid.toFixed(2)}</td>
                           </tr>
                       `).join('')}
                   </table>
               </div>
           </body>
           </html>
       `;
   }
   
   function exportToCSV() {
       if (!window.lastCalculationResults) {
           alert('No results to export. Please run a calculation first.');
           return;
       }
       
       const data = window.lastCalculationResults;
       const csvContent = generateCSVContent(data);
       
       // Create and download the file
       const blob = new Blob([csvContent], { type: 'text/csv' });
       const url = window.URL.createObjectURL(blob);
       const a = document.createElement('a');
       a.href = url;
       a.download = `debt-payoff-plan-${new Date().toISOString().split('T')[0]}.csv`;
       document.body.appendChild(a);
       a.click();
       document.body.removeChild(a);
       window.URL.revokeObjectURL(url);
   }
   
   function generateCSVContent(data) {
       let csv = 'Month,Balance,Interest Charged,Payment Made,Principal Paid\n';
       
       data.timeline.forEach(month => {
           csv += `${month.month},${month.balance.toFixed(2)},${month.interest_charged.toFixed(2)},${month.payment_made.toFixed(2)},${month.principal_paid.toFixed(2)}\n`;
       });
       
       return csv;
   }
   ```

### Success Criteria
- [ ] Users can export results as PDF
- [ ] Users can export results as CSV
- [ ] PDF includes summary and detailed timeline
- [ ] CSV contains all monthly data
- [ ] Files are properly formatted and downloadable

---

## 🎯 Task 4: Add Input Validation to Backend

**Difficulty**: ⭐⭐⭐ (Medium)  
**Time**: 2-3 hours  
**Files to modify**: `Backend/utils/validation.py`, `Backend/routes/simulation.py`

### What You'll Do
Create comprehensive input validation for the backend API endpoints.

### Step-by-Step Instructions

1. **Enhance the validation utility** (`Backend/utils/validation.py`):
   ```python
   from typing import Dict, List, Any
   import re
   
   class ValidationError(Exception):
       """Custom exception for validation errors"""
       pass
   
   class DebtValidator:
       """Validates debt-related input data"""
       
       @staticmethod
       def validate_debt_amount(amount: float) -> float:
           """Validate debt amount"""
           if not isinstance(amount, (int, float)):
               raise ValidationError("Debt amount must be a number")
           
           if amount <= 0:
               raise ValidationError("Debt amount must be greater than 0")
           
           if amount > 10000000:  # 10 million
               raise ValidationError("Debt amount seems unreasonably high")
           
           return float(amount)
       
       @staticmethod
       def validate_interest_rate(rate: float) -> float:
           """Validate interest rate"""
           if not isinstance(rate, (int, float)):
               raise ValidationError("Interest rate must be a number")
           
           if rate < 0:
               raise ValidationError("Interest rate cannot be negative")
           
           if rate > 100:
               raise ValidationError("Interest rate cannot exceed 100%")
           
           return float(rate)
       
       @staticmethod
       def validate_payment_amount(payment: float, debt_amount: float) -> float:
           """Validate payment amount"""
           if not isinstance(payment, (int, float)):
               raise ValidationError("Payment amount must be a number")
           
           if payment <= 0:
               raise ValidationError("Payment amount must be greater than 0")
           
           if payment > debt_amount * 2:
               raise ValidationError("Payment amount seems unreasonably high")
           
           return float(payment)
       
       @staticmethod
       def validate_simulation_input(data: Dict[str, Any]) -> Dict[str, Any]:
           """Validate complete simulation input"""
           errors = []
           
           try:
               # Validate debt information
               if 'debt' not in data:
                   errors.append("Missing debt information")
               else:
                   debt = data['debt']
                   
                   if 'balance' not in debt:
                       errors.append("Missing debt balance")
                   else:
                       debt['balance'] = DebtValidator.validate_debt_amount(debt['balance'])
                   
                   if 'interest_rate' not in debt:
                       errors.append("Missing interest rate")
                   else:
                       debt['interest_rate'] = DebtValidator.validate_interest_rate(debt['interest_rate'])
                   
                   if 'name' not in debt or not debt['name'].strip():
                       errors.append("Debt name is required")
               
               # Validate payment amount
               if 'payment_amount' not in data:
                   errors.append("Missing payment amount")
               else:
                   data['payment_amount'] = DebtValidator.validate_payment_amount(
                       data['payment_amount'], 
                       data.get('debt', {}).get('balance', 0)
                   )
               
               if errors:
                   raise ValidationError("; ".join(errors))
               
               return data
               
           except ValidationError:
               raise
           except Exception as e:
               raise ValidationError(f"Invalid input data: {str(e)}")
   
   # Create validator instance
   debt_validator = DebtValidator()
   ```

2. **Update the simulation route** (`Backend/routes/simulation.py`):
   ```python
   from utils.validation import debt_validator, ValidationError
   
   @simulation_bp.route('/simulate', methods=['POST'])
   def simulate_debt():
       try:
           # Get and validate input data
           data = request.get_json()
           if not data:
               return jsonify({'error': 'No data provided'}), 400
           
           # Validate input
           validated_data = debt_validator.validate_simulation_input(data)
           
           # Create simulation input object
           simulation_input = SimulationInput(**validated_data)
           
           # Run simulation
           result = simulation_service.run_simulation(simulation_input)
           
           return jsonify({
               'success': True,
               'data': result,
               'timestamp': datetime.now().isoformat()
           }), 200
           
       except ValidationError as e:
           return jsonify({
               'success': False,
               'error': str(e),
               'timestamp': datetime.now().isoformat()
           }), 400
           
       except Exception as e:
           return jsonify({
               'success': False,
               'error': f'Server error: {str(e)}',
               'timestamp': datetime.now().isoformat()
           }), 500
   ```

3. **Add validation to the comparison endpoint**:
   ```python
   @simulation_bp.route('/compare', methods=['POST'])
   def compare_strategies():
       try:
           data = request.get_json()
           if not data:
               return jsonify({'error': 'No data provided'}), 400
           
           # Validate required fields
           required_fields = ['debt', 'payment_a', 'payment_b']
           for field in required_fields:
               if field not in data:
                   return jsonify({'error': f'Missing required field: {field}'}), 400
           
           # Validate debt information
           debt = debt_validator.validate_simulation_input({
               'debt': data['debt'],
               'payment_amount': data['payment_a']
           })['debt']
           
           # Validate payment amounts
           payment_a = debt_validator.validate_payment_amount(
               data['payment_a'], debt['balance']
           )
           payment_b = debt_validator.validate_payment_amount(
               data['payment_b'], debt['balance']
           )
           
           # Create debt info object
           debt_info = DebtInfo(**debt)
           
           # Run comparison
           result = simulation_service.compare_strategies(debt_info, payment_a, payment_b)
           
           return jsonify({
               'success': True,
               'data': result,
               'timestamp': datetime.now().isoformat()
           }), 200
           
       except ValidationError as e:
           return jsonify({
               'success': False,
               'error': str(e),
               'timestamp': datetime.now().isoformat()
           }), 400
           
       except Exception as e:
           return jsonify({
               'success': False,
               'error': f'Server error: {str(e)}',
               'timestamp': datetime.now().isoformat()
           }), 500
   ```

### Success Criteria
- [ ] All API endpoints validate input data
- [ ] Clear error messages are returned for invalid input
- [ ] Validation prevents common errors (negative amounts, etc.)
- [ ] Backend handles edge cases gracefully
- [ ] Error responses are consistent and helpful

---

## 🏆 Completion Checklist

When you've finished all tasks, you should have:

- [ ] ✅ Debt comparison tool working
- [ ] ✅ Visual timeline chart implemented
- [ ] ✅ Export functionality (PDF and CSV)
- [ ] ✅ Comprehensive backend validation
- [ ] ✅ All features integrated smoothly
- [ ] ✅ Error handling throughout
- [ ] ✅ Code is well-documented

## 🎯 What You've Learned

After completing these tasks, you'll understand:
- **Full-stack development** - both frontend and backend
- **API design** and RESTful principles
- **Data validation** and error handling
- **Chart.js integration** for data visualization
- **File export** functionality
- **Advanced JavaScript** concepts
- **Python validation** and error handling
- **Code organization** and best practices

## 🚀 Next Steps

Once you've completed these tasks:
1. **Test thoroughly** - Make sure everything works together
2. **Code review** - Have someone review your code
3. **Documentation** - Update any relevant documentation
4. **Advanced tasks** - Move on to expert-level tasks
5. **Mentoring** - Help other team members

## 💡 Tips for Success

- **Test each feature** as you build it
- **Handle errors gracefully** - users will make mistakes
- **Write clean code** - others will need to understand it
- **Ask for help** when you're stuck
- **Take pride in your work** - these are real features users will use!

**Remember**: These tasks are more complex and will challenge you. Take your time, break problems down into smaller pieces, and don't hesitate to ask for help when you need it! 🎉
