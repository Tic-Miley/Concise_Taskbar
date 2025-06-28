#!/usr/bin/env python3
# ui/taskbar.py - TaskbarUI component handling all UI elements
import tkinter as tk
import os
import webbrowser

class TaskbarUI:
    def __init__(self, root, system_monitor):
        self.root = root
        self.system_monitor = system_monitor
        
        # Default style settings
        self.DEFAULT_FONT = ("Microsoft YaHei", 14, "bold")
        self.DEFAULT_FONT_SMALL = ("Microsoft YaHei", 13, "bold")
        self.DEFAULT_FG = "black"
        self.DEFAULT_BG = "#F8F8F8"
        self.DEFAULT_CURSOR = "hand2"
        
        # Special color flags
        self.is_clash_on = False
        
        # Set up all UI elements
        self.setup_ui()
        
    def setup_ui(self):
        """Set up all UI labels and buttons"""
        # Time label
        self.label_time = tk.Label(self.root, font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, anchor="w")
        self.label_time.pack(side="right", padx=16)
        
        # Date label
        self.label_date = tk.Label(self.root, font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, anchor="w")
        self.label_date.pack(side="right", padx=8)
        
        # Power label
        self.label_power = tk.Label(self.root, font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, anchor="w")
        self.label_power.pack(side="right", padx=8)
        
        # Volume label
        self.label_volume = tk.Label(self.root, font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, anchor="w")
        self.label_volume.pack(side="right", padx=8)
        
        # Input method label
        self.label_input = tk.Label(self.root, font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, anchor="w")
        self.label_input.pack(side="right", padx=8)

        # Clash status label
        self.label_clash = tk.Label(self.root, font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, anchor="w")
        self.label_clash.pack(side="right", padx=8)
        
        # Tic brand
        self.button_tic = tk.Label(self.root, text="江麦里   |", font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, cursor=self.DEFAULT_CURSOR)
        # self.button_tic = tk.Label(self.root, text=" ", font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, cursor=self.DEFAULT_CURSOR)
        self.button_tic.pack(side="left", padx=16)
        self.button_tic.bind("<Button-1>", self.open_folder_computer)
        self.button_tic.bind("<Button-3>", self.open_system_menu)
        
        # Files button
        self.button_files = tk.Label(self.root, text="文件", font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, cursor=self.DEFAULT_CURSOR)
        self.button_files.pack(side="left", padx=8)
        self.button_files.bind("<Button-1>", self.open_folder_d6)
        
        # Apps button
        self.button_apps = tk.Label(self.root, text="应用", font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, cursor=self.DEFAULT_CURSOR)
        self.button_apps.pack(side="left", padx=8)
        self.button_apps.bind("<Button-1>", self.open_folder_list)
        
        # Terminal button
        self.button_terminal = tk.Label(self.root, text="终端", font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, cursor=self.DEFAULT_CURSOR)
        self.button_terminal.pack(side="left", padx=8)
        self.button_terminal.bind("<Button-1>", self.open_folder_terminal)
        
        # Music button
        self.button_music = tk.Label(self.root, text="音乐", font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, cursor=self.DEFAULT_CURSOR)
        self.button_music.pack(side="left", padx=8)
        self.button_music.bind("<Button-1>", self.open_folder_music)
        
        # Draft button
        self.button_draft = tk.Label(self.root, text="草稿", font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, cursor=self.DEFAULT_CURSOR)
        self.button_draft.pack(side="left", padx=8)
        self.button_draft.bind("<Button-1>", self.open_folder_onenote)
        
        # Plan button
        self.button_plan = tk.Label(self.root, text="计划", font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, cursor=self.DEFAULT_CURSOR)
        self.button_plan.pack(side="left", padx=8)
        self.button_plan.bind("<Button-1>", self.open_folder_todo)

        # Edge button
        self.button_edge = tk.Label(self.root, text="互联", font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, cursor=self.DEFAULT_CURSOR)
        self.button_edge.pack(side="left", padx=8)
        self.button_edge.bind("<Button-1>", self.open_folder_edge)
        
        # VSCode button
        self.button_vscode = tk.Label(self.root, text="VSCode", font=self.DEFAULT_FONT, fg=self.DEFAULT_FG, bg=self.DEFAULT_BG, cursor=self.DEFAULT_CURSOR)
        self.button_vscode.pack(side="left", padx=8)
        self.button_vscode.bind("<Button-1>", self.open_folder_vscode)
        
    def update_status(self):
        """Update all status information in the UI"""
        # Get input method state directly from system_monitor
        clash_status = self.system_monitor.get_clash_status()
        input_mode = self.system_monitor.get_input_method()
        volume_status = self.system_monitor.get_volume()
        power_status = self.system_monitor.get_power()
        time_info = self.system_monitor.get_time_info()
        
        # Update status text (but not colors - ColorAdapter handles that)
        self.label_clash.config(text="Clash")
        
        # Track clash status for special color handling
        self.is_clash_on = (clash_status == "Clash ON")
        
        self.label_input.config(text=input_mode)
        self.label_volume.config(text=volume_status)
        self.label_power.config(text=power_status)
        self.label_date.config(text=time_info["date"])
        self.label_time.config(text=time_info["time"])
        
        # Schedule next update
        self.root.after(1000, self.update_status)
    
    # Button click handlers
    def open_folder_computer(self, event=None):
        os.system('explorer ::{20D04FE0-3AEA-1069-A2D8-08002B30309D}')
    
    def open_system_menu(self, event=None):
        system_menu = tk.Menu(self.root, tearoff=0, font=self.DEFAULT_FONT_SMALL)
        system_menu.add_command(label="重启", command=self.restart_computer)
        system_menu.add_command(label="关机", command=self.shutdown_computer)
        system_menu.add_command(label="睡眠", command=self.put_computer_to_sleep)
        system_menu.add_command(label="设置", command=self.open_settings)
        system_menu.add_command(label="面板", command=self.open_control_panel)
        system_menu.add_command(label="退出", command=self.exit_program)
        
        system_menu.post(event.x_root, event.y_root)
    
    def exit_program(self):
        """Exit program through app reference"""
        # This will be connected to the main app instance later
        self.root.event_generate('<<ExitApplication>>')
    
    def restart_computer(self):
        # os.system('shutdown /r /t 1')
        pass

    def shutdown_computer(self):
        # os.system('shutdown /s /t 1')
        pass

    def put_computer_to_sleep(self):
        # os.system('rundll32 powrprof.dll,SetSuspendState 0,1,0')
        pass

    def open_settings(self):
        # webbrowser.open('ms-settings:')
        pass

    def open_control_panel(self):
        # os.startfile('::{26EE0668-A00A-44D7-9371-BEB064C98683}')
        pass
    
    def open_folder_d6(self, event=None):
        folder_path = "D:\\Web\\学习\\第六学期"
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            print(f"路径不存在: {folder_path}")
    
    def open_folder_list(self, event=None):
        folder_path = "D:\\Tic_Programs\\# List"
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            print(f"路径不存在: {folder_path}")
    
    def open_folder_terminal(self, event=None):
        folder_path = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            print(f"路径不存在: {folder_path}")
    
    def open_folder_music(self, event=None):
        folder_path = "D:\\Tic_Programs\\CloudMusic\\cloudmusic.exe"
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            print(f"路径不存在: {folder_path}")
    
    def open_folder_onenote(self, event=None):
        folder_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE"
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            print(f"路径不存在: {folder_path}")
    
    def open_folder_todo(self, event=None):
        folder_path = "D:\\Tic_Programs\\# List\\Microsoft To Do.lnk"
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            print(f"路径不存在: {folder_path}")

    def open_folder_edge(self, event=None):
        folder_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            print(f"路径不存在: {folder_path}")
    
    def open_folder_vscode(self, event=None):
        folder_path = "D:\\Tic_Programs\\Microsoft VS Code\\Code.exe"
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            print(f"路径不存在: {folder_path}")