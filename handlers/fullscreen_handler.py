#!/usr/bin/env python3
# handlers/fullscreen_handler.py - Fullscreen detection and handling
from ctypes import windll, wintypes, byref, create_unicode_buffer

class FullscreenHandler:
    def __init__(self, root, workspace_manager=None):
        """Initialize fullscreen detection
        
        Args:
            root: Reference to the tkinter root window
            workspace_manager: Reference to the WorkspaceManager
        """
        self.root = root
        self.workspace_manager = workspace_manager
        self.last_state = False  # Track last fullscreen state to avoid unnecessary actions
    
    def is_fullscreen(self):
        """Detect if there is a fullscreen window active"""
        try:
            # Get foreground window handle
            hwnd_foreground = windll.user32.GetForegroundWindow()
            if not hwnd_foreground:
                return False
                
            # Get our own window handle to ignore it
            own_hwnd = int(self.root.winfo_id())
            if hwnd_foreground == own_hwnd:
                return False
            
            # Get window rect
            rect = wintypes.RECT()
            windll.user32.GetWindowRect(hwnd_foreground, byref(rect))
            
            # Get window class name
            class_name = create_unicode_buffer(256)
            windll.user32.GetClassNameW(hwnd_foreground, class_name, 256)
            
            # Check if it's the desktop window
            if class_name.value in ["Progman", "WorkerW", "Shell_TrayWnd", "Shell_SecondaryTrayWnd"]:
                return False
            
            # Get screen dimensions
            screen_width = windll.user32.GetSystemMetrics(0)
            screen_height = windll.user32.GetSystemMetrics(1)
            
            # Check if window covers the entire screen
            return (
                rect.left <= 0 and rect.top <= 0 and
                rect.right >= screen_width and rect.bottom >= screen_height
            )
        except Exception as e:
            print(f"Error detecting fullscreen state: {e}")
            return False
    
    def monitor_fullscreen(self):
        """Hide or show the taskbar based on fullscreen state"""
        is_full = self.is_fullscreen()
        
        # Only take action if the state has changed
        if is_full != self.last_state:
            self.last_state = is_full
            
            if is_full:
                if self.workspace_manager:
                    self.workspace_manager.hide()
                else:
                    self.root.withdraw()  # Fallback to direct hiding
            else:
                if self.workspace_manager:
                    self.workspace_manager.show()
                else:
                    self.root.deiconify()  # Fallback to direct showing
    
    def start_monitoring(self):
        """Start periodic monitoring of fullscreen state"""
        self.monitor_fullscreen()
        self.root.after(1000, self.start_monitoring)  # Check every half second