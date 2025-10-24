// Jarvis AI Assistant - Main Script
// 60+ System Commands & 40+ Quick Actions

const QUICK_ACTIONS = [
  // Important System Commands (Top Priority)
  { name: "Current Time", icon: "⏰", command: "what time is it" },
  { name: "System Info", icon: "💻", command: "system info" },
  { name: "CPU Usage", icon: "⚙️", command: "cpu usage" },
  { name: "Memory Usage", icon: "🧠", command: "memory usage" },
  { name: "Battery Status", icon: "🔋", command: "battery status" },

  // Web Browsers & Search
  { name: "Open Browser", icon: "🌐", command: "open browser" },
  { name: "Google Search", icon: "🔍", command: "open google" },
  { name: "YouTube", icon: "📺", command: "open youtube" },
  { name: "Wikipedia", icon: "📚", command: "open wikipedia" },

  // Microsoft Office
  { name: "MS Word", icon: "📝", command: "open word" },
  { name: "MS Excel", icon: "📊", command: "open excel" },
  { name: "PowerPoint", icon: "🎨", command: "open powerpoint" },

  // Social Media & Communication
  { name: "Instagram", icon: "📷", command: "open instagram" },
  { name: "Facebook", icon: "👥", command: "open facebook" },
  { name: "Twitter/X", icon: "𝕏", command: "open twitter" },
  { name: "Gmail", icon: "✉️", command: "open gmail" },
  { name: "WhatsApp", icon: "💬", command: "open whatsapp" },
  { name: "Telegram", icon: "✈️", command: "open telegram" },
  { name: "Discord", icon: "🎮", command: "open discord" },
  { name: "Slack", icon: "💼", command: "open slack" },

  // Entertainment & Media
  { name: "Spotify", icon: "🎵", command: "open spotify" },
  { name: "Netflix", icon: "🎬", command: "open netflix" },
  { name: "VLC Player", icon: "▶️", command: "open vlc" },
  { name: "Play Music", icon: "🎧", command: "play music" },

  // Development & Tools
  { name: "VS Code", icon: "💻", command: "open vscode" },
  { name: "GitHub", icon: "🐙", command: "open github" },
  { name: "Command Prompt", icon: "⌨️", command: "open command prompt" },

  // Graphics & Design
  { name: "Paint", icon: "🎨", command: "open paint" },
  { name: "Photoshop", icon: "🖼️", command: "open photoshop" },

  // System Tools
  { name: "Calculator", icon: "🧮", command: "open calculator" },
  { name: "Notepad", icon: "📄", command: "open notepad" },
  { name: "File Explorer", icon: "📁", command: "open file explorer" },
  { name: "Settings", icon: "⚙️", command: "open settings" },
  { name: "Task Manager", icon: "📊", command: "open task manager" },
  { name: "Control Panel", icon: "🎛️", command: "open control panel" },
  { name: "Device Manager", icon: "🖥️", command: "open device manager" },
  { name: "Registry Editor", icon: "📋", command: "open registry" },
  { name: "Performance Monitor", icon: "📈", command: "open system monitor" },

  // System Status
  { name: "Disk Usage", icon: "💾", command: "disk usage" },
  { name: "WiFi Status", icon: "📡", command: "wifi status" },
  { name: "IP Address", icon: "🌐", command: "ip address" },
  { name: "Network Status", icon: "📶", command: "network status" },

  // System Control
  { name: "Lock Screen", icon: "🔒", command: "lock screen" },
  { name: "Sleep Mode", icon: "😴", command: "sleep" },
  { name: "Shutdown", icon: "⏹️", command: "shutdown" },
  { name: "Restart", icon: "🔄", command: "restart" },

  // Audio & Visual
  { name: "Volume Up", icon: "🔊", command: "volume up" },
  { name: "Volume Down", icon: "🔉", command: "volume down" },
  { name: "Mute", icon: "🔇", command: "mute" },
  { name: "Brightness Up", icon: "☀️", command: "brightness up" },
  { name: "Brightness Down", icon: "🌙", command: "brightness down" },

  // Utilities
  { name: "Take Screenshot", icon: "📸", command: "take screenshot" },
  { name: "Check Updates", icon: "🔄", command: "check updates" },
  { name: "Disk Cleanup", icon: "🧹", command: "disk cleanup" },
  { name: "Defragment Disk", icon: "🔧", command: "defragment disk" },
  { name: "Weather Info", icon: "🌤️", command: "weather" },
]

