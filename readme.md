# Project Setup Guide

This document provides step-by-step instructions to set up the Python environment for this project.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python**: Version 3.10.11
- **pip**: Python's package manager (comes pre-installed with Python 3.4+)

You may also want to install a virtual environment tool like `venv` or `virtualenv` to isolate dependencies.

---

## Installation Steps

### 1. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone <repository_url>
cd <project_directory>
```
---

### 2. Set Up a Virtual Environment (Optional but Recommended)

Create and activate a virtual environment to isolate dependencies.

#### On macOS/Linux:

```bash
python3 -m venv .venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install the Dependencies
Install the required Python modules listed in requirements.txt:
```bash
pip install -r requirements.txt
```
### 4. Verify the Installation
Check if all required packages are installed and the Python version is correct:
```bash
python --version
```
Ensure it displays Python 3.10.11.
List the installed packages to confirm dependencies:
```bash
pip list
```

---

### 5. Running the Project

After completing the installation, you can run the project by executing the appropriate script:
```bash
python app.py
```
---