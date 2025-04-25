#!/bin/bash
# setup.sh - Setup script for SMORT Thrasher Backend
set -e

# Text formatting
BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BOLD}SMORT Thrasher Backend Setup${NC}"
echo "==============================="
echo ""

# Function to display steps
step() {
    echo -e "${GREEN}[+] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[!] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# Check if running as root for systemd setup
if [[ $EUID -ne 0 && "$1" == "--systemd" ]]; then
    error "Systemd setup requires root privileges. Run with sudo."
fi

# Check for required tools
step "Checking requirements..."
command -v python3 >/dev/null 2>&1 || error "Python 3 is required but not installed."

if [[ "$1" == "--docker" ]]; then
    command -v docker >/dev/null 2>&1 || error "Docker is required but not installed."
fi

# Setup Python environment
step "Setting up Python environment..."
if ! command -v poetry >/dev/null 2>&1; then
    echo "Poetry not found. Installing..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install dependencies
step "Installing dependencies..."
poetry install

# Check if .env file exists
if [ ! -f .env ]; then
    warn ".env file not found. Creating a sample one..."
    echo "CONNECTION_STRING=postgresql://postgres:password@localhost/postgres" > .env
    echo "Please update the .env file with your actual database connection string."
fi

# Option to run database migrations
read -p "Do you want to run database migrations? (y/n): " run_migrations
if [[ $run_migrations == "y" || $run_migrations == "Y" ]]; then
    step "Running database migrations..."
    poetry run alembic upgrade head
fi

# Handle deployment options
if [[ "$1" == "--docker" ]]; then
    step "Building Docker image..."
    docker build -t smort-thrasher-backend .
    
    step "Starting Docker container..."
    docker run -d -p 80:80 --name smort-api smort-thrasher-backend
    echo "Application is running in Docker on port 80"

elif [[ "$1" == "--systemd" ]]; then
    step "Setting up systemd service..."
    
    # Get absolute path to the project directory
    PROJECT_DIR=$(pwd)
    
    # Find Poetry's Python path
    POETRY_PYTHON=$(poetry run which python)
    
    # Create systemd service file
    cat > /etc/systemd/system/smort-thrasher.service << EOF
[Unit]
Description=SMORT Thrasher Backend
After=network.target postgresql.service

[Service]
User=$(whoami)
Group=$(id -gn)
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PATH"
ExecStart=$POETRY_PYTHON -m uvicorn app.main:app --host 0.0.0.0 --port 80

# Restart on failure
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

    # Set proper permissions
    chmod 644 /etc/systemd/system/smort-thrasher.service
    
    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable smort-thrasher.service
    systemctl start smort-thrasher.service
    
    echo "Systemd service installed and started."
    echo "You can check its status with: sudo systemctl status smort-thrasher.service"

else
    # Default: just start the app in development mode
    step "Starting development server..."
    poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    echo "Application is running on http://localhost:8000"
fi

echo ""
echo -e "${BOLD}Setup completed successfully!${NC}"
echo "==============================="
echo ""
echo "Usage:"
echo "  • Development mode: ./setup.sh"
echo "  • Docker mode: ./setup.sh --docker"
echo "  • Systemd service: sudo ./setup.sh --systemd"
