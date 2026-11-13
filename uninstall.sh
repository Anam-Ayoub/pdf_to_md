#!/usr/bin/env bash
set -e

APP_NAME="pdf-to-md"
APP_DISPLAY_NAME="PDF to Markdown"

echo "==> Uninstalling $APP_DISPLAY_NAME..."

rm -rf "$HOME/.local/share/$APP_NAME"
rm -f "$HOME/.local/bin/$APP_NAME"
rm -f "$HOME/.local/share/applications/$APP_NAME.desktop"
rm -f "$HOME/.local/share/icons/hicolor/256x256/apps/$APP_NAME.png"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
fi

echo "✅ $APP_DISPLAY_NAME has been uninstalled."
