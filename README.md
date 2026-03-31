# Pratik Browser

A stunning, modern web browser with liquid glass design aesthetics, built with Python and PyQt5.

## ✨ Features

### 🎨 Modern Design
- **Liquid Glass UI**: Beautiful semi-transparent glass-like interface with rounded corners
- **Custom Title Bar**: Sleek window controls with minimize, maximize, and close buttons
- **Gradient Backgrounds**: Smooth color transitions and modern styling
- **Dark/Light Mode**: Toggle between themes for comfortable browsing

### 🌐 Browsing Features
- **Tabbed Browsing**: Open multiple websites in elegant tabs
- **Smart Navigation**: Back, forward, reload, and home buttons with icons
- **Intelligent Address Bar**: Enter URLs or search terms directly
- **Zoom Controls**: Zoom in/out and reset zoom per tab
- **Find in Page**: Search for text within web pages

### ⭐ Organization
- **Bookmarks Manager**: Save and organize favorite websites with visual indicators
- **History Tracking**: Comprehensive browsing history with easy access
- **Quick Access**: Open bookmarks and history entries with one click

### 🔧 Advanced Tools
- **File Opening**: Open local HTML files directly in the browser
- **Download Manager**: Track and manage file downloads
- **Developer Tools**: Built-in developer console access
- **Multiple Windows**: Open new browser windows
- **Keyboard Shortcuts**: Full keyboard navigation support

### ⚙️ Customization
- **Home Page Settings**: Set your preferred start page
- **Search Engine Options**: Choose from Google, Bing, DuckDuckGo, or Yahoo
- **Theme Preferences**: Light, dark, or automatic theme switching

## 🐛 Recent Fixes

- **Transparency Issue**: Reduced excessive transparency for better visibility
- **New Tab Crash**: Fixed initialization order to prevent crashes when creating new tabs
- **Stability Improvements**: Added error handling for better reliability

## 📸 Screenshots

### Main Interface
![Pratik Browser Main Interface](screenshots/Screenshot%202026-03-31%20at%208.22.50%E2%80%AFPM.png)

*Screenshots of the Pratik Browser interface and features are stored in the [`screenshots/`](screenshots/) folder. To add new screenshots:*

1. Take screenshots of the browser in action
2. Save them in the `screenshots/` folder with descriptive names (e.g., `main-interface.png`, `tabbed-browsing.png`)
3. Update this README with image references using the format: `![Alt Text](screenshots/filename.png)`

## �📋 Requirements

- Python 3.6+
- PyQt5
- PyQtWebEngine

## 🚀 Installation

1. Clone or download the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install PyQt5 PyQtWebEngine
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## 🎯 Usage

### Keyboard Shortcuts
- **Ctrl+T**: New Tab
- **Ctrl+N**: New Window
- **Ctrl+W**: Close Tab
- **Ctrl+O**: Open File
- **Ctrl+F**: Find in Page
- **Ctrl+D**: Add Bookmark
- **Ctrl+H**: Show History
- **Ctrl+J**: Show Downloads
- **F12**: Developer Tools
- **Ctrl++**: Zoom In
- **Ctrl+-**: Zoom Out
- **Ctrl+0**: Reset Zoom
- **Ctrl+Q**: Exit

### Menu Navigation
- **File**: Tab and window management
- **Edit**: Find in page functionality
- **View**: Zoom controls and theme switching
- **Bookmarks**: Bookmark management
- **History**: History viewing and clearing
- **Tools**: Downloads and developer tools
- **Settings**: Preferences and customization
- **Help**: About information

## 📁 Files

- `main.py`: Main application code with modern UI
- `bookmarks.txt`: Stores saved bookmarks
- `history.txt`: Stores browsing history
- `README.md`: This documentation
- `requirements.txt`: Python dependencies

## 🎨 Design Philosophy

Pratik Browser embraces modern design principles:
- **Transparency**: Glass-like effects with subtle transparency
- **Rounded Corners**: Soft, modern edge treatment
- **Intuitive Icons**: Clear, emoji-based visual indicators
- **Responsive Layout**: Adapts to different window sizes
- **Consistent Styling**: Unified design language throughout

## 🔧 Technical Details

- Built with PyQt5 for native desktop experience
- Uses QWebEngineView for modern web rendering
- Implements custom window chrome for seamless integration
- Persistent storage for bookmarks and history
- Event-driven architecture for responsive UI

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve Pratik Browser!

---

**Enjoy browsing with Pratik Browser - where modern design meets powerful functionality! 🌊✨**