# Calorie Plot

A dashboard for visualizing cronology.com calorie data.

## Usage

1.  **Install dependencies:**

    ```bash
    uv pip install -r requirements.txt
    ```

2.  **Set environment variables:**

    Before running the script, you need to set the following environment variables with your Cronometer credentials.

    **On macOS or Linux:**
    ```bash
    export CRONOMETER_USER="your_username"
    export CRONOMETER_PASS="your_password"
    ```

    **On Windows (Command Prompt):**
    ```cmd
    set CRONOMETER_USER="your_username"
    set CRONOMETER_PASS="your_password"
    ```

    **On Windows (PowerShell):**
    ```powershell
    $env:CRONOMETER_USER="your_username"
    $env:CRONOMETER_PASS="your_password"
    ```

3.  **Run the dashboard:**

    ```bash
    python dashboard.py
    ```

    The script will download your Cronometer data, cache it locally, and then display the dashboard.
