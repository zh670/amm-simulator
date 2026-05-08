#!/bin/bash
# Double-click on macOS to open the local BloomMind preview page in default browser.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
open "$SCRIPT_DIR/preview_bloommind.html"
