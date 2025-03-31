#!/bin/bash
# Safely downgrades database to the previous Alembic revision
# Usage: ./downgrade_head.sh [-y|--yes] [revision_id]

set -eo pipefail
shopt -s nullglob

readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

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
# Validate environment and prerequisites
#######################################
_validate_environment() {
    if ! command -v alembic >/dev/null 2>&1; then
        _error_exit "Alembic not found. Install with: pip install alembic"
    fi

    if [[ ! -d "alembic" ]]; then
        _error_exit "Alembic directory not found. Run 'alembic init alembic' first."
    fi

    if [[ ! -d "alembic/versions" ]]; then
        _error_exit "No versions directory found. Create revisions first."
    fi

    local migration_count=$(ls -1 alembic/versions/*.py 2>/dev/null | wc -l)
    if [[ $migration_count -eq 0 ]]; then
        _error_exit "No migration files found in versions directory."
    fi
}

#######################################
# Get current database revision
#######################################
_get_current_revision() {
    alembic current 2>&1 | awk '{print $1}'
}

#######################################
# Get previous revision ID
#######################################
_get_previous_revision() {
    local current_rev="$1"
    alembic history | grep -B1 "$current_rev" | head -n1 | awk '{print $1}'
}

#######################################
# Confirm downgrade with user
#######################################
_confirm_downgrade() {
    local target_rev="$1"
    local current_rev="$2"

    if [[ "$AUTO_CONFIRM" == "true" ]]; then
        return 0
    fi

    echo -e "${YELLOW}WARNING: You are about to downgrade the database${NC}"
    echo -e "Current revision: ${GREEN}${current_rev}${NC}"
    echo -e "Target revision:  ${RED}${target_rev}${NC}"
    read -p "Are you sure you want to continue? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        _log_info "Downgrade cancelled by user"
        exit 0
    fi
}

#######################################
# Perform the downgrade operation
#######################################
_perform_downgrade() {
    local target_rev="$1"
    _log_info "Downgrading to revision: ${target_rev}"

    if alembic downgrade "$target_rev"; then
        _log_info "Successfully downgraded database"
        _log_info "New current revision: $(_get_current_revision)"
    else
        _error_exit "Database downgrade failed"
    fi
}

#######################################
# Main execution flow
#######################################
_main() {
    local target_revision=""
    AUTO_CONFIRM="false"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -y|--yes)
                AUTO_CONFIRM="true"
                shift
                ;;
            *)
                if [[ -z "$target_revision" ]]; then
                    target_revision="$1"
                    shift
                else
                    _error_exit "Too many arguments provided"
                fi
                ;;
        esac
    done

    _validate_environment

    local current_rev=$(_get_current_revision)
    if [[ -z "$current_rev" ]]; then
        _error_exit "Unable to determine current database revision"
    fi

    if [[ -z "$target_revision" ]]; then
        target_revision=$(_get_previous_revision "$current_rev")
        if [[ -z "$target_revision" ]]; then
            _error_exit "Could not determine previous revision"
        fi
    fi

    _confirm_downgrade "$target_revision" "$current_rev"
    _perform_downgrade "$target_revision"
}

_main "$@"