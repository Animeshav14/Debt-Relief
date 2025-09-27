# 🛠️ Debt Relief Project - Complete Setup Guide

This guide will walk you through setting up the Debt Relief project on your computer from scratch. Follow these steps carefully, and you'll have everything running in no time!

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Testing Your Setup](#testing-your-setup)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)

---

## ✅ Prerequisites

### Required Software
Before you start, make sure you have these installed:

#### 1. **Python 3.8 or Higher**
- **Download**: https://www.python.org/downloads/
- **Check version**: Open terminal/command prompt and run:
  ```bash
  python --version
  # or
  python3 --version
  ```
- **If not installed**: Download and install Python 3.8+ from the official website

#### 2. **Git**
- **Download**: https://git-scm.com/downloads
- **Check installation**: Run in terminal:
  ```bash
  git --version
  ```
- **If not installed**: Download and install Git from the official website

#### 3. **Code Editor** (Recommended: VS Code)
- **Download**: https://code.visualstudio.com/
- **Extensions to install**:
  - Python (by Microsoft)
  - HTML CSS Support
  - JavaScript (ES6) code snippets
  - Live Server (for frontend development)

#### 4. **Web Browser**
- Any modern browser (Chrome, Firefox, Safari, Edge)
- Chrome recommended for best debugging experience

---

## 🚀 Initial Setup

### Step 1: Clone the Repository
1. **Open terminal/command prompt**
2. **Navigate to where you want the project** (e.g., Desktop or Documents)
   ```bash
   cd ~/Desktop  # On Mac/Linux
   # or
   cd C:\Users\YourName\Desktop  # On Windows
   ```
3. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Debt-Relief.git
   ```
4. **Navigate into the project directory**:
   ```bash
   cd Debt-Relief
   ```

### Step 2: Verify Project Structure
You should see these files and folders:
```
Debt-Relief/
├── Backend/
│   ├── app.py
│   ├── config/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── frontend.html
├── medical_debt_frontend.html
├── typeform_frontend.html
├── requirements.txt
└── README.md
```

**If you don't see this structure, something went wrong with the clone. Try cloning again.**

---

## 🐍 Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd Backend
```

### Step 2: Create Virtual Environment (Recommended)
**Why use a virtual environment?**
- Keeps project dependencies separate from system Python
- Prevents conflicts between different projects
- Makes it easier to manage dependencies

**Create virtual environment**:
```bash
# On Mac/Linux
python3 -m venv venv

# On Windows
python -m venv venv
```

**Activate virtual environment**:
```bash
# On Mac/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

**You should see `(venv)` at the beginning of your terminal prompt when activated.**

### Step 3: Install Dependencies
```bash
pip install -r ../requirements.txt
```

**Expected output**:
```
Collecting Flask==3.0.0
  Downloading Flask-3.0.0-py3-none-any.whl
Collecting Flask-CORS==4.0.0
  Downloading Flask_CORS-4.0.0-py2.py3-none-any.whl
Collecting python-dotenv==1.0.0
  Downloading python_dotenv-1.0.0-py2.py3-none-any.whl
Collecting requests==2.31.0
  Downloading requests-2.31.0-py2.py3-none-any.whl
Installing collected packages: ...
Successfully installed Flask-3.0.0 Flask-CORS-4.0.0 python-dotenv-1.0.0 requests-2.31.0
```

### Step 4: Set Up Environment Variables (Optional)
Create a `.env` file in the Backend directory:
```bash
# Create .env file
touch .env  # On Mac/Linux
# or
echo. > .env  # On Windows
```

Add these lines to the `.env` file:
```env
# Backend server configuration
PORT=5001
FLASK_ENV=development

# Nessie API (optional - for advanced features)
NESSIE_API_KEY=your_api_key_here
```

**Note**: The Nessie API key is optional. The system works without it using fallback calculations.

### Step 5: Start the Backend Server
```bash
python app.py
```

**Expected output**:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://[your-ip]:5001
 * Press CTRL+C to quit
```

**🎉 Congratulations! Your backend is running!**

**Keep this terminal window open** - the server needs to stay running for the frontend to work.

---

## 🖥️ Frontend Setup

### Step 1: Open Frontend Files
You have three options for viewing the frontend:

#### Option A: Direct File Opening (Simplest)
1. **Navigate to the project root directory** (one level up from Backend)
2. **Double-click on any HTML file**:
   - `frontend.html` - Basic debt calculator
   - `medical_debt_frontend.html` - Advanced medical debt simulator
   - `typeform_frontend.html` - Step-by-step questionnaire

#### Option B: VS Code Live Server (Recommended)
1. **Open VS Code**
2. **Open the project folder**: File → Open Folder → Select Debt-Relief folder
3. **Right-click on any HTML file** → "Open with Live Server"
4. **Browser will open automatically**

#### Option C: Python Simple Server
1. **Open a new terminal window** (keep the backend running in the first one)
2. **Navigate to project root**:
   ```bash
   cd ..  # Go up one level from Backend directory
   ```
3. **Start simple server**:
   ```bash
   python -m http.server 8000
   ```
4. **Open browser** and go to:
   - http://localhost:8000/frontend.html
   - http://localhost:8000/medical_debt_frontend.html
   - http://localhost:8000/typeform_frontend.html

### Step 2: Test Frontend-Backend Connection
1. **Open the basic calculator** (`frontend.html`)
2. **Fill in some test data**:
   - Debt amount: `5000`
   - Interest rate: `18`
   - Monthly payment: `200`
3. **Click "Calculate"**
4. **You should see results** with months to payoff and total interest

**If you get an error**, check that:
- Backend server is still running
- You're using the correct URL (localhost:5001)
- No firewall is blocking the connection

---

## ✅ Testing Your Setup

### Test 1: Basic Debt Calculator
1. **Open** `frontend.html`
2. **Enter test data**:
   - Debt Amount: `10000`
   - Interest Rate: `15`
   - Monthly Payment: `300`
3. **Click Calculate**
4. **Expected result**: Should show approximately 42 months to payoff

### Test 2: Medical Debt Simulator
1. **Open** `medical_debt_frontend.html`
2. **Fill in financial information**:
   - Monthly Income: `5000`
   - Current Balance: `2000`
   - Monthly Expenses: `3500`
3. **Add a medical debt**:
   - Provider: `General Hospital`
   - Amount: `8000`
   - Interest Rate: `0`
   - Minimum Payment: `200`
4. **Click "Run Complete Simulation"**
5. **Expected result**: Should show three different payoff strategies

### Test 3: Backend Health Check
1. **Open browser** and go to: http://localhost:5001/api/health
2. **Expected result**: Should show `{"status": "OK", "message": "Server is running"}`

### Test 4: API Endpoint Test
1. **Open browser** and go to: http://localhost:5001/api/medical/test
2. **Expected result**: Should show a test response from the medical simulation API

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Python not found" or "python: command not found"
**Solution**:
- Make sure Python is installed correctly
- Try using `python3` instead of `python`
- Add Python to your system PATH

#### Issue 2: "Module not found" errors when running app.py
**Solution**:
- Make sure you're in the Backend directory
- Make sure virtual environment is activated
- Reinstall requirements: `pip install -r ../requirements.txt`

#### Issue 3: "Address already in use" error
**Solution**:
- Another process is using port 5001
- Kill the process: `lsof -ti:5001 | xargs kill -9` (Mac/Linux)
- Or change the port in app.py

#### Issue 4: Frontend can't connect to backend
**Solution**:
- Make sure backend is running (check terminal)
- Check the URL in frontend JavaScript
- Make sure no firewall is blocking the connection
- Try refreshing the page

#### Issue 5: "CORS" errors in browser console
**Solution**:
- This is normal for local development
- The backend has CORS enabled, so this shouldn't be an issue
- If it persists, check that Flask-CORS is installed

#### Issue 6: Calculations not working
**Solution**:
- Check browser console for JavaScript errors
- Verify backend is running and accessible
- Check that all required fields are filled
- Try with different test data

### Getting Help
If you're still having issues:
1. **Check the terminal output** for error messages
2. **Check browser console** (F12 → Console tab) for JavaScript errors
3. **Try the troubleshooting steps above**
4. **Ask for help** with specific error messages

---

## 🎯 Next Steps

### Once Everything is Working:
1. **Explore the codebase** - Open different files and understand how they work
2. **Try making small changes** - Change some text or colors
3. **Read the documentation** - Check out the other README files
4. **Start working on tasks** - Look at the task files we'll create next

### Development Workflow:
1. **Always activate virtual environment** before working
2. **Keep backend running** in one terminal
3. **Use frontend in browser** for testing
4. **Make changes and refresh** to see results

### File Organization:
- **Backend code**: All in the `Backend/` directory
- **Frontend code**: HTML files in the root directory
- **Documentation**: Various README files
- **Your work**: Will be in specific task files

---

## 🎉 Congratulations!

You now have a fully working Debt Relief project! You can:
- ✅ Run the backend server
- ✅ View and interact with the frontend
- ✅ Perform debt calculations
- ✅ Test all the features
- ✅ Start developing new features

**Next up**: We'll create specific task files with detailed instructions for what you can work on. Stay tuned!

---

## 📞 Support

If you run into any issues during setup:
1. **Check this guide again** - Make sure you followed all steps
2. **Check the troubleshooting section** - Common issues are covered
3. **Ask for help** - Provide specific error messages and what you've tried

**Remember**: There's no such thing as a stupid question! We're here to help you succeed! 🚀
