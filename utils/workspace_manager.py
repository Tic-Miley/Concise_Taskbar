#!/usr/bin/env python3
# utils/workspace_manager.py - Manages workspace area adjustments
from ctypes import windll, wintypes, byref, c_int, Structure, sizeof, c_ulong, pointer

# Windows API constants
GWL_EXSTYLE = -20
WS_EX_TOPMOST = 0x0008
WS_EX_TOOLWINDOW = 0x0080
WS_EX_NOACTIVATE = 0x08000000
HWND_TOPMOST = -1
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040
SPI_GETWORKAREA = 0x0030
SPI_SETWORKAREA = 0x002F

class APPBARDATA(Structure):
    _fields_ = [
        ("cbSize", c_int),
        ("hWnd", wintypes.HWND),
        ("uCallbackMessage", c_int),
        ("uEdge", c_int),
        ("rc", wintypes.RECT),
        ("lParam", wintypes.LPARAM)
    ]

# AppBar messages
ABM_NEW = 0x00000000
ABM_REMOVE = 0x00000001
ABM_QUERYPOS = 0x00000002
ABM_SETPOS = 0x00000003
ABM_GETSTATE = 0x00000004
ABM_GETTASKBARPOS = 0x00000005
ABM_ACTIVATE = 0x00000006
ABM_GETAUTOHIDEBAR = 0x00000007
ABM_SETAUTOHIDEBAR = 0x00000008
ABM_WINDOWPOSCHANGED = 0x00000009
ABM_SETSTATE = 0x0000000A

# AppBar edges
ABE_LEFT = 0
ABE_TOP = 1
ABE_RIGHT = 2
ABE_BOTTOM = 3

# AppBar states
ABS_AUTOHIDE = 0x0000001
ABS_ALWAYSONTOP = 0x0000002

class WorkspaceManager:
    def __init__(self, taskbar_height=22):
        """Initialize workspace manager
        
        Args:
            taskbar_height: Height of the taskbar in pixels
        """
        self.taskbar_height = taskbar_height
        self.root = None
        self.appbar_data = None
        self.registered = False
        self.is_visible = True
        
    def set_root(self, root):
        """Set the tkinter root window reference
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        
        # Get the window handle
        hwnd = int(self.root.winfo_id())
        
        # Set the window as a tool window (doesn't appear in Alt+Tab)
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        windll.user32.SetWindowLongW(
            hwnd, 
            GWL_EXSTYLE, 
            style | WS_EX_TOOLWINDOW | WS_EX_TOPMOST | WS_EX_NOACTIVATE
        )
        
        # Set window always on top with proper flags
        windll.user32.SetWindowPos(
            hwnd,
            HWND_TOPMOST,
            0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW
        )
        
        # Try both AppBar and direct work area adjustment methods
        self.register_app_bar()
        self.manual_adjust_work_area()
        
    def register_app_bar(self):
        """Register the window as a Windows AppBar, like the taskbar"""
        if not self.root or self.registered:
            return
            
        # Initialize APPBARDATA structure
        self.appbar_data = APPBARDATA()
        self.appbar_data.cbSize = sizeof(APPBARDATA)
        self.appbar_data.hWnd = int(self.root.winfo_id())
        self.appbar_data.uEdge = ABE_TOP
        
        # Register as new AppBar
        result = windll.shell32.SHAppBarMessage(ABM_NEW, byref(self.appbar_data))
        if result:
            self.registered = True
            
            # Set the position
            screen_width = self.root.winfo_screenwidth()
            
            # Define the AppBar area - top of the screen
            self.appbar_data.rc.left = 0
            self.appbar_data.rc.top = 0
            self.appbar_data.rc.right = screen_width
            self.appbar_data.rc.bottom = self.taskbar_height
            
            # Query Windows for the position (might adjust our requested position)
            windll.shell32.SHAppBarMessage(ABM_QUERYPOS, byref(self.appbar_data))
            
            # Set the position
            windll.shell32.SHAppBarMessage(ABM_SETPOS, byref(self.appbar_data))
            
            # Notify the system when the position changes
            windll.shell32.SHAppBarMessage(ABM_WINDOWPOSCHANGED, byref(self.appbar_data))
            
            print("AppBar registered successfully")
        else:
            print("Failed to register AppBar, falling back to manual work area adjustment")
            self.manual_adjust_work_area()
    
    def manual_adjust_work_area(self):
        """Directly adjust the Windows work area as fallback"""
        try:
            # Get current work area
            work_area = wintypes.RECT()
            windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, byref(work_area), 0)
            
            # Store original work area if we haven't yet
            if not hasattr(self, 'original_work_area'):
                self.original_work_area = wintypes.RECT()
                self.original_work_area.left = work_area.left
                self.original_work_area.top = work_area.top
                self.original_work_area.right = work_area.right
                self.original_work_area.bottom = work_area.bottom
            
            # Check if work area needs adjustment
            if work_area.top < self.taskbar_height:
                # Adjust work area to account for taskbar height
                work_area.top = self.taskbar_height
                
                # Apply the new work area with broadcast to all windows
                windll.user32.SystemParametersInfoW(
                    SPI_SETWORKAREA, 
                    0, 
                    byref(work_area),
                    0x01  # SPIF_SENDCHANGE - Broadcast the change to all windows
                )
                print(f"Work area manually adjusted: top={work_area.top}")
                
                # Schedule a check to ensure the work area stays adjusted
                if self.root:
                    self.root.after(5000, self.check_work_area)
            
        except Exception as e:
            print(f"Error in manual_adjust_work_area: {e}")
    
    def check_work_area(self):
        """Check and re-adjust the work area if needed"""
        # Only check if we're visible
        if self.is_visible:
            work_area = wintypes.RECT()
            windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, byref(work_area), 0)
            
            # If work area has been reset, adjust it again
            if work_area.top < self.taskbar_height:
                print("Work area was reset, readjusting...")
                self.manual_adjust_work_area()
            
        # Schedule next check
        if self.root:
            self.root.after(1000, self.check_work_area)
    
    def hide(self):
        """Hide the taskbar"""
        if self.root and self.is_visible:
            self.root.withdraw()
            self.is_visible = False
            
            # Restore original work area when hiding
            if hasattr(self, 'original_work_area'):
                windll.user32.SystemParametersInfoW(
                    SPI_SETWORKAREA, 
                    0, 
                    byref(self.original_work_area),
                    0x01  # SPIF_SENDCHANGE
                )
            
    def show(self):
        """Show the taskbar"""
        if self.root and not self.is_visible:
            self.root.deiconify()
            self.is_visible = True
            
            # Ensure it stays on top after showing
            hwnd = int(self.root.winfo_id())
            windll.user32.SetWindowPos(
                hwnd,
                HWND_TOPMOST,
                0, 0, 0, 0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW
            )
            
            # Re-adjust work area
            self.manual_adjust_work_area()
            
    def adjust_work_area(self):
        """Legacy method for compatibility, calls manual_adjust_work_area"""
        self.manual_adjust_work_area()
            
    def restore_work_area(self):
        """Remove AppBar status and restore original Windows work area"""
        # Unregister AppBar if registered
        if self.registered and self.appbar_data:
            windll.shell32.SHAppBarMessage(ABM_REMOVE, byref(self.appbar_data))
            self.registered = False
            print("AppBar unregistered")
        
        # Restore original work area if we stored it
        if hasattr(self, 'original_work_area'):
            windll.user32.SystemParametersInfoW(
                SPI_SETWORKAREA, 
                0, 
                byref(self.original_work_area),
                0x01  # SPIF_SENDCHANGE
            )
            print("Original work area restored")