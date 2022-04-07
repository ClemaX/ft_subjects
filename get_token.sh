#!/usr/bin/env bash

# Abort on errors.
set -euo pipefail

# Get cache directory.
UNAME=$(uname -s)
case "$UNAME" in
	Linux*)		CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/subjects";;
	Darwin*)	CACHE_DIR="$HOME/Library/Caches/fr.42lyon.chamada.subjects";;
	*)			echo "Unknown system: '$UNAME'!" >&2 && exit 1;;
esac

# Script directory.
PARENT_DIR=$(dirname "$0")

# Firefox profile directory.
PROFILE=$("$PARENT_DIR/select_profile.sh")

# Temporary database copy location.
DB_TMP="$CACHE_DIR/webappsstore.sqlite"

# Token destination.
TOKEN="$CACHE_DIR/token"

# Create cache directory.
mkdir -p "$CACHE_DIR"

# Files should be accessible only to the current user.
umask 177

# Copy database.
cp "$PROFILE/cookies.sqlite" "$DB_TMP"

# Extract token.
sqlite3 "$DB_TMP" <<EOF | tr -d $'"\x1e' > "$TOKEN"
.mode ascii
SELECT value FROM moz_cookies WHERE host = '.intra.42.fr' AND name = '_intra_42_session_production';
EOF

# Remove temporary files.
rm "$DB_TMP"*
