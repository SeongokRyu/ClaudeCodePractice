#!/bin/bash
#
# Notification Hook: Send desktop notifications
#
# This hook runs when Claude produces a notification.
# It auto-detects macOS vs Linux and uses the appropriate notification system.
#
# Input: JSON on stdin with notification details
#

# Read the JSON input from stdin
INPUT=$(cat)

# Extract the notification message
TITLE=$(echo "$INPUT" | jq -r '.title // "Claude Code"')
MESSAGE=$(echo "$INPUT" | jq -r '.message // "Task complete"')

# Truncate long messages for desktop notification
if [ ${#MESSAGE} -gt 200 ]; then
  MESSAGE="${MESSAGE:0:197}..."
fi

# Detect OS and send notification
case "$(uname -s)" in
  Darwin)
    # macOS: use osascript
    osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\"" 2>/dev/null
    ;;
  Linux)
    # Linux: try notify-send (requires libnotify)
    if command -v notify-send &> /dev/null; then
      notify-send "$TITLE" "$MESSAGE" 2>/dev/null
    elif command -v zenity &> /dev/null; then
      # Fallback: zenity notification
      zenity --notification --text="$TITLE: $MESSAGE" 2>/dev/null &
    fi
    ;;
  CYGWIN*|MINGW*|MSYS*)
    # Windows (Git Bash): use PowerShell toast
    powershell.exe -Command "
      [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > \$null
      \$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
      \$textNodes = \$template.GetElementsByTagName('text')
      \$textNodes.Item(0).AppendChild(\$template.CreateTextNode('$TITLE'))
      \$textNodes.Item(1).AppendChild(\$template.CreateTextNode('$MESSAGE'))
      \$toast = [Windows.UI.Notifications.ToastNotification]::new(\$template)
      [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude Code').Show(\$toast)
    " 2>/dev/null
    ;;
esac

exit 0
