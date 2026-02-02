### General Style Options

|Option|Description|How to See It In Action|
|---|---|---|
|`message-style`|Styles messages shown when using commands like prefix + `:` (command prompt) or prompts.|Press `prefix + :`, and see how the prompt is styled.|
|`message-command-style`|Styles the command prompt specifically (e.g., for rename, find-window).|Try `prefix + ,` to rename a window and observe the prompt style.|
|`status-style`|Base style for the status bar at the bottom.|Look at the bottom bar of tmux.|
|`status-left-style` / `status-right-style`|Style for the left/right section of the status bar.|Add text to `status-left` or `status-right` to see changes.|
|`window-status-style`|Style for inactive windows in the status bar.|Look at the list of windows — inactive ones use this.|
|`window-status-current-style`|Style for the currently active window.|Switch between windows with `prefix + n` or `prefix + p`.|
|`window-status-activity-style`|Style when a window has activity (e.g., bell or output).|Generate output in a background window (e.g., `echo test`).|
|`pane-border-style`|Style for pane borders (inactive).|Split panes, and see the border between them.|
|`pane-active-border-style`|Style for the active pane's border.|Focus different panes with `prefix + o`.|
|`display-panes-active-colour` / `display-panes-colour`|Colors shown when using `display-panes` (`prefix + q`).|Press `prefix + q` and observe the numbers.|
|`mode-style`|Style for copy-mode or view-mode (e.g., with `prefix + [`).|Enter copy mode, and observe the highlight/cursor.|
|`clock-mode-style`|Style for the clock display (`prefix + t`).|Press `prefix + t`.|
|`copy-mode-match-style`|Style for matched text in copy-mode (like searching).|Enter copy mode, search with `/`, and see matches.|
|`popup-style`|Style for tmux popups (if supported).|Used by plugins like `fzf-tmux`, or `display-popup`.|
|`prompt-style`|Style for text prompts. Used for general prompts.|Try `rename-window`, etc.|