#!/bin/sh
# Install or reinstall the collector LaunchAgent for the current user.
# Usage: sh deploy/macos/install.sh [uninstall]
set -eu

LABEL="com.crypto-institution-research.collector"
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
TARGET="$HOME/Library/LaunchAgents/$LABEL.plist"
DOMAIN="gui/$(id -u)"

launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true

if [ "${1:-}" = "uninstall" ]; then
    rm -f "$TARGET"
    echo "removed $TARGET"
    exit 0
fi

if [ ! -x "$REPO/.venv/bin/python" ]; then
    echo "missing $REPO/.venv; run: python3 -m venv .venv && .venv/bin/pip install -e ." >&2
    exit 1
fi
case "$REPO" in
    *"&"*|*"<"*|*">"*) echo "repository path must not contain & < >" >&2; exit 1 ;;
esac

mkdir -p "$REPO/data" "$HOME/Library/LaunchAgents"
sed "s|__REPO__|$REPO|g" "$REPO/deploy/macos/$LABEL.plist.template" > "$TARGET"
plutil -lint "$TARGET"
launchctl bootstrap "$DOMAIN" "$TARGET"
echo "installed $TARGET"
launchctl print "$DOMAIN/$LABEL" | grep -E "state|pid" || true
