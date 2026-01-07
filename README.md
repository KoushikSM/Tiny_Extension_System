# Tiny-Extension-Analysis
A browser extension security analysis lab that performs static analysis + dynamic (runtime) analysis on Chrome extensions, with automated execution and log collection.

## Prerequisites

Make sure the following are installed:

- Python 3.9+
- Node.js 18+
- Google Chrome
- `pip` and `npm` available in PATH

### Verify installations

```bash
python --version
node --version

Clone the Repository
git clone https://github.com/KoushikSM/Tiny_Extension_System.git
cd Tiny_Extension_System

Project Structure Overview
Tiny_Extension_System/
├── api/                 # FastAPI backend
├── static_analysis/     # Static analysis scripts
├── dynamic_analysis/    # Runtime analysis automation
├── extensions/          # Sample Chrome extensions
├── docs/                # Documentation
├── README.md
├── .gitignore
└── LICENSE

Static Analysis (FIRST STEP)
Analyze a single extension
python static_analysis/static_scanner.py extensions/tiny-extension

Batch scan all extensions
python static_analysis/batch_scan.py extensions/