// DOM Elements
const chatContainer = document.getElementById("chatContainer")
const userInput = document.getElementById("userInput")
const sendBtn = document.getElementById("sendBtn")
const voiceInputBtn = document.getElementById("voiceInputBtn")
const clearChatBtn = document.getElementById("clearChatBtn")
const noteInput = document.getElementById("noteInput")
const addNoteBtn = document.getElementById("addNoteBtn")
const voiceNoteBtn = document.getElementById("voiceNoteBtn")
const saveNotesBtn = document.getElementById("saveNotesBtn")
const clearNotesBtn = document.getElementById("clearNotesBtn")
const notesList = document.getElementById("notesList")
const speechRateSlider = document.getElementById("speechRate")
const rateValue = document.getElementById("rateValue")
const volumeSlider = document.getElementById("volume")
const volumeValue = document.getElementById("volumeValue")
const voiceSelect = document.getElementById("voiceSelect")
const wakeWordCheckbox = document.getElementById("wakeWord")
const voiceResponseCheckbox = document.getElementById("voiceResponse")
const quickActionsList = document.getElementById("quickActionsList")

// Speech Recognition Setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
const recognition = new SpeechRecognition()
recognition.continuous = false
recognition.interimResults = false
recognition.lang = "en-US"

let isListening = false
let notes = JSON.parse(localStorage.getItem("jarvisNotes")) || []

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  initializeQuickActions()
  loadNotes()
  setupEventListeners()
  addJarvisMessage("System initialized. Ready to assist!")
})

// Event Listeners
function setupEventListeners() {
  sendBtn.addEventListener("click", sendMessage)
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage()
  })
  voiceInputBtn.addEventListener("click", toggleVoiceInput)
  clearChatBtn.addEventListener("click", clearChat)
  addNoteBtn.addEventListener("click", addNote)
  voiceNoteBtn.addEventListener("click", addVoiceNote)
  saveNotesBtn.addEventListener("click", saveNotes)
  clearNotesBtn.addEventListener("click", clearAllNotes)

  speechRateSlider.addEventListener("input", (e) => {
    rateValue.textContent = e.target.value + "x"
  })

  volumeSlider.addEventListener("input", (e) => {
    volumeValue.textContent = e.target.value + "%"
  })

  recognition.onstart = () => {
    isListening = true
    voiceInputBtn.style.background = "rgba(255, 107, 53, 0.3)"
    voiceInputBtn.style.borderColor = "#ff6b35"
  }

  recognition.onend = () => {
    isListening = false
    voiceInputBtn.style.background = "rgba(0, 212, 255, 0.1)"
    voiceInputBtn.style.borderColor = "#00d4ff"
  }

  recognition.onresult = (event) => {
    let transcript = ""
    for (let i = event.resultIndex; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript
    }
    userInput.value = transcript
    sendMessage()
  }

  recognition.onerror = (event) => {
    addJarvisMessage(`Voice error: ${event.error}`)
  }
}

// Initialize Quick Actions
function initializeQuickActions() {
  quickActionsList.innerHTML = ""
  QUICK_ACTIONS.forEach((action) => {
    const btn = document.createElement("button")
    btn.className = "quick-action-btn"
    btn.innerHTML = `<span class="quick-action-icon">${action.icon}</span> ${action.name}`
    btn.addEventListener("click", () => {
      userInput.value = action.command
      sendMessage()
    })
    quickActionsList.appendChild(btn)
  })
}

