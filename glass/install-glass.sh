#!/usr/bin/env bash
# Claudy Theme — instalador de Glass Mode
set -e

echo "Claudy Theme · Glass Mode"
echo "========================="
echo ""

if ! command -v code >/dev/null 2>&1; then
  echo "Error: no encuentro el comando 'code' (VSCode CLI) en el PATH."
  echo "Abri VSCode -> Command Palette -> 'Shell Command: Install code command in PATH'."
  exit 1
fi

echo "Instalando la extension Custom UI Style..."
code --install-extension subframe7536.custom-ui-style --force

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "Extension instalada. Para activar el glass:"
echo ""
echo "  1. Command Palette -> 'Preferences: Open User Settings (JSON)'"
echo "  2. Pega adentro de las llaves el contenido de:"
echo "       $DIR/claudy-glass.jsonc"
echo "  3. Command Palette -> 'Custom UI Style: Enable' -> recarga VSCode"
echo ""
echo "Toggle del glass (cuando quieras):"
echo "  Apagar:   Command Palette -> 'Custom UI Style: Disable' -> recarga"
echo "  Encender: Command Palette -> 'Custom UI Style: Enable'  -> recarga"
echo ""
echo "Nota: Custom UI Style parchea VSCode; vas a ver un aviso de 'instalacion"
echo "corrupta'. Es esperado. Tras cada update de VSCode hay que hacer Enable de nuevo."
