#!/usr/bin/env python3
# utils/color_adapter.py - Adapts UI colors based on screen sampling
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import colorsys

class ColorAdapter:
    def __init__(self, root, taskbar_height=22, sample_count=10):
        """Initialize color adapter
        
        Args:
            root: Tkinter root window
            taskbar_height: Height of the taskbar in pixels
            sample_count: Number of points to sample for color detection
        """
        self.root = root
        self.taskbar_height = taskbar_height
        self.sample_count = sample_count
        self.sample_y = self.taskbar_height + 2  # Sample a few pixels below the taskbar
        self.ui_elements = []  # List to store UI elements for color updating
        self.special_elements = {}  # Dictionary to store elements with special color handling
        
    def add_ui_element(self, element):
        """Add a UI element to be color-updated
        
        Args:
            element: Tkinter widget to update colors for
        """
        self.ui_elements.append(element)
        
    def add_ui_elements(self, elements):
        """Add multiple UI elements to be color-updated
        
        Args:
            elements: List of Tkinter widgets to update colors for
        """
        self.ui_elements.extend(elements)
    
    def register_special_element(self, element, color_handler):
        """Register an element with special color handling
        
        Args:
            element: Tkinter widget with special color handling
            color_handler: Function that takes (element, bg_color, is_dark) and returns None
        """
        self.special_elements[element] = color_handler
        
    def sample_screen_color(self):
        """Sample colors from screen below the taskbar
        
        Returns:
            tuple: (r, g, b) color values
        """
        try:
            screen_width = self.root.winfo_screenwidth()
            sample_points = np.linspace(0, screen_width-1, self.sample_count, dtype=int)
            
            # Capture a small strip below the taskbar
            img = ImageGrab.grab(bbox=(0, self.sample_y, screen_width, self.sample_y+1))
            img_array = np.array(img)
            
            # Extract colors from sample points
            colors = [img_array[0, x] for x in sample_points]
            
            # Try to find most common color
            unique_colors, counts = np.unique(colors, axis=0, return_counts=True)
            if len(unique_colors) > 0 and np.max(counts) > 1:
                # If we have a dominant color, use it
                most_common_idx = np.argmax(counts)
                dominant_color = unique_colors[most_common_idx]
            else:
                # If no dominant color, use average
                dominant_color = np.mean(colors, axis=0).astype(int)
                
            return tuple(dominant_color)
        except Exception as e:
            print(f"Error sampling screen color: {e}")
            return (248, 248, 248)  # Default to #F8F8F8
    
    def rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color string
        
        Args:
            rgb: (r, g, b) tuple
            
        Returns:
            str: Hex color string like '#RRGGBB'
        """
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def is_dark_color(self, rgb, threshold=0.5):
        """Determine if a color is dark (needs light text)
        
        Args:
            rgb: (r, g, b) tuple
            threshold: Brightness threshold (0-1)
            
        Returns:
            bool: True if color is dark, False if light
        """
        # Convert RGB to HSV and use V (brightness) to determine if dark
        r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
        _, _, v = colorsys.rgb_to_hsv(r, g, b)
        return v < threshold
    
    def get_contrasting_color(self, rgb):
        """Get contrasting text color for given background
        
        Args:
            rgb: (r, g, b) background color
            
        Returns:
            str: 'white' or 'black' depending on contrast needs
        """
        return "white" if self.is_dark_color(rgb) else "black"
        
    def update_colors(self):
        """Update UI colors based on sampled screen color"""
        try:
            # Sample color
            rgb_color = self.sample_screen_color()
            bg_color = self.rgb_to_hex(rgb_color)
            
            # Determine appropriate text color
            is_dark = self.is_dark_color(rgb_color)
            fg_color = "white" if is_dark else "black"
            
            # Update root window background
            self.root.configure(bg=bg_color)
            
            # Update all standard UI elements
            for element in self.ui_elements:
                if element not in self.special_elements:
                    element.configure(bg=bg_color, fg=fg_color)
            
            # Update special elements with their custom handlers
            for element, handler in self.special_elements.items():
                handler(element, bg_color, is_dark)
                
            # Schedule next update
            self.root.after(1000, self.update_colors)
        except Exception as e:
            print(f"Error updating colors: {e}")
            self.root.after(1000, self.update_colors)  # Retry on next interval