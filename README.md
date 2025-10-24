# Jarvis AI Assistant - Complete Project

<img width="1366" height="768" alt="screenshot" src="https://github.com/user-attachments/assets/0d365d38-6cbf-4810-8736-52c61f94db56" />


A fully functional AI assistant with 60+ system commands and 30+ quick actions. Built with Flask backend and modern HTML/CSS/JS frontend.

## Features

- **60+ System Commands**: Execute system operations directly
- **30+ Quick Actions**: One-click command execution
- **Voice Input/Output**: Speak commands and hear responses
- **Voice Settings**: Customize voice, speech rate, and volume
- **Notes & Tasks**: Add, save, and manage notes
- **Real-time Chat**: Interactive conversation interface
- **Cross-platform**: Works on Windows, Mac, and Linux
- **Modern UI**: Dark theme with glassmorphism effects

## System Commands

### Time & Date
- Current time
- Current date
- Day of week

### System Information
- System info
- CPU usage
- Memory usage
- Disk usage
- Battery status
- Network status
- IP address
- WiFi status

### Application Launcher
- Open browser
- Open calculator
- Open notepad
- Open file explorer
- Open settings
- Open task manager
- Play music

### System Control
- Lock screen
- Sleep mode
- Shutdown
- Restart
- Volume up/down
- Mute
- Brightness up/down

### Utilities
- Take screenshot
- Clear cache
- Check updates
- Disk cleanup
- Defragment disk
- System backup

## Quick Actions (30+)<img width="1024" height="403" alt="linkedinposter" src="https://github.com/user-attachments/assets/1afd6491-df48-4a98-8776-f7225e02eaff" />


1. Current Time
2. Weather Info
3. Open Browser
4. Play Music
5. System Info
6. CPU Usage
7. Memory Usage
8. Disk Usage
9. Battery Status
10. WiFi Status
11. IP Address
12. Open Calculator
13. Open Notepad
14. Take Screenshot
15. Lock Screen
16. Sleep Mode
17. Shutdown
18. Restart
19. Volume Up
20. Volume Down
21. Mute
22. Brightness Up
23. Brightness Down
24. Open File Explorer
25. Open Settings
26. Open Task Manager
27. Clear Cache
28. Check Updates
29. Network Status
30. Disk Cleanup
31. Defragment Disk
32. System Backup

## Installation

### Requirements
- Python 3.7+
- pip

### Setup

1. **Install dependencies**:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. **Run the application**:
\`\`\`bash
python app.py
\`\`\`

3. **Open in browser**:
\`\`\`
http://localhost:5000
\`\`\`

## Project Structure

\`\`\`
jarvis-ai/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── system_commands.json   # Command definitions
├── README.md             # This file
├── static/
│   ├── index.html        # Main HTML
│   ├── style.css         # Styling
│   └── script.js         # Frontend logic
└── templates/
    └── index.html        # Flask template
\`\`\`

## Usage

### Text Commands
Type any command in the message input and press Enter or click Send.

### Voice Commands
Click the microphone button to speak commands. The system will recognize and execute them.

### Quick Actions
Click any quick action button in the sidebar for instant command execution.

### Notes
- Add notes using the text input or voice
- Save notes to local storage
- Clear all notes when needed

### Voice Settings
- Choose between male and female voices
- Adjust speech rate (0.5x - 2x)
- Control volume (0% - 100%)
- Enable/disable wake word
- Enable/disable voice response

## Supported Platforms

- **Windows**: Full support for all commands
- **macOS**: Most commands supported
- **Linux**: Most commands supported

## Troubleshooting

### Voice not working
- Check browser microphone permissions
- Ensure microphone is connected
- Try refreshing the page

### Commands not executing
- Check system permissions
- Ensure required applications are installed
- Try running as administrator (Windows)

### Port already in use
- Change port in app.py: `app.run(port=5001)`
- Or kill process using port 5000

## API Endpoints

### POST /api/command
Execute a system command

**Request**:
\`\`\`json
{
  "command": "what time is it"
}
\`\`\`

**Response**:
\`\`\`json
{
  "response": "The current time is 11:24:57 pm. Today is 21/10/2025."
}
\`\`\`

## Customization

### Add New Commands
Edit `system_commands.json` and add new command definitions.

### Add New Quick Actions
Edit `QUICK_ACTIONS` array in `static/script.js`.

### Change Colors
Modify CSS variables in `static/style.css`:
\`\`\`css
:root {
    --primary-color: #00d4ff;
    --secondary-color: #ff6b35;
    /* ... */
}
\`\`\`

## License

MIT License - Feel free to use and modify

## Support

For issues or questions, please check the troubleshooting section or create an issue.

---

**Jarvis AI Assistant v2.0** - Your personal AI assistant with 100% FREE models