// Send Message
async function sendMessage() {
  const message = userInput.value.trim()
  if (!message) return

  addUserMessage(message)
  userInput.value = ""

  try {
    const response = await fetch("/api/command", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command: message }),
    })

    const data = await response.json()
    addJarvisMessage(data.response)

    if (voiceResponseCheckbox.checked) {
      speakResponse(data.response)
    }
  } catch (error) {
    addJarvisMessage(`Error: ${error.message}`)
  }
}

// Add User Message
function addUserMessage(text) {
  const messageDiv = document.createElement("div")
  messageDiv.className = "message user-message"
  messageDiv.innerHTML = `
        <div class="message-content">
            <p>${escapeHtml(text)}</p>
        </div>
        <div class="message-avatar">👤</div>
    `
  chatContainer.appendChild(messageDiv)
  chatContainer.scrollTop = chatContainer.scrollHeight
}

// Add Jarvis Message
function addJarvisMessage(text) {
  const messageDiv = document.createElement("div")
  messageDiv.className = "message jarvis-message"
  messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <p>${escapeHtml(text)}</p>
        </div>
    `
  chatContainer.appendChild(messageDiv)
  chatContainer.scrollTop = chatContainer.scrollHeight
}

// Voice Input
function toggleVoiceInput() {
  if (isListening) {
    recognition.stop()
  } else {
    recognition.start()
  }
}

// Text to Speech
function speakResponse(text) {
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.rate = Number.parseFloat(speechRateSlider.value)
  utterance.volume = volumeSlider.value / 100
  utterance.voice =
    voiceSelect.value === "female"
      ? speechSynthesis.getVoices().find((v) => v.name.includes("Female"))
      : speechSynthesis.getVoices().find((v) => v.name.includes("Male"))

  speechSynthesis.speak(utterance)
}

// Notes Management
function addNote() {
  const noteText = noteInput.value.trim()
  if (!noteText) return

  notes.push({ id: Date.now(), text: noteText })
  noteInput.value = ""
  renderNotes()
}

function addVoiceNote() {
  if (isListening) return
  recognition.onend = () => {
    isListening = false
  }
  recognition.onresult = (event) => {
    let transcript = ""
    for (let i = event.resultIndex; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript
    }
    notes.push({ id: Date.now(), text: transcript })
    renderNotes()
    recognition.onresult = originalOnResult
  }
  recognition.start()
}

function renderNotes() {
  notesList.innerHTML = ""
  notes.forEach((note) => {
    const noteDiv = document.createElement("div")
    noteDiv.className = "note-item"
    noteDiv.innerHTML = `
            <span class="note-item-text">${escapeHtml(note.text)}</span>
            <button class="note-item-delete" onclick="deleteNote(${note.id})">✕</button>
        `
    notesList.appendChild(noteDiv)
  })
}

function deleteNote(id) {
  notes = notes.filter((n) => n.id !== id)
  renderNotes()
}

function saveNotes() {
  localStorage.setItem("jarvisNotes", JSON.stringify(notes))
  addJarvisMessage("Notes saved successfully!")
}

function clearAllNotes() {
  if (confirm("Clear all notes?")) {
    notes = []
    renderNotes()
    localStorage.removeItem("jarvisNotes")
    addJarvisMessage("All notes cleared!")
  }
}

function loadNotes() {
  renderNotes()
}

// Clear Chat
function clearChat() {
  if (confirm("Clear chat history?")) {
    chatContainer.innerHTML = ""
    addJarvisMessage("Chat cleared. How can I help you?")
  }
}

// Toggle Section
function toggleSection(element) {
  const section = element.parentElement
  section.classList.toggle("collapsed")
}

// Utility Functions
function escapeHtml(text) {
  const div = document.createElement("div")
  div.textContent = text
  return div.innerHTML
}

// Store original onResult for voice notes
const originalOnResult = recognition.onresult
