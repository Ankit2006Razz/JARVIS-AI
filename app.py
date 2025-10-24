from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import json
import os
import platform
import subprocess
import psutil
import datetime
import socket
import webbrowser
from difflib import SequenceMatcher
import re

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

COMMAND_ALIASES = {
    # Microsoft Office
    'word': ['open word', 'ms word', 'microsoft word', 'word document', 'word processor', 'word app', 'open ms word', 'start word', 'launch word'],
    'excel': ['open excel', 'ms excel', 'microsoft excel', 'spreadsheet', 'excel sheet', 'excel app', 'open ms excel', 'start excel', 'launch excel'],
    'powerpoint': ['open powerpoint', 'ms powerpoint', 'microsoft powerpoint', 'presentation', 'ppt', 'powerpoint app', 'open ppt', 'start powerpoint', 'launch powerpoint'],
    
    # Web Browsers
    'chrome': ['open browser', 'open chrome', 'google chrome', 'chrome browser', 'chrome app', 'start chrome', 'launch chrome', 'open google chrome'],
    'google': ['open google', 'google search', 'search google', 'go to google', 'open google.com'],
    'youtube': ['open youtube', 'youtube video', 'watch youtube', 'youtube app', 'start youtube', 'launch youtube', 'go to youtube'],
    'wikipedia': ['open wikipedia', 'wikipedia search', 'wikipedia app', 'start wikipedia', 'launch wikipedia', 'go to wikipedia'],
    
    # Social Media
    'instagram': ['open instagram', 'instagram app', 'insta', 'start instagram', 'launch instagram', 'go to instagram', 'open insta'],
    'facebook': ['open facebook', 'facebook app', 'fb', 'start facebook', 'launch facebook', 'go to facebook', 'open fb'],
    'twitter': ['open twitter', 'open x', 'twitter app', 'x app', 'start twitter', 'launch twitter', 'go to twitter', 'open x.com'],
    'gmail': ['open gmail', 'gmail email', 'google mail', 'gmail app', 'start gmail', 'launch gmail', 'go to gmail', 'open mail'],
    'whatsapp': ['open whatsapp', 'whatsapp web', 'whatsapp app', 'start whatsapp', 'launch whatsapp', 'go to whatsapp', 'open whatsapp web'],
    'telegram': ['open telegram', 'telegram app', 'start telegram', 'launch telegram', 'go to telegram', 'open telegram app'],
    'discord': ['open discord', 'discord app', 'start discord', 'launch discord', 'go to discord', 'open discord app'],
    'slack': ['open slack', 'slack app', 'start slack', 'launch slack', 'go to slack', 'open slack app'],
    
    # Entertainment
    'spotify': ['open spotify', 'spotify music', 'spotify app', 'start spotify', 'launch spotify', 'go to spotify', 'open spotify app'],
    'netflix': ['open netflix', 'netflix app', 'netflix movie', 'start netflix', 'launch netflix', 'go to netflix', 'open netflix app'],
    'vlc': ['open vlc', 'vlc player', 'video player', 'start vlc', 'launch vlc', 'open vlc player'],
    
    # Development
    'vscode': ['open vscode', 'open vs code', 'visual studio code', 'code editor', 'start vscode', 'launch vscode', 'open code', 'start vs code'],
    'github': ['open github', 'github app', 'start github', 'launch github', 'go to github', 'open github app'],
    'cmd': ['open command prompt', 'open cmd', 'command line', 'terminal', 'start cmd', 'launch cmd', 'open terminal', 'command prompt'],
    
    # Graphics
    'paint': ['open paint', 'ms paint', 'paint app', 'start paint', 'launch paint', 'open ms paint', 'start ms paint'],
    'photoshop': ['open photoshop', 'adobe photoshop', 'photoshop app', 'start photoshop', 'launch photoshop', 'open adobe photoshop'],
    
    # System Tools
    'calculator': ['open calculator', 'calculator app', 'calc', 'start calculator', 'launch calculator', 'open calc', 'calculator'],
    'notepad': ['open notepad', 'open text editor', 'notepad app', 'text editor', 'start notepad', 'launch notepad', 'open text editor'],
    'explorer': ['open file explorer', 'open files', 'file explorer', 'file manager', 'start explorer', 'launch explorer', 'open file manager'],
    'settings': ['open settings', 'settings app', 'system settings', 'start settings', 'launch settings', 'open system settings'],
    'taskmanager': ['open task manager', 'task manager', 'task mgr', 'start task manager', 'launch task manager', 'open task mgr'],
    'controlpanel': ['open control panel', 'control panel', 'start control panel', 'launch control panel'],
    'devicemanager': ['open device manager', 'device manager', 'start device manager', 'launch device manager'],
    'registry': ['open registry', 'registry editor', 'regedit', 'start registry', 'launch registry', 'open regedit'],
    'systemmonitor': ['open system monitor', 'performance monitor', 'system performance', 'start system monitor', 'launch system monitor'],
    
    # System Info
    'time': ['what time is it', 'current time', 'time', 'tell me time', 'what is the time', 'show time', 'time now'],
    'date': ['what date is it', 'current date', 'date', 'today date', 'what is today', 'show date', 'today'],
    'systeminfo': ['system info', 'system information', 'computer info', 'pc info', 'system details', 'show system info'],
    'cpu': ['cpu usage', 'cpu percent', 'processor usage', 'cpu load', 'show cpu', 'cpu info'],
    'memory': ['memory usage', 'ram usage', 'memory info', 'show memory', 'memory status', 'ram info'],
    'disk': ['disk usage', 'storage usage', 'disk space', 'show disk', 'disk info', 'storage info'],
    'battery': ['battery status', 'battery info', 'battery level', 'show battery', 'battery percentage'],
    'ip': ['ip address', 'my ip', 'ip info', 'show ip', 'what is my ip', 'ip'],
    'wifi': ['wifi status', 'network status', 'wifi connection', 'show wifi', 'wifi info', 'network info'],
    
    # System Control
    'lock': ['lock screen', 'lock', 'lock computer', 'lock system', 'lock now'],
    'sleep': ['sleep', 'sleep mode', 'go to sleep', 'sleep now', 'put to sleep'],
    'shutdown': ['shutdown', 'shut down', 'power off', 'turn off', 'shutdown now', 'power down'],
    'restart': ['restart', 'reboot', 'restart computer', 'restart system', 'reboot now'],
    
    # Audio/Visual
    'volumeup': ['volume up', 'increase volume', 'louder', 'turn up volume', 'volume higher'],
    'volumedown': ['volume down', 'decrease volume', 'quieter', 'turn down volume', 'volume lower'],
    'mute': ['mute', 'mute audio', 'silence', 'mute sound', 'mute system'],
    'brightnessup': ['brightness up', 'increase brightness', 'brighter', 'turn up brightness', 'brightness higher'],
    'brightnessdown': ['brightness down', 'decrease brightness', 'darker', 'turn down brightness', 'brightness lower'],
    
    # Utilities
    'screenshot': ['take screenshot', 'screenshot', 'capture screen', 'screen capture', 'take screenshot now'],
    'updates': ['check updates', 'check for updates', 'update check', 'show updates', 'check for updates'],
    'cleanup': ['disk cleanup', 'clean disk', 'cleanup', 'clean up disk', 'disk clean'],
    'defrag': ['defragment', 'defrag', 'defragmentation', 'defrag disk', 'defragment disk'],
    'weather': ['weather', 'weather info', 'weather forecast', 'show weather', 'what is the weather'],
    'music': ['play music', 'music player', 'open music', 'start music', 'launch music'],
    'help': ['help', 'what can you do', 'available commands', 'show commands', 'help me', 'show help'],
}

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/command', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get('command', '').lower().strip()
    
    response = process_command(command)
    return jsonify({'response': response})

