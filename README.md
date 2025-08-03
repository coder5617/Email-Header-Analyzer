# Email Header Analyzer

Comprehensive email header analysis tool for cybersecurity professionals.

## Features

- **Authentication Analysis**: SPF, DKIM, DMARC verification
- **Routing Analysis**: SMTP hop analysis and suspicious routing detection  
- **Spoofing Detection**: Domain spoofing, display name impersonation
- **Geographic Analysis**: IP geolocation and reputation checking
- **Content Analysis**: Subject line analysis and social engineering detection
- **Web Interface**: User-friendly Streamlit interface

## Quick Start

1. **Clone the repository and navigate into it:**
    ```bash
    git clone <repository-url>
    cd email-header-analyzer
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install pip-tools and compile dependencies:**
    ```bash
    pip install --upgrade pip pip-tools
    pip-compile requirements.in
    ```

4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the web application:**
    ```bash
    email-header-analyzer --mode web
    ```
    Open your browser at http://localhost:8501

6. **Run CLI analysis:**
    ```bash
    email-header-analyzer --mode cli --file tests/sample_headers/legitimate.txt
    ```

7. **Run tests:**
    ```bash
    pytest -v
    ```

## Updating Dependencies

- Edit `requirements.in` with desired version ranges.
- Run `pip-compile requirements.in` to update `requirements.txt`.
- Re-install with `pip install -r requirements.txt`.

## Docker Deployment

See `Dockerfile` for container setup, which uses pip-tools to compile and pin dependencies.

## License

MIT License
