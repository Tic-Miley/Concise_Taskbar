## Appearance

<div align="center">
  <img src="https://github.com/Concise_Taskbar/Soda/blob/main/images/show_taskbar.png" width="800" alt="Taskbar">
</div>

<div align="center">
  <img src="https://github.com/Concise_Taskbar/Soda/blob/main/images/show_on_desktop.png" width="800" alt="Taskbar on Desktop">
</div>

<div align="center">
  <img src="https://github.com/Concise_Taskbar/Soda/blob/main/images/show_on_edge.png" width="800" alt="Taskbar on Edge">
</div>

1. UI Components (Tkinter labels, buttons, layout)
2. System Monitoring (power, volume, time, date)
3. Event Handlers (keyboard shortcuts, button actions)
4. Utility Functions (opening folders, system commands)
5. Main Application Logic

## Project Structure Overview

```
Mac_Taskbar/
├── main.py                 # Application entry point
├── app.py                  # Main application class
├── ui/
│   ├── __init__.py
│   └── taskbar.py          # UI components and layout
├── system/
│   ├── __init__.py
│   └── monitor.py          # System monitoring (volume, power, time)
├── handlers/
│   ├── __init__.py
│   ├── keyboard_handler.py # Keyboard shortcut handling
│   └── fullscreen_handler.py # Fullscreen detection
└── utils/
    ├── __init__.py
    └── workspace_manager.py # Windows work area management
```

**Separation of Concerns**: Each class has a specific responsibility:
   - `TaskbarApp`: Central coordinator
   - `TaskbarUI`: Manages UI elements and their layout
   - `SystemMonitor`: Collects system information
   - `KeyboardHandler`: Monitors keyboard shortcuts
   - `FullscreenHandler`: Detects fullscreen applications
   - `WorkspaceManager`: Adjusts the Windows work area


## How to Run

The application can be launched by running main.py, which will instantiate the `TaskbarApp` and start the application. All the original functionality has been preserved:

- The taskbar appears at the top of the screen
- System info (time, date, volume, power) is displayed
- Application buttons work as before
- Keyboard shortcuts (Alt+C for Clash, Shift for input mode, Alt+Q to exit)
- Taskbar hides when applications are in fullscreen mode