#!/usr/bin/env python3
# handlers/keyboard_handler.py - Keyboard event handling
from pynput import keyboard

# class KeyboardHandler:
    # def __init__(self, app):
    #     """Initialize keyboard listener
        
    #     Args:
    #         app: Reference to the main application
    #     """
    #     self.app = app
    #     self.listener = None
    #     self.pressed_keys = set()  # Track pressed keys for combinations
    #     self.start_listening()
    
    # def start_listening(self):
    #     """Start the keyboard listener"""
    #     try:
    #         self.listener = keyboard.Listener(
    #             on_press=self._on_press,
    #             on_release=self._on_release
    #         )
    #         self.listener.start()
    #     except Exception as e:
    #         print(f"Error starting keyboard listener: {e}")
    
    # def _on_press(self, key):
    #     """Handle key press events"""
    #     self.pressed_keys.add(key)
        
    #     # Alt + C combination for Clash toggle
    #     if (keyboard.Key.alt_l in self.pressed_keys and 
    #             keyboard.KeyCode(char='c') in self.pressed_keys and 
    #             len(self.pressed_keys) == 2):
    #         self.app.toggle_clash_status()
        
    #     # Alt + Q combination for exit
    #     if (keyboard.Key.alt_l in self.pressed_keys and 
    #             keyboard.KeyCode(char='q') in self.pressed_keys and 
    #             len(self.pressed_keys) == 2):
    #         self.app.exit_program()
    
    # def _on_release(self, key):
    #     """Handle key release events"""
    #     if key in self.pressed_keys:
    #         self.pressed_keys.remove(key)
    
    # def stop(self):
    #     """Stop the keyboard listener"""
    #     if self.listener:
    #         self.listener.stop()