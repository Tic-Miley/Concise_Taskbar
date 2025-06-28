#!/usr/bin/env python3
# app.py - Main application class
import tkinter as tk
from ctypes import windll

from ui.taskbar import TaskbarUI
from system.monitor import SystemMonitor
# from handlers.keyboard_handler import KeyboardHandler
from handlers.fullscreen_handler import FullscreenHandler
from utils.workspace_manager import WorkspaceManager
from utils.color_adapter import ColorAdapter

class TaskbarApp:
    def __init__(self):
        self.root = tk.Tk()
        try:
            windll.shcore.SetProcessDpiAwareness(1)
            ScaleFactor = int(windll.shcore.GetScaleFactorForDevice(0) / 100)
            self.root.tk.call("tk", "scaling", ScaleFactor)
        except Exception as e:
            print(f"Failed to set DPI awareness: {e}")

        self.root.title("Taskbar")
        self.root.overrideredirect(True)  # Remove window border
        self.root.configure(bg="#F8F8F8")  # Initial background color
        
        # Configure window size and position
        screen_width = self.root.winfo_screenwidth()  * ScaleFactor
        self.height = 22 * ScaleFactor
        self.root.geometry(f"{screen_width}x{self.height}+{0}+{0}")
        
        # Initialize components
        self.workspace_manager = WorkspaceManager(self.height)
        self.workspace_manager.set_root(self.root)
        
        self.system_monitor = SystemMonitor()
        self.ui = TaskbarUI(self.root, self.system_monitor)
        # self.keyboard_handler = KeyboardHandler(self)
        self.fullscreen_handler = FullscreenHandler(self.root, self.workspace_manager)
        
        # Initialize color adapter
        self.color_adapter = ColorAdapter(self.root, self.height)
        
        # Set up event bindings
        self.root.bind("<<ExitApplication>>", lambda e: self.exit_program())
        
        # Set up periodic updates
        self.start_update_routines()

    def start_update_routines(self):
        """Start all periodic update routines"""
        # Register UI elements with color adapter
        self.register_ui_elements()
        
        # Start color adaptation
        self.color_adapter.update_colors()
        
        # Start other regular updates
        self.ui.update_status()
        # No need for continuous work area adjustment anymore
        # self.workspace_manager.adjust_work_area()
        self.fullscreen_handler.start_monitoring()
    
    def register_ui_elements(self):
        """Register all UI elements that should adapt their colors"""
        # Add all labels and buttons from UI except special ones
        ui_elements = [
            self.ui.label_time,
            self.ui.label_date,
            self.ui.label_power,
            self.ui.label_volume,
            self.ui.label_input,
            # self.ui.label_clash,  # Handled separately as special element
            self.ui.button_tic,
            self.ui.button_files,
            self.ui.button_apps,
            self.ui.button_terminal,
            self.ui.button_music,
            self.ui.button_draft,
            self.ui.button_plan,
            self.ui.button_edge,
            self.ui.button_vscode
        ]
        self.color_adapter.add_ui_elements(ui_elements)
        
        # Register special elements with custom color handling
        self.color_adapter.register_special_element(
            self.ui.label_clash,
            lambda element, bg_color, is_dark: self._handle_clash_colors(element, bg_color, is_dark)
        )
    
    def _handle_clash_colors(self, element, bg_color, is_dark):
        """Custom color handler for Clash status label
        
        Args:
            element: The Clash label element
            bg_color: Current background color (hex)
            is_dark: Boolean indicating if background is dark
        """
        # Always update background color to match
        element.configure(bg=bg_color)
        
        # If Clash is on, use orange color, otherwise use standard contrast color
        if self.ui.is_clash_on:
            element.configure(fg="orange")
        else:
            # Use appropriate contrast color based on background
            contrast_color = "white" if is_dark else "black"
            element.configure(fg=contrast_color)
    
    # def toggle_clash_status(self):
    #     """Toggle Clash proxy status"""
    #     self.state["clash_on"] = not self.state["clash_on"]
    
    def exit_program(self):
        """Clean exit of the application"""
        try:
            # self.keyboard_handler.stop()
            self.workspace_manager.restore_work_area()  # Unregister AppBar
            self.root.destroy()
            print("Program exited successfully.")
        except Exception as e:
            print(f"Error during exit: {e}")
    
    def run(self):
        """Start the main application loop"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.exit_program()
