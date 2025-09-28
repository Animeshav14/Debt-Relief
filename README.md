# Debt Relief Simulator - Complete Setup Guide

A debt relief calculator with medical debt simulation capabilities. This project includes a Flask backend API and a modern HTML frontend with a step-by-step questionnaire interface.

## 📋 Quick Start

### Prerequisites
- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/downloads/)
- **Web Browser** (Chrome, Firefox, Safari, or Edge)

### Step-by-Step Setup

#### 1. Clone and Navigate to Project
```bash
# Clone the repository
git clone https://github.com/yourusername/Debt-Relief.git

# Navigate to project directory
cd Debt-Relief
```

#### 2. Set Up Backend (Flask API)

**Navigate to Backend directory:**
```bash
cd Backend
```

**Create and activate virtual environment:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install -r ../requirements.txt
```

**Start the backend server:**
```bash
python app.py
```

**You should see:**
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5001
* Press CTRL+C to quit
```

**Keep this terminal window open** - the server must stay running!

#### 3. Open the Frontend

**Option A: Direct File Opening (Easiest)**
1. Navigate back to project root: `cd ..`
2. Double-click `typeform_frontend.html` to open in your browser

**Option B: VS Code Live Server (Recommended)**
1. Open VS Code
2. Open the Debt-Relief folder
3. Right-click `typeform_frontend.html` → "Open with Live Server"

**Option C: Python Simple Server**
```bash
# In a new terminal window (keep backend running)
cd /path/to/Debt-Relief
python -m http.server 8000
# Then open http://localhost:8000/typeform_frontend.html
```

## How to Use the Application

### 1. Open the Application
- Open `typeform_frontend.html` in your web browser
- You'll see a beautiful step-by-step questionnaire interface

### 2. Fill Out the Form
**Step 1: Financial Information**
- Enter your monthly income
- Enter your current savings balance
- Enter your monthly expenses

**Step 2: Medical Debts**
- Add details for each medical debt:
  - What the debt is for
  - Provider/hospital name
  - Amount owed
  - Interest rate (usually 0% for medical debt)
  - Minimum payment
  - Current monthly payment
  - Service date
  - Insurance coverage amount
- Click "+ Add Another Medical Debt" for multiple debts

**Step 3: Goals**
- Set your target payoff time in months
- Click "Analyze My Current Trajectory"

### 3. View Results
The application will show:
- **Current Trajectory**: How long it will take with your current payments
- **Personalized Plans**: Different payoff strategies based on your goals
- **Recommendations**: Specific advice for your situation
