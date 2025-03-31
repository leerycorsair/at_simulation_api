#!/bin/bash
# Creates a new Alembic database revision with proper validation and error handling
# Usage: ./create_revision.sh "Your revision description"

set -eo pipefail  # Exit on error and pipeline failures
shopt -s nullglob # Prevent globbing from returning literal patterns

readonly SCRIPT_NAME=$(basename "$0")
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Logs an error message and exits
# Arguments:
#   $1 - Error message
#   $2 - Exit code (optional, default: 1)
#######################################
_error_exit() {
  echo -e "${RED}ERROR: ${1}${NC}" >&2
  exit "${2:-1}"
}

#######################################
# Logs an informational message
# Arguments:
#   $1 - Message to display
#######################################
_log_info() {
  echo -e "${GREEN}INFO: ${1}${NC}"
}

#######################################
# Validates script prerequisites
#######################################
_validate_prerequisites() {
  if [[ -z "$1" ]]; then
    _error_exit "Revision message required\nUsage: $SCRIPT_NAME \"Your revision message\"" 2
  fi

  if ! command -v alembic >/dev/null 2>&1; then
    _error_exit "Alembic not found. Please install with:\n  pip install alembic"
  fi

  if [[ ! -d "alembic" ]]; then
    _error_exit "Alembic directory not found. Run 'alembic init alembic' first."
  fi
}

#######################################
# Creates versions directory if missing
#######################################
_ensure_versions_directory() {
  local versions_dir="alembic/versions"

  if [[ ! -d "$versions_dir" ]]; then
    _log_info "Creating versions directory..."
    mkdir -p "$versions_dir" || _error_exit "Failed to create versions directory"
  fi
}

#######################################
# Creates new alembic revision
# Arguments:
#   $1 - Revision message
#######################################
_create_revision() {
  local msg="$1"

  _log_info "Creating revision: \"$msg\""
  if alembic revision --autogenerate -m "$msg"; then
    local latest_revision=$(ls -1t alembic/versions/ | head -n 1)
    _log_info "Successfully created revision: ${latest_revision}"
  else
    _error_exit "Revision creation failed"
  fi
}

#######################################
# Main execution
#######################################
_main() {
  _validate_prerequisites "$@"
  _ensure_versions_directory
  _create_revision "$1"
}

_main "$@"