def find_best_match(user_input, aliases_dict):
    """Find the best matching command using advanced fuzzy matching"""
    best_match = None
    best_score = 0.5  # Lower threshold for better matching
    
    # First, try exact matches
    for key, variations in aliases_dict.items():
        for variation in variations:
            if user_input == variation:
                return key
    
    # Then try partial matches and fuzzy matching
    for key, variations in aliases_dict.items():
        for variation in variations:
            # Check if user input contains the variation
            if variation in user_input or user_input in variation:
                score = SequenceMatcher(None, user_input, variation).ratio()
                if score > best_score:
                    best_score = score
                    best_match = key
            else:
                # Fuzzy matching
                score = SequenceMatcher(None, user_input, variation).ratio()
                if score > best_score:
                    best_score = score
                    best_match = key
    
    return best_match

def process_command(command):
    """Process user command with intelligent matching and conversational responses"""
    
    matched_command = find_best_match(command, COMMAND_ALIASES)
    
    if matched_command:
        command = matched_command
    
    # Time commands
    if command in ['time', 'what time is it', 'current time']:
        current_time = datetime.datetime.now().strftime('%I:%M:%S %p')
        current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
        return f"The current time is {current_time}. Today is {current_date}."
    
    if command in ['date', 'what date is it', 'current date']:
        return f"Today's date is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."
    
    # System Info
    if command in ['systeminfo', 'system info', 'system information']:
        system = platform.system()
        release = platform.release()
        processor = platform.processor()
        return f"System: {system} {release}. Processor: {processor}. Python: {platform.python_version()}"
    
    if command in ['cpu', 'cpu usage', 'cpu percent']:
        cpu_percent = psutil.cpu_percent(interval=1)
        return f"Current CPU usage is {cpu_percent}%. Your processor is {'running smoothly' if cpu_percent < 50 else 'working hard' if cpu_percent < 80 else 'at high load'}."
    
    if command in ['memory', 'memory usage', 'ram usage']:
        memory = psutil.virtual_memory()
        return f"Memory usage: {memory.percent}%. Used: {memory.used // (1024**3)}GB / Total: {memory.total // (1024**3)}GB."
    
    if command in ['disk', 'disk usage', 'storage usage']:
        disk = psutil.disk_usage('/')
        return f"Disk usage: {disk.percent}%. Used: {disk.used // (1024**3)}GB / Total: {disk.total // (1024**3)}GB."
    
    if command in ['battery', 'battery status', 'battery info']:
        try:
            battery = psutil.sensors_battery()
            status = 'Charging' if battery.power_plugged else 'Discharging'
            return f"Battery: {battery.percent}%. Status: {status}."
        except:
            return "Battery information not available on this system."
    
    # Network
    if command in ['ip', 'ip address', 'my ip']:
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return f"Your IP address is {ip}. Hostname: {hostname}"
        except:
            return "Could not retrieve IP address."
    
    if command in ['wifi', 'network status', 'wifi connection']:
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
                if 'connected' in result.stdout.lower():
                    return "WiFi is connected and working properly."
                else:
                    return "WiFi is not connected."
            else:
                return "WiFi status check available on Windows. Your system appears to be online."
        except:
            return "Could not check WiFi status."
    
    # Web Browsers & Search
    if command in ['chrome', 'open browser', 'open chrome']:
        try:
            if platform.system() == 'Windows':
                os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Google Chrome'])
            else:
                subprocess.Popen(['google-chrome'])
            return "Opening Chrome browser for you..."
        except:
            try:
                webbrowser.open('https://www.google.com')
                return "Opening default browser..."
            except:
                return "Could not open browser. Please ensure Chrome is installed."
    
    if command in ['google', 'open google', 'google search']:
        try:
            webbrowser.open('https://www.google.com')
            return "Opening Google search engine..."
        except:
            return "Could not open Google."
    
    if command in ['youtube', 'open youtube', 'youtube video']:
        try:
            webbrowser.open('https://www.youtube.com')
            return "Opening YouTube. Enjoy watching!"
        except:
            return "Could not open YouTube."
    
    if command in ['wikipedia', 'open wikipedia', 'wikipedia search']:
        try:
            webbrowser.open('https://www.wikipedia.org')
            return "Opening Wikipedia for you..."
        except:
            return "Could not open Wikipedia."
    
    # Microsoft Office Applications
    if command in ['word', 'open word', 'ms word']:
        try:
            if platform.system() == 'Windows':
                os.startfile('C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Microsoft Word'])
            else:
                subprocess.Popen(['libreoffice', '--writer'])
            return "Opening Microsoft Word for you..."
        except:
            return "Microsoft Word not found. Please install Microsoft Office or LibreOffice."
    
    if command in ['excel', 'open excel', 'ms excel']:
        try:
            if platform.system() == 'Windows':
                os.startfile('C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Microsoft Excel'])
            else:
                subprocess.Popen(['libreoffice', '--calc'])
            return "Opening Microsoft Excel for you..."
        except:
            return "Microsoft Excel not found. Please install Microsoft Office or LibreOffice."
    
    if command in ['powerpoint', 'open powerpoint', 'ms powerpoint']:
        try:
            if platform.system() == 'Windows':
                os.startfile('C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Microsoft PowerPoint'])
            else:
                subprocess.Popen(['libreoffice', '--impress'])
            return "Opening Microsoft PowerPoint for you..."
        except:
            return "Microsoft PowerPoint not found. Please install Microsoft Office or LibreOffice."
    
    # Social Media & Communication
    if command in ['instagram', 'open instagram', 'insta']:
        try:
            webbrowser.open('https://www.instagram.com')
            return "Opening Instagram. Have fun!"
        except:
            return "Could not open Instagram."
    
    if command in ['facebook', 'open facebook', 'fb']:
        try:
            webbrowser.open('https://www.facebook.com')
            return "Opening Facebook for you..."
        except:
            return "Could not open Facebook."
    
    if command in ['twitter', 'open twitter', 'open x']:
        try:
            webbrowser.open('https://www.twitter.com')
            return "Opening Twitter/X for you..."
        except:
            return "Could not open Twitter."
    
    if command in ['gmail', 'open gmail', 'google mail']:
        try:
            webbrowser.open('https://mail.google.com')
            return "Opening Gmail. Check your emails!"
        except:
            return "Could not open Gmail."
    
    if command in ['whatsapp', 'open whatsapp', 'whatsapp web']:
        try:
            webbrowser.open('https://web.whatsapp.com')
            return "Opening WhatsApp Web for you..."
        except:
            return "Could not open WhatsApp."
    
    if command in ['telegram', 'open telegram', 'telegram app']:
        try:
            webbrowser.open('https://web.telegram.org')
            return "Opening Telegram for you..."
        except:
            return "Could not open Telegram."
    
    if command in ['discord', 'open discord', 'discord app']:
        try:
            if platform.system() == 'Windows':
                os.startfile('C:\\Users\\' + os.getenv('USERNAME') + '\\AppData\\Local\\Discord\\app-1.0.9015\\Discord.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Discord'])
            else:
                subprocess.Popen(['discord'])
            return "Opening Discord for you..."
        except:
            try:
                webbrowser.open('https://discord.com')
                return "Opening Discord in browser..."
            except:
                return "Could not open Discord."
    
    if command in ['slack', 'open slack', 'slack app']:
        try:
            if platform.system() == 'Windows':
                os.startfile('C:\\Users\\' + os.getenv('USERNAME') + '\\AppData\\Local\\slack\\slack.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Slack'])
            else:
                subprocess.Popen(['slack'])
            return "Opening Slack for you..."
        except:
            try:
                webbrowser.open('https://slack.com')
                return "Opening Slack in browser..."
            except:
                return "Could not open Slack."
    
    # Entertainment & Media
    if command in ['spotify', 'open spotify', 'spotify music']:
        try:
            if platform.system() == 'Windows':
                os.startfile('C:\\Users\\' + os.getenv('USERNAME') + '\\AppData\\Roaming\\Spotify\\Spotify.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Spotify'])
            else:
                subprocess.Popen(['spotify'])
            return "Opening Spotify. Enjoy your music!"
        except:
            try:
                webbrowser.open('https://www.spotify.com')
                return "Opening Spotify in browser..."
            except:
                return "Could not open Spotify."
    
    if command in ['netflix', 'open netflix', 'netflix movie']:
        try:
            webbrowser.open('https://www.netflix.com')
            return "Opening Netflix. Enjoy watching!"
        except:
            return "Could not open Netflix."
    
    if command in ['vlc', 'open vlc', 'vlc player']:
        try:
            if platform.system() == 'Windows':
                os.startfile('C:\\Program Files\\VideoLAN\\VLC\\vlc.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'VLC'])
            else:
                subprocess.Popen(['vlc'])
            return "Opening VLC Player for you..."
        except:
            return "VLC Player not found. Please install it."
    
    # Development & Tools
    if command in ['vscode', 'open vscode', 'visual studio code']:
        try:
            if platform.system() == 'Windows':
                os.startfile('C:\\Program Files\\Microsoft VS Code\\Code.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Visual Studio Code'])
            else:
                subprocess.Popen(['code'])
            return "Opening Visual Studio Code for you..."
        except:
            return "Visual Studio Code not found. Please install it."
    
    if command in ['github', 'open github', 'github app']:
        try:
            webbrowser.open('https://www.github.com')
            return "Opening GitHub for you..."
        except:
            return "Could not open GitHub."
    
    if command in ['cmd', 'open command prompt', 'open cmd']:
        try:
            if platform.system() == 'Windows':
                os.startfile('cmd.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Terminal'])
            else:
                subprocess.Popen(['gnome-terminal'])
            return "Opening Command Prompt for you..."
        except:
            return "Could not open Command Prompt."
    
    # Graphics & Design
    if command in ['paint', 'open paint', 'ms paint']:
        try:
            if platform.system() == 'Windows':
                os.startfile('mspaint.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Preview'])
            else:
                subprocess.Popen(['pinta'])
            return "Opening Paint for you..."
        except:
            return "Paint not found. Please install it."
    
    if command in ['photoshop', 'open photoshop', 'adobe photoshop']:
        try:
            if platform.system() == 'Windows':
                os.startfile('C:\\Program Files\\Adobe\\Adobe Photoshop 2024\\Photoshop.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Adobe Photoshop'])
            else:
                subprocess.Popen(['photoshop'])
            return "Opening Photoshop for you..."
        except:
            return "Photoshop not found. Please install it."
    
    # System Tools
    if command in ['calculator', 'open calculator', 'calc']:
        try:
            if platform.system() == 'Windows':
                os.startfile('calc.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Calculator'])
            else:
                subprocess.Popen(['gnome-calculator'])
            return "Opening Calculator for you..."
        except:
            return "Could not open Calculator."
    
    if command in ['notepad', 'open notepad', 'text editor']:
        try:
            if platform.system() == 'Windows':
                os.startfile('notepad.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'TextEdit'])
            else:
                subprocess.Popen(['gedit'])
            return "Opening Notepad for you..."
        except:
            return "Could not open Notepad."
    
    if command in ['explorer', 'open file explorer', 'file manager']:
        try:
            if platform.system() == 'Windows':
                os.startfile('explorer.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '.'])
            else:
                subprocess.Popen(['nautilus', '.'])
            return "Opening File Explorer for you..."
        except:
            return "Could not open File Explorer."
    
    if command in ['settings', 'open settings', 'system settings']:
        try:
            if platform.system() == 'Windows':
                os.startfile('ms-settings:')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'System Preferences'])
            else:
                subprocess.Popen(['gnome-control-center'])
            return "Opening Settings for you..."
        except:
            return "Could not open Settings."
    
    if command in ['taskmanager', 'open task manager', 'task mgr']:
        try:
            if platform.system() == 'Windows':
                os.startfile('taskmgr.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Activity Monitor'])
            else:
                subprocess.Popen(['gnome-system-monitor'])
            return "Opening Task Manager for you..."
        except:
            return "Could not open Task Manager."
    
    if command in ['controlpanel', 'open control panel', 'control panel']:
        try:
            if platform.system() == 'Windows':
                os.startfile('control.exe')
            else:
                return "Control Panel is Windows only."
        except:
            return "Could not open Control Panel."
    
    if command in ['devicemanager', 'open device manager', 'device manager']:
        try:
            if platform.system() == 'Windows':
                os.startfile('devmgmt.msc')
            else:
                return "Device Manager is Windows only."
        except:
            return "Could not open Device Manager."
    
    if command in ['registry', 'open registry', 'registry editor']:
        try:
            if platform.system() == 'Windows':
                os.startfile('regedit.exe')
            else:
                return "Registry Editor is Windows only."
        except:
            return "Could not open Registry Editor."
    
    if command in ['systemmonitor', 'open system monitor', 'performance monitor']:
        try:
            if platform.system() == 'Windows':
                os.startfile('perfmon.exe')
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', '-a', 'Activity Monitor'])
            else:
                subprocess.Popen(['gnome-system-monitor'])
            return "Opening System Monitor for you..."
        except:
            return "Could not open System Monitor."
    
    # System Control
    if command in ['lock', 'lock screen', 'lock computer']:
        try:
            if platform.system() == 'Windows':
                os.system('rundll32.exe user32.dll,LockWorkStation')
            elif platform.system() == 'Darwin':
                os.system('open -a /System/Library/CoreServices/ScreenLock.app')
            else:
                os.system('gnome-screensaver-command -l')
            return "Locking your screen now..."
        except:
            return "Could not lock screen."
    
    if command in ['sleep', 'sleep mode', 'go to sleep']:
        try:
            if platform.system() == 'Windows':
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            elif platform.system() == 'Darwin':
                os.system('osascript -e "tell application \\"System Events\\" to sleep"')
            else:
                os.system('systemctl suspend')
            return "Going to sleep mode now..."
        except:
            return "Could not enter sleep mode."
    
    if command in ['shutdown', 'shut down', 'power off']:
        try:
            if platform.system() == 'Windows':
                os.system('shutdown /s /t 30')
            elif platform.system() == 'Darwin':
                os.system('osascript -e "tell application \\"System Events\\" to shut down"')
            else:
                os.system('shutdown -h +1')
            return "System will shutdown in 30 seconds. Save your work!"
        except:
            return "Could not shutdown system."
    
    if command in ['restart', 'reboot', 'restart computer']:
        try:
            if platform.system() == 'Windows':
                os.system('shutdown /r /t 30')
            elif platform.system() == 'Darwin':
                os.system('osascript -e "tell application \\"System Events\\" to restart"')
            else:
                os.system('shutdown -r +1')
            return "System will restart in 30 seconds. Save your work!"
        except:
            return "Could not restart system."
    
    # Volume Control
    if command in ['volumeup', 'volume up', 'increase volume']:
        try:
            if platform.system() == 'Windows':
                os.system('nircmd.exe changesysvolume 5000')
            return "Volume increased."
        except:
            return "Could not adjust volume."
    
    if command in ['volumedown', 'volume down', 'decrease volume']:
        try:
            if platform.system() == 'Windows':
                os.system('nircmd.exe changesysvolume -5000')
            return "Volume decreased."
        except:
            return "Could not adjust volume."
    
    if command in ['mute', 'mute audio', 'silence']:
        try:
            if platform.system() == 'Windows':
                os.system('nircmd.exe mutesysvolume 1')
            return "System muted."
        except:
            return "Could not mute system."
    
    # Brightness Control
    if command in ['brightnessup', 'brightness up', 'brighter']:
        return "Brightness increased. (Note: Requires system-specific tools)"
    
    if command in ['brightnessdown', 'brightness down', 'darker']:
        return "Brightness decreased. (Note: Requires system-specific tools)"
    
    # Utility Commands
    if command in ['weather', 'weather info', 'weather forecast']:
        return "Weather information requires internet connection. Please check your weather app or visit weather.com"
    
    if command in ['music', 'play music', 'music player']:
        try:
            if platform.system() == 'Windows':
                os.startfile('wmplayer.exe')
            return "Opening media player..."
        except:
            return "Could not open media player."
    
    if command in ['screenshot', 'take screenshot', 'capture screen']:
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            screenshot.save('screenshot.png')
            return "Screenshot saved as screenshot.png in your project folder."
        except:
            return "Could not take screenshot. Please install Pillow: pip install Pillow"
    
    if command in ['updates', 'check updates', 'check for updates']:
        try:
            if platform.system() == 'Windows':
                os.system('start ms-settings:windowsupdate')
            return "Opening Windows Update..."
        except:
            return "Could not check updates."
    
    if command in ['cleanup', 'disk cleanup', 'clean disk']:
        try:
            if platform.system() == 'Windows':
                os.system('cleanmgr.exe')
            return "Opening Disk Cleanup..."
        except:
            return "Could not open Disk Cleanup."
    
    if command in ['defrag', 'defragment', 'defragmentation']:
        try:
            if platform.system() == 'Windows':
                os.system('defrag C: /U /V')
            return "Defragmentation started..."
        except:
            return "Could not start defragmentation."
    
    # Help
    if command in ['help', 'what can you do', 'available commands']:
        return """I can help with:
        
SYSTEM INFO: Time, Date, System Info, CPU/Memory/Disk Usage, Battery Status, IP Address, WiFi Status

APPLICATIONS: Word, Excel, PowerPoint, Chrome, YouTube, Wikipedia, Instagram, Facebook, Twitter, Gmail, WhatsApp, Telegram, Discord, Slack, Spotify, Netflix, VLC, VS Code, GitHub, Paint, Photoshop, Calculator, Notepad, File Explorer, Settings, Task Manager, Control Panel, Device Manager, Registry Editor, System Monitor

SYSTEM CONTROL: Lock Screen, Sleep Mode, Shutdown, Restart, Volume Control, Brightness Control

UTILITIES: Take Screenshot, Check Updates, Disk Cleanup, Defragmentation, Weather Info, Play Music

Try saying or typing: "open word", "what time is it", "cpu usage", "lock screen", or any application name!"""
    
    return f"I didn't quite understand '{command}'. Let me help you! Try commands like: 'open word', 'what time is it', 'system info', 'open youtube', 'lock screen', 'cpu usage', or type 'help' to see all available commands."

if __name__ == '__main__':
    app.run(debug=True, port=5000)
