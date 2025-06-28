#!/usr/bin/env python3
# system/monitor.py - System monitoring functionality
import psutil
import numpy as np
from datetime import datetime
from ctypes import cast, POINTER, windll, c_uint, create_unicode_buffer, byref, WinDLL, c_long
from ctypes import wintypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import winreg

class SystemMonitor:
    def __init__(self):
        """Initialize system monitor"""
        pass
    
    def get_volume(self):
        """Get current system volume level"""
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Check for mute state first
            if volume.GetMute():
                return "静音"
            
            volume_value = volume.GetMasterVolumeLevelScalar()  # 0.0 to 1.0
            
            return f"音量 {volume_value * 100:.0f}"
            
        except Exception as e:
            print(f"Error fetching volume: {e}")
            return "音量 N/A"
    
    def get_power(self):
        """Get battery power status"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return f"电量 {battery.percent}%"
            return "Power N/A"
        except Exception as e:
            print(f"Error fetching power status: {e}")
            return "Power N/A"
    
    def get_day_of_week(self):
        """Get current day of week in Chinese"""
        today = datetime.today()
        weekday = today.weekday()
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return days[weekday]
    
    def get_time_info(self):
        """Get current date and time information"""
        now = datetime.now()
        return {
            "date": now.strftime("%m-%d"),
            "time": now.strftime("%H:%M"),
            "day_of_week": self.get_day_of_week()
        }
    
    def get_input_method(self):
        """Get current Windows input method state
        
        Returns:
            str: "中" for Chinese input, "英" for English input
        """
        try:
            # Define Windows API constants
            WM_IME_CONTROL = 0x0283
            IMC_GETCONVERSIONMODE = 0x0001
            IME_CMODE_NATIVE = 0x0001  # Chinese mode
            
            # Get user32 and imm32 DLLs
            user32 = WinDLL('user32', use_last_error=True)
            imm32 = WinDLL('imm32', use_last_error=True)
            
            # Get foreground window
            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                return "英"  # Default to English if can't get window
            
            # Get IME context for the window
            himc = imm32.ImmGetContext(hwnd)
            
            if not himc:
                # Try to get default IME window
                ime_hwnd = imm32.ImmGetDefaultIMEWnd(hwnd)
                
                if ime_hwnd:
                    # Use SendMessage to get conversion mode
                    LRESULT = c_long
                    user32.SendMessageW.restype = LRESULT
                    result = user32.SendMessageW(ime_hwnd, WM_IME_CONTROL, IMC_GETCONVERSIONMODE, 0)
                    
                    # Determine input state
                    if result & IME_CMODE_NATIVE:
                        return "中"
                    else:
                        return "英"
                return "英"
            
            # Get conversion mode through ImmGetConversionStatus
            dwConversion = wintypes.DWORD(0)
            dwSentence = wintypes.DWORD(0)
            
            ret = imm32.ImmGetConversionStatus(himc, byref(dwConversion), byref(dwSentence))
            
            # Release IME context
            imm32.ImmReleaseContext(hwnd, himc)
            
            if not ret:
                return "英"
            
            # Check if in Chinese input mode
            if dwConversion.value & IME_CMODE_NATIVE:
                return "中"
            else:
                return "英"
            
        except Exception as e:
            print(f"Error detecting input method: {e}")
            return "英"  # Default to English on error
        
    def get_clash_status(self):
        '''Check if Clash proxy is enabled in system settings
        查看Windows注册表中的代理设置
        '''
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
            proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
            proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
            winreg.CloseKey(key)
            
            # 查看到Clash默认代理端口为7890
            if proxy_enable == 1 and "7890" in proxy_server:
                return "Clash ON"
            else:
                return "Clash OFF"
        except Exception as e:
            return "Clash N/A"