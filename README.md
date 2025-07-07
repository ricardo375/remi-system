# REMI Automation System

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Fill in credentials in the `.env` files inside the `credentials` folder.
3. Run workflows or agents directly as needed.

## Usage

- **Push leads to Google Sheets**
  ```bash
  python lead_pusher.py
  ```
- **Run lead intake and follow-up workflow**
  ```bash
  python workflows/lead_intake_followup.py
  ```
- **Organize files**
  ```bash
  python agents/admin.py
  ```
