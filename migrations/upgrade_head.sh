#!/bin/bash
# Upgrades database to the latest Alembic revision
# Usage: ./upgrade_head.sh

set -eo pipefail  # Exit on error and pipeline failures
shopt -s nullglob # Prevent globbing from returning literal patterns

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
    if ! command -v alembic >/dev/null 2>&1; then
        _error_exit "Alembic not found. Please install with:\n  pip install alembic"
    fi

    if [[ ! -d "alembic" ]]; then
        _error_exit "Alembic directory not found. Run 'alembic init alembic' first."
    fi

    if [[ ! -d "alembic/versions" ]]; then
        _error_exit "No versions directory found. Create your first revision first."
    fi

    local migration_count=$(ls -1 alembic/versions/*.py 2>/dev/null | wc -l)
    if [[ $migration_count -eq 0 ]]; then
        _error_exit "No migration files found in versions directory."
    fi
}

#######################################
# Gets current database revision
#######################################
_get_current_revision() {
    alembic current 2>&1 | awk '{print $1}'
}

#######################################
# Gets head revision
#######################################
_get_head_revision() {
    alembic heads | awk '{print $1}'
}

#######################################
# Performs the database upgrade
#######################################
_perform_upgrade() {
    local current_rev=$(_get_current_revision)
    local head_rev=$(_get_head_revision)

    if [[ "$current_rev" == "$head_rev" ]]; then
        _log_info "Database is already at the latest revision (${head_rev})"
        return 0
    fi

    _log_info "Current revision: ${current_rev:-<base>}"
    _log_info "Upgrading to head revision: ${head_rev}"

    if alembic upgrade head; then
        _log_info "Successfully upgraded database to head revision"
        return 0
    else
        _error_exit "Database upgrade failed"
    fi
}

#######################################
# Main execution
#######################################
_main() {
    _validate_prerequisites
    _perform_upgrade
}

_main "$@"