#!/bin/bash

# ========================================
# Conda Environment Setup Script (Linux)
# ========================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "========================================"
echo "Conda Environment Setup Script (Linux)"
echo "========================================"
echo

# 1) Check if conda is available
print_status "Checking conda environment..."
if ! command -v conda &> /dev/null; then
    print_error "conda not detected, please install Anaconda/Miniconda and add it to PATH"
    echo "CentOS installation reference:"
    echo "  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
    echo "  bash Miniconda3-latest-Linux-x86_64.sh"
    echo "  source ~/.bashrc"
    exit 1
fi

# 2) Parse default environment name (from name field in HTTP/environment.yml)
DEFAULT_ENV_NAME=$(grep "^name:" HTTP/environment.yml | cut -d: -f2 | tr -d ' ')
if [ -z "$DEFAULT_ENV_NAME" ]; then
    DEFAULT_ENV_NAME="NWT"
fi
echo "Detected default environment name: $DEFAULT_ENV_NAME"
echo

# Tool function: Check if environment exists
check_env_exists() {
    local env_name="$1"
    conda env list | grep -E "^[[:space:]]*${env_name}[[:space:]]" > /dev/null
    return $?
}

# 3) Check if default environment already exists
if check_env_exists "$DEFAULT_ENV_NAME"; then
    echo "Found existing Conda environment with same name: $DEFAULT_ENV_NAME"
    read -p "Use existing environment? (y=use, n=create new): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        # Ask for new environment name
        while true; do
            read -p "Enter new environment name (letters/numbers/underscores/hyphens only): " ENV_NAME
            if [ -z "$ENV_NAME" ]; then
                echo "Environment name cannot be empty, please re-enter."
                continue
            fi
            if [[ ! "$ENV_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
                echo "Environment name can only contain letters, numbers, underscores and hyphens, please re-enter."
                continue
            fi
            if check_env_exists "$ENV_NAME"; then
                echo "This environment name already exists, please re-enter."
                continue
            fi
            break
        done
    else
        ENV_NAME="$DEFAULT_ENV_NAME"
    fi
else
    ENV_NAME="$DEFAULT_ENV_NAME"
fi

# 4) Create environment if it doesn't exist; activate if it exists
if ! check_env_exists "$ENV_NAME"; then
    echo
    print_status "Creating environment '$ENV_NAME' using HTTP/environment.yml..."
    if conda env create -n "$ENV_NAME" -f HTTP/environment.yml -y; then
        print_success "Environment '$ENV_NAME' created successfully ✓"
    else
        print_error "Failed to create Conda environment."
        exit 1
    fi
else
    echo
    print_status "Using existing environment '$ENV_NAME'..."
fi

# 5) Activate environment (effective in current session, for use by subsequent scripts)
print_status "Activating conda environment..."
if conda activate "$ENV_NAME"; then
    export CONDA_ENV_NAME="$ENV_NAME"
    print_success "Conda environment activated: $ENV_NAME"
    python --version 2>/dev/null || echo "Failed to get Python version information"
    echo
else
    print_error "Failed to activate environment."
    exit 1
fi

# 6) Verify environment is correctly activated
if [ -z "$CONDA_DEFAULT_ENV" ] || [ "$CONDA_DEFAULT_ENV" != "$ENV_NAME" ]; then
    print_warning "Environment may not be correctly activated, trying manual activation..."
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate "$ENV_NAME"
    export CONDA_ENV_NAME="$ENV_NAME"
fi

print_success "Conda environment setup completed!"
echo "Current environment: $ENV_NAME"
echo "Python path: $(which python)"
echo "Conda path: $(which conda)"
echo

exit 0
