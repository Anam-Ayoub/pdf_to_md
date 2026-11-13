#!/usr/bin/env bash
set -e

# Directories
APP_NAME="pdf-to-md"
APP_DISPLAY_NAME="PDF to Markdown"
INSTALL_DIR="$HOME/.local/share/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Installing $APP_DISPLAY_NAME..."

# Create target directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# 1. Copy application files
if [ -d "$SCRIPT_DIR/dist/pdf-to-md" ]; then
    echo "--> Installing standalone build to $INSTALL_DIR..."
    rm -rf "$INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
    cp -r "$SCRIPT_DIR/dist/pdf-to-md/"* "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/pdf-to-md"
    ln -sf "$INSTALL_DIR/pdf-to-md" "$BIN_DIR/pdf-to-md"
    EXEC_CMD="$INSTALL_DIR/pdf-to-md"
else
    echo "--> Standalone build not found, installing wrapper for virtualenv..."
    rm -rf "$INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
    cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"
    EXEC_CMD="$INSTALL_DIR/venv/bin/python $INSTALL_DIR/pdf_to_md_webview.py"
fi

# 2. Copy Icon
if [ -f "$SCRIPT_DIR/assets/icon.png" ]; then
    cp "$SCRIPT_DIR/assets/icon.png" "$ICON_DIR/$APP_NAME.png"
    ICON_PATH="$ICON_DIR/$APP_NAME.png"
else
    ICON_PATH="accessories-text-editor"
fi

# 3. Create Desktop Entry
cat <<EOF > "$DESKTOP_DIR/$APP_NAME.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=$APP_DISPLAY_NAME
Comment=Convert PDF documents to clean Markdown with Microsoft MarkItDown
Exec=$EXEC_CMD
Icon=$ICON_PATH
Terminal=false
Categories=Utility;Office;
Keywords=PDF;Markdown;Convert;Document;MarkItDown;
StartupNotify=true
EOF

chmod +x "$DESKTOP_DIR/$APP_NAME.desktop"

# 4. Refresh Desktop Database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

echo ""
echo "✅ Installation complete!"
echo "You can now find '$APP_DISPLAY_NAME' in your application list / launcher."
echo "Or run it from terminal: pdf-to-md"
