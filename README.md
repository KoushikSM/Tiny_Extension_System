# Tiny-Extension-Analysis
A browser extension security analysis lab that performs static analysis + dynamic (runtime) analysis on Chrome extensions, with automated execution and log collection.
🧩 Tiny Extension System — How to Run (From Start) 

This guide explains how to run the project from scratch, in the correct order. 

 

1️⃣ Prerequisites 

Make sure the following are installed: 

Python 3.9+ 

Node.js 18+ 

Google Chrome 

pip and npm available in PATH 

Verify: 

python --version 
node --version 
 

 

2️⃣ Clone the Repository 

git clone https://github.com/KoushikSM/Tiny_Extension_System.git 
cd Tiny_Extension_System 
 

 

3️⃣ Project Structure Overview 

Tiny_Extension_System/ 
├── api/                  # FastAPI backend 
├── static_analysis/      # Static analysis scripts 
├── dynamic_analysis/     # Runtime analysis automation 
├── extensions/           # Sample Chrome extensions 
├── docs/                 # Documentation 
├── README.md 
├── .gitignore 
└── LICENSE 
 

 

4️⃣ Static Analysis (FIRST STEP) 

Static analysis inspects extension manifests and code without executing them. 

4.1 Run static analysis on a single extension 

python static_analysis/static_scanner.py extensions/tiny-extension 
 

This analyzes: 

manifest.json 

permissions 

risky patterns 

 

4.2 Run batch static analysis on all extensions 

python static_analysis/batch_scan.py extensions/ 
 

This scans all subfolders inside extensions/ that contain a manifest.json. 

Output reports are generated locally and excluded from version control. 

 

5️⃣ Backend API (SECOND STEP) 

The backend collects runtime logs during dynamic analysis. 

5.1 Create and activate virtual environment 

python -m venv venv 
 

Windows 

venv\Scripts\activate 
 

Linux / macOS 

source venv/bin/activate 
 

 

5.2 Install dependencies 

pip install fastapi uvicorn 
 

 

5.3 Start the API server 

uvicorn api.main:app --reload 
 

The server starts at: 

http://127.0.0.1:8000 
 

 

6️⃣ Dynamic Analysis (FINAL STEP) 

Dynamic analysis executes extensions in a real browser environment and captures behavior. 

6.1 Install Node.js dependencies (if required) 

npm install 
 

 

6.2 Run dynamic analysis 

node dynamic_analysis/dynamic_runner.js 
 

This step: 

Launches Chrome 

Loads sample extensions 

Monitors runtime activity 

Sends logs to the API backend 

 

7️⃣ Results 

Static analysis generates reports locally 

Dynamic analysis collects runtime network logs 

All generated files are ignored via .gitignore 

 

⚠️ Notes 

This project is intended for educational and research purposes only 

Do not analyze extensions you do not own or have permission to test 

 
