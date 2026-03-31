import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest


class CustomTabBar(QTabBar):
    """Custom tab bar with favicon, title, and close button"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setExpanding(False)  # Disable expanding to enable scrolling
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setUsesScrollButtons(True)  # Enable scroll buttons
        self.setElideMode(Qt.ElideRight)  # Elide text when too long
        
        self.setStyleSheet("""
            QTabBar {
                background: rgba(255, 255, 255, 0.95);
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 0px;
                margin: 2px;
                min-width: 150px;
                max-width: 200px;
                height: 32px;
                color: #333;
                font-weight: bold;
                text-align: left;
                alignment: left;
            }
            QTabBar::tab:selected {
                background: rgba(0, 123, 255, 0.2);
                border: 2px solid #007bff;
            }
            QTabBar::tab:hover {
                background: rgba(0, 123, 255, 0.1);
            }
            QTabBar::close-button {
                image: url(close.png);
                subcontrol-position: right;
                margin: 4px;
            }
            QTabBar QToolButton {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 4px;
                width: 16px;
                height: 16px;
            }
            QTabBar QToolButton:hover {
                background: rgba(0, 123, 255, 0.1);
            }
        """)
        
        # Store tab data
        self.tab_data = {}  # tab_index -> {'title': str, 'favicon': QIcon, 'url': str}
    
    def paintEvent(self, event):
        """Custom paint event to draw favicon, title, and close button"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for i in range(self.count()):
            rect = self.tabRect(i)
            is_selected = (i == self.currentIndex())
            
            # Draw tab background
            if is_selected:
                painter.fillRect(rect, QColor(0, 123, 255, 51))  # Selected color
                painter.setPen(QPen(QColor(0, 123, 255), 2))
            else:
                painter.fillRect(rect, QColor(255, 255, 255, 242))  # Normal color
                painter.setPen(QPen(QColor(0, 0, 0, 25), 1))
            
            painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 8, 8)
            
            # Get tab data
            tab_data = self.tabData(i)
            title = tab_data.get('title', f'Tab {i+1}')
            favicon = tab_data.get('favicon')
            
            # Draw favicon (16x16) - improved handling
            favicon_rect = QRect(rect.left() + 8, rect.top() + 8, 16, 16)
            if favicon and not favicon.isNull():
                try:
                    # Try to get pixmap from icon
                    pixmap = favicon.pixmap(16, 16)
                    if not pixmap.isNull():
                        painter.drawPixmap(favicon_rect, pixmap)
                    else:
                        # Try to get pixmap at any available size
                        sizes = favicon.availableSizes()
                        if sizes:
                            pixmap = favicon.pixmap(sizes[0])
                            if not pixmap.isNull():
                                scaled_pixmap = pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                                painter.drawPixmap(favicon_rect, scaled_pixmap)
                            else:
                                self.draw_default_favicon(painter, favicon_rect)
                        else:
                            self.draw_default_favicon(painter, favicon_rect)
                except Exception as e:
                    self.draw_default_favicon(painter, favicon_rect)
            else:
                # Draw default favicon
                self.draw_default_favicon(painter, favicon_rect)
            
            # Draw title (left-aligned, with proper spacing for favicon and close button)
            title_rect = QRect(rect.left() + 32, rect.top(), rect.width() - 60, rect.height())
            painter.setPen(QPen(QColor(51, 51, 51)))  # Text color
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            
            # Elide text if too long
            metrics = painter.fontMetrics()
            elided_text = metrics.elidedText(title, Qt.ElideRight, title_rect.width())
            painter.drawText(title_rect, Qt.AlignLeft | Qt.AlignVCenter, elided_text)
            
            # Draw close button (X)
            if self.tabsClosable():
                close_rect = QRect(rect.right() - 20, rect.top() + 6, 14, 14)
                painter.setPen(QPen(QColor(102, 102, 102), 2))
                painter.drawLine(close_rect.left() + 3, close_rect.top() + 3, 
                               close_rect.right() - 3, close_rect.bottom() - 3)
                painter.drawLine(close_rect.right() - 3, close_rect.top() + 3, 
                               close_rect.left() + 3, close_rect.bottom() - 3)
    
    def draw_default_favicon(self, painter, rect):
        """Draw a default globe favicon when no icon is available"""
        painter.setPen(QPen(QColor(0, 123, 255), 2))
        painter.setBrush(QBrush(QColor(0, 123, 255, 100)))
        painter.drawEllipse(rect)
        
        # Draw simple globe lines
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.drawLine(rect.center().x(), rect.top() + 2, rect.center().x(), rect.bottom() - 2)
        painter.drawLine(rect.left() + 2, rect.center().y(), rect.right() - 2, rect.center().y())
    
    def setTabData(self, index, title, favicon=None, url=""):
        """Set custom data for a tab"""
        if favicon is None:
            favicon = QIcon()  # Empty icon
        
        self.tab_data[index] = {
            'title': title,
            'favicon': favicon,
            'url': url
        }
        
        # Update the tab text in the parent QTabWidget
        if hasattr(self.parent(), 'setTabText'):
            self.parent().setTabText(index, title)
        
        self.update()  # Force repaint
    
    def tabData(self, index):
        """Get custom data for a tab"""
        return self.tab_data.get(index, {'title': '', 'favicon': QIcon(), 'url': ''})
    
    def mousePressEvent(self, event):
        """Handle mouse press events, especially for close button"""
        if event.button() == Qt.LeftButton:
            tab_index = self.tabAt(event.pos())
            if tab_index >= 0:
                rect = self.tabRect(tab_index)
                # Check if click is on close button (right side of tab)
                close_rect = QRect(rect.right() - 20, rect.top() + 6, 14, 14)
                if close_rect.contains(event.pos()) and self.tabsClosable():
                    # Emit close signal
                    self.tabCloseRequested.emit(tab_index)
                    return
        
        # Call parent mouse press event for normal tab selection
        super().mousePressEvent(event)


class ModernBrowserTab(QWidget):
    def __init__(self, tab_widget, main_window, url="https://www.google.com"):
        super().__init__()
        self.tab_widget = tab_widget
        self.main_window = main_window
        self.browser = QWebEngineView()
        if isinstance(url, str):
            self.browser.setUrl(QUrl(url))
        else:
            self.browser.setUrl(QUrl("https://www.google.com"))

        # Modern glass-like styling
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.98);
                border-radius: 12px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: #333;
                min-width: 40px;
            }
            QPushButton:hover {
                background: rgba(0, 123, 255, 0.1);
                border: 1px solid rgba(0, 123, 255, 0.3);
            }
            QPushButton:pressed {
                background: rgba(0, 123, 255, 0.2);
            }
            QLineEdit {
                background: rgba(255, 255, 255, 0.97);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #007bff;
                background: rgba(255, 255, 255, 1);
            }
        """)

        # Navigation bar with modern design
        self.navbar = QHBoxLayout()
        self.navbar.setContentsMargins(15, 15, 15, 10)
        self.navbar.setSpacing(8)

        # Navigation buttons with icons
        self.back_btn = QPushButton("⬅")
        self.back_btn.setToolTip("Go Back")
        self.back_btn.clicked.connect(self.browser.back)
        self.navbar.addWidget(self.back_btn)

        self.forward_btn = QPushButton("➡")
        self.forward_btn.setToolTip("Go Forward")
        self.forward_btn.clicked.connect(self.browser.forward)
        self.navbar.addWidget(self.forward_btn)

        self.reload_btn = QPushButton("🔄")
        self.reload_btn.setToolTip("Reload Page")
        self.reload_btn.clicked.connect(self.browser.reload)
        self.navbar.addWidget(self.reload_btn)

        self.home_btn = QPushButton("🏠")
        self.home_btn.setToolTip("Go Home")
        self.home_btn.clicked.connect(self.navigate_home)
        self.navbar.addWidget(self.home_btn)

        self.new_tab_btn = QPushButton("➕")
        self.new_tab_btn.setToolTip("New Tab")
        self.new_tab_btn.clicked.connect(self.main_window.add_new_tab)
        self.navbar.addWidget(self.new_tab_btn)

        # Spacer
        self.navbar.addStretch()

        # URL bar with modern styling
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter URL...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar, 1)

        # Go button
        self.go_btn = QPushButton("🔍")
        self.go_btn.setToolTip("Go")
        self.go_btn.clicked.connect(self.navigate_to_url)
        self.navbar.addWidget(self.go_btn)

        # Additional buttons
        self.bookmark_btn = QPushButton("⭐")
        self.bookmark_btn.setToolTip("Add Bookmark")
        self.bookmark_btn.clicked.connect(self.add_bookmark)
        self.navbar.addWidget(self.bookmark_btn)

        self.zoom_in_btn = QPushButton("🔍+")
        self.zoom_in_btn.setToolTip("Zoom In")
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.navbar.addWidget(self.zoom_in_btn)

        self.zoom_out_btn = QPushButton("🔍-")
        self.zoom_out_btn.setToolTip("Zoom Out")
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.navbar.addWidget(self.zoom_out_btn)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addLayout(self.navbar)
        layout.addWidget(self.browser)

        self.setLayout(layout)

        # Connect signals
        self.browser.urlChanged.connect(self.update_url)
        self.browser.loadFinished.connect(self.update_title_and_icon)
        self.browser.loadProgress.connect(self.update_progress)

        # Zoom factor
        self.zoom_factor = 1.0
        
        # Favicon storage
        self.current_favicon = None

    def navigate_home(self):
        home_url = "https://www.google.com"  # Could be made configurable
        self.browser.setUrl(QUrl(home_url))

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return

        # Handle search queries vs URLs
        if not url.startswith("http") and "." not in url:
            # It's a search query
            url = f"https://www.google.com/search?q={QUrl.toPercentEncoding(url).data().decode()}"
        elif not url.startswith("http"):
            url = "https://" + url

        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def update_title_and_icon(self):
        title = self.browser.page().title()
        if title:
            # Truncate title if too long
            display_title = title[:20] + "..." if len(title) > 20 else title
            index = self.tab_widget.indexOf(self)
            
            # Update tab data with title
            tab_data = self.main_window.custom_tab_bar.tabData(index)
            tab_data['title'] = display_title
            self.main_window.custom_tab_bar.setTabData(index, display_title, tab_data['favicon'], tab_data['url'])
            
            # Try to get favicon
            self.fetch_favicon()

    def fetch_favicon(self):
        """Fetch and set the favicon for the current tab"""
        try:
            url = self.browser.url()
            if not url.isValid():
                return
                
            # Get the full URL for favicon lookup
            full_url = url.toString()
            if not full_url:
                return
                
            # Use the provided favicon service URL format
            favicon_url = f"https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={full_url}&size=32"
            
            # Create a network request for the favicon
            from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
            
            if not hasattr(self, 'network_manager'):
                self.network_manager = QNetworkAccessManager()
                self.network_manager.finished.connect(self.on_favicon_downloaded)
            
            request = QNetworkRequest(QUrl(favicon_url))
            self.network_manager.get(request)
            
        except Exception as e:
            # If favicon fetching fails, use default icon
            self.set_default_favicon()
    
    def on_favicon_downloaded(self, reply):
        """Handle favicon download completion"""
        try:
            if reply.error() == 0:  # No error
                data = reply.readAll()
                pixmap = QPixmap()
                if pixmap.loadFromData(data):
                    # Scale favicon to 16x16 for tab
                    scaled_pixmap = pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    icon = QIcon(scaled_pixmap)
                    index = self.tab_widget.indexOf(self)
                    
                    if index >= 0:  # Make sure tab still exists
                        # Update tab data with favicon
                        tab_data = self.main_window.custom_tab_bar.tabData(index)
                        tab_data['favicon'] = icon
                        self.main_window.custom_tab_bar.setTabData(index, tab_data['title'], icon, tab_data['url'])
                        
                        self.current_favicon = icon
                        return
            
            # If loading failed, set default icon
            self.set_default_favicon()
            
        except Exception as e:
            self.set_default_favicon()
        finally:
            reply.deleteLater()
    
    def set_default_favicon(self):
        """Set a default globe icon when favicon is not available"""
        default_icon = QIcon()  # Empty icon for now, could add a default globe
        index = self.tab_widget.indexOf(self)
        
        # Update tab data with default favicon
        tab_data = self.main_window.custom_tab_bar.tabData(index)
        tab_data['favicon'] = default_icon
        self.main_window.custom_tab_bar.setTabData(index, tab_data['title'], default_icon, tab_data['url'])
        
        self.current_favicon = default_icon

    def update_progress(self, progress):
        # Could add a progress bar here
        pass

    def add_bookmark(self):
        # This will be handled by the main window
        pass

    def zoom_in(self):
        self.zoom_factor *= 1.1
        self.browser.setZoomFactor(self.zoom_factor)

    def zoom_out(self):
        self.zoom_factor /= 1.1
        self.browser.setZoomFactor(self.zoom_factor)

class ModernBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pratik Browser")
        self.setGeometry(100, 100, 1400, 900)

        # Initialize data first
        self.bookmarks = []
        self.history = []
        self.downloads = []
        self.home_url = "https://www.google.com"
        self.dark_mode = False
        self.setStyleSheet("""
            QMainWindow {
                background: rgba(255, 255, 255, 0.98);
                border-radius: 15px;
            }
            QTabWidget::pane {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.97);
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 8px 16px;
                margin-right: 2px;
                color: #333;
                font-weight: bold;
                text-align: left;
            }
            QTabBar::tab:selected {
                background: rgba(0, 123, 255, 0.2);
                border: 2px solid #007bff;
            }
            QTabBar::tab:hover {
                background: rgba(0, 123, 255, 0.1);
            }
            QMenuBar {
                background: rgba(255, 255, 255, 0.95);
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                padding: 5px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 5px 10px;
                border-radius: 5px;
                color: #333;
            }
            QMenuBar::item:selected {
                background: rgba(0, 123, 255, 0.1);
            }
            QMenu {
                background: rgba(255, 255, 255, 0.97);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
                color: #333;
            }
            QMenu::item:selected {
                background: rgba(0, 123, 255, 0.1);
            }
            QStatusBar {
                background: rgba(255, 255, 255, 0.95);
                border-top: 1px solid rgba(0, 0, 0, 0.1);
                color: #666;
            }
        """)

        # Remove the translucent background for better visibility
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        # Create central widget with glass effect
        central_widget = QWidget()
        central_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.98);
                border-radius: 15px;
            }
        """)
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Custom title bar
        self.create_title_bar()
        main_layout.addWidget(self.title_bar)

        # Tab widget with custom tab bar
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        
        # Use custom tab bar
        self.custom_tab_bar = CustomTabBar()
        self.tabs.setTabBar(self.custom_tab_bar)
        
        # Connect tab close signal
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        # Initial stylesheet will be set by update_tab_widths
        main_layout.addWidget(self.tabs)
        
        # Connect tab change signals to update widths
        self.tabs.tabBar().tabMoved.connect(self.update_tab_widths)
        self.tabs.currentChanged.connect(self.update_tab_widths)
        
        # Connect resize event to update tab widths
        self.resizeEvent = self.on_resize

        # Create menus
        self.create_menus()

        # Status bar
        self.status = QStatusBar()
        self.status.setStyleSheet("""
            QStatusBar {
                background: rgba(255, 255, 255, 0.9);
                border-top: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 0 0 15px 15px;
                color: #666;
                padding: 5px;
            }
        """)
        main_layout.addWidget(self.status)

        # Load data
        self.load_bookmarks()
        self.load_history()

        self.show()

    def create_title_bar(self):
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 15px 15px 0 0;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)

        layout = QHBoxLayout(self.title_bar)
        layout.setContentsMargins(15, 5, 15, 5)

        # Window title
        title = QLabel("Pratik Browser")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        layout.addWidget(title)

        layout.addStretch()

        # Window controls
        minimize_btn = QPushButton("─")
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.8);
                border: none;
                border-radius: 15px;
                color: #666;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(255, 215, 0, 0.2);
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        layout.addWidget(minimize_btn)

        maximize_btn = QPushButton("⬜")
        maximize_btn.setFixedSize(30, 30)
        maximize_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.8);
                border: none;
                border-radius: 15px;
                color: #666;
                font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(0, 255, 0, 0.2);
            }
        """)
        maximize_btn.clicked.connect(self.toggle_maximize)
        layout.addWidget(maximize_btn)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.8);
                border: none;
                border-radius: 15px;
                color: #666;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(255, 0, 0, 0.2);
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        # Enable dragging
        self.title_bar.mousePressEvent = self.title_bar_mouse_press
        self.title_bar.mouseMoveEvent = self.title_bar_mouse_move

    def title_bar_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def title_bar_mouse_move(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_pos'):
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def create_menus(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background: rgba(255, 255, 255, 0.9);
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                padding: 5px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 5px 10px;
                border-radius: 5px;
                color: #333;
            }
            QMenuBar::item:selected {
                background: rgba(0, 123, 255, 0.1);
            }
        """)

        # File menu
        file_menu = menubar.addMenu("📁 File")
        new_tab_action = QAction("New Tab", self)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab_action)

        new_window_action = QAction("New Window", self)
        new_window_action.setShortcut("Ctrl+N")
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)

        open_file_action = QAction("Open File...", self)
        open_file_action.setShortcut("Ctrl+O")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        file_menu.addSeparator()

        close_tab_action = QAction("Close Tab", self)
        close_tab_action.setShortcut("Ctrl+W")
        close_tab_action.triggered.connect(lambda: self.close_tab(self.tabs.currentIndex()))
        file_menu.addAction(close_tab_action)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("✏️ Edit")
        find_action = QAction("Find in Page", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.find_in_page)
        edit_menu.addAction(find_action)

        # View menu
        view_menu = menubar.addMenu("👁️ View")
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self.zoom_in_current)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.zoom_out_current)
        view_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.triggered.connect(self.reset_zoom_current)
        view_menu.addAction(reset_zoom_action)

        view_menu.addSeparator()

        toggle_dark_mode_action = QAction("Toggle Dark Mode", self)
        toggle_dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(toggle_dark_mode_action)

        # Bookmarks menu
        bookmarks_menu = menubar.addMenu("⭐ Bookmarks")
        add_bookmark_action = QAction("Add Bookmark", self)
        add_bookmark_action.setShortcut("Ctrl+D")
        add_bookmark_action.triggered.connect(self.add_bookmark)
        bookmarks_menu.addAction(add_bookmark_action)

        manage_bookmarks_action = QAction("Manage Bookmarks", self)
        manage_bookmarks_action.triggered.connect(self.manage_bookmarks)
        bookmarks_menu.addAction(manage_bookmarks_action)

        # History menu
        history_menu = menubar.addMenu("🕐 History")
        show_history_action = QAction("Show History", self)
        show_history_action.setShortcut("Ctrl+H")
        show_history_action.triggered.connect(self.show_history)
        history_menu.addAction(show_history_action)

        clear_history_action = QAction("Clear History", self)
        clear_history_action.triggered.connect(self.clear_history)
        history_menu.addAction(clear_history_action)

        # Tools menu
        tools_menu = menubar.addMenu("🔧 Tools")
        downloads_action = QAction("Downloads", self)
        downloads_action.setShortcut("Ctrl+J")
        downloads_action.triggered.connect(self.show_downloads)
        tools_menu.addAction(downloads_action)

        developer_tools_action = QAction("Developer Tools", self)
        developer_tools_action.setShortcut("F12")
        developer_tools_action.triggered.connect(self.show_dev_tools)
        tools_menu.addAction(developer_tools_action)

        # Settings menu
        settings_menu = menubar.addMenu("⚙️ Settings")
        preferences_action = QAction("Preferences", self)
        preferences_action.triggered.connect(self.show_preferences)
        settings_menu.addAction(preferences_action)

        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        about_action = QAction("About Pratik Browser", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Toolbar
        # toolbar = self.addToolBar("Navigation")
        # toolbar.addAction(new_tab_action)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Load data
        self.load_bookmarks()
        self.load_history()

        # Add initial tab (only once)
        self.add_new_tab()

        self.show()

    def add_new_tab(self, url=None):
        try:
            if url is None:
                url = self.home_url
            if not isinstance(url, str):
                url = str(url)
            tab = ModernBrowserTab(self.tabs, self, url)
            index = self.tabs.addTab(tab, "🌐 New Tab")
            self.tabs.setCurrentIndex(index)
            
            # Set initial tab data with default favicon
            default_icon = QIcon()  # Will show default globe
            self.custom_tab_bar.setTabData(index, "New Tab", default_icon, url)
            
            tab.browser.urlChanged.connect(lambda q, tab=tab: self.add_to_history(q.toString()))
            tab.bookmark_btn.clicked.connect(self.add_bookmark)
            
            # Update tab widths after adding new tab
            self.update_tab_widths()
        except Exception as e:
            print(f"Error creating new tab: {e}")
            QMessageBox.warning(self, "Error", f"Failed to create new tab: {e}")

    def close_tab(self, index):
        if self.tabs.count() > 1:
            # Clean up tab data
            if index in self.custom_tab_bar.tab_data:
                del self.custom_tab_bar.tab_data[index]
            
            # Shift remaining tab data indices
            new_data = {}
            for old_index, data in self.custom_tab_bar.tab_data.items():
                if old_index > index:
                    new_data[old_index - 1] = data
                elif old_index < index:
                    new_data[old_index] = data
            self.custom_tab_bar.tab_data = new_data
            
            self.tabs.removeTab(index)
            self.update_tab_widths()
        else:
            self.close()

    def update_tab_widths(self):
        """Update tab display when tabs change (no longer manages widths since we use scrolling)"""
        # With scrollable tabs, we don't need to manage widths
        # Just ensure the tab bar updates properly
        self.custom_tab_bar.update()
        
        # Update status bar with tab count
        tab_count = self.tabs.count()
        if tab_count > 0:
            self.status.showMessage(f"{tab_count} tab{'s' if tab_count != 1 else ''} open")
        else:
            self.status.showMessage("No tabs open")

    def on_resize(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        # With scrollable tabs, no need to update widths on resize
        self.custom_tab_bar.update()

    def new_window(self):
        new_window = ModernBrowser()
        new_window.show()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "HTML Files (*.html *.htm);;All Files (*)")
        if file_path:
            self.add_new_tab(QUrl.fromLocalFile(file_path).toString())

    def find_in_page(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            search_text, ok = QInputDialog.getText(self, "Find in Page", "Enter text to find:")
            if ok and search_text:
                current_tab.browser.findText(search_text)

    def zoom_in_current(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.zoom_in()

    def zoom_out_current(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.zoom_out()

    def reset_zoom_current(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.zoom_factor = 1.0
            current_tab.browser.setZoomFactor(1.0)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(30, 30, 30, 0.95),
                        stop:1 rgba(45, 45, 45, 0.98));
                    border-radius: 15px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(240, 248, 255, 0.95),
                        stop:1 rgba(255, 255, 255, 0.98));
                    border-radius: 15px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                }
            """)

    def add_bookmark(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            url = current_tab.browser.url().toString()
            title = current_tab.browser.page().title()
            if title and url:
                self.bookmarks.append({"title": title, "url": url})
                self.save_bookmarks()
                self.status.showMessage(f"Bookmarked: {title}", 3000)

    def manage_bookmarks(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("⭐ Manage Bookmarks")
        dialog.setStyleSheet("""
            QDialog {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            QListWidget {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton {
                background: rgba(0, 123, 255, 0.8);
                border: 1px solid rgba(0, 123, 255, 0.3);
                border-radius: 8px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 123, 255, 1);
            }
        """)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        list_widget = QListWidget()
        for bookmark in self.bookmarks:
            item = QListWidgetItem(f"⭐ {bookmark['title']}")
            item.setToolTip(bookmark['url'])
            list_widget.addItem(item)
        layout.addWidget(list_widget)

        buttons = QHBoxLayout()
        open_btn = QPushButton("🌐 Open")
        open_btn.clicked.connect(lambda: self.open_bookmark(list_widget.currentRow()))
        buttons.addWidget(open_btn)

        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.clicked.connect(lambda: self.delete_bookmark(list_widget.currentRow(), list_widget))
        buttons.addWidget(delete_btn)

        layout.addLayout(buttons)
        dialog.setLayout(layout)
        dialog.exec_()

    def open_bookmark(self, index):
        if 0 <= index < len(self.bookmarks):
            url = self.bookmarks[index]["url"]
            self.add_new_tab(url)

    def delete_bookmark(self, index, list_widget):
        if 0 <= index < len(self.bookmarks):
            del self.bookmarks[index]
            self.save_bookmarks()
            list_widget.takeItem(index)

    def show_history(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("🕐 Browsing History")
        dialog.setStyleSheet("""
            QDialog {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            QListWidget {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton {
                background: rgba(0, 123, 255, 0.8);
                border: 1px solid rgba(0, 123, 255, 0.3);
                border-radius: 8px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 123, 255, 1);
            }
        """)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        list_widget = QListWidget()
        for entry in self.history[-100:]:  # Last 100 entries
            item = QListWidgetItem(f"🕐 {entry}")
            list_widget.addItem(item)
        layout.addWidget(list_widget)

        buttons = QHBoxLayout()
        open_btn = QPushButton("🌐 Open")
        open_btn.clicked.connect(lambda: self.open_history(list_widget.currentItem().text()[2:] if list_widget.currentItem() else ""))
        buttons.addWidget(open_btn)

        clear_btn = QPushButton("🗑️ Clear History")
        clear_btn.clicked.connect(self.clear_history)
        buttons.addWidget(clear_btn)

        layout.addLayout(buttons)
        dialog.setLayout(layout)
        dialog.exec_()

    def clear_history(self):
        reply = QMessageBox.question(self, "Clear History",
                                   "Are you sure you want to clear all browsing history?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.history.clear()
            self.save_history()
            QMessageBox.information(self, "History Cleared", "Browsing history has been cleared.")

    def open_history(self, url):
        if url:
            self.add_new_tab(url)

    def show_downloads(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("📥 Downloads")
        dialog.setStyleSheet("""
            QDialog {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            QListWidget {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 5px;
            }
        """)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        if not self.downloads:
            no_downloads_label = QLabel("📥 No downloads yet")
            no_downloads_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_downloads_label)
        else:
            list_widget = QListWidget()
            for download in self.downloads:
                item = QListWidgetItem(f"📄 {download['filename']} - {download['status']}")
                list_widget.addItem(item)
            layout.addWidget(list_widget)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_dev_tools(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.page().setDevToolsPage(QWebEnginePage())
            # This would open developer tools - requires more complex implementation

    def show_preferences(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("⚙️ Preferences")
        dialog.setStyleSheet("""
            QDialog {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            QLabel {
                color: #333;
                font-weight: bold;
            }
            QLineEdit {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 8px;
                color: #333;
            }
            QPushButton {
                background: rgba(0, 123, 255, 0.8);
                border: 1px solid rgba(0, 123, 255, 0.3);
                border-radius: 8px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 123, 255, 1);
            }
        """)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        # Home page setting
        home_label = QLabel("🏠 Home Page:")
        self.home_edit = QLineEdit(self.home_url)
        layout.addWidget(home_label)
        layout.addWidget(self.home_edit)

        # Search engine setting
        search_label = QLabel("🔍 Default Search Engine:")
        self.search_combo = QComboBox()
        self.search_combo.addItems(["Google", "Bing", "DuckDuckGo", "Yahoo"])
        layout.addWidget(search_label)
        layout.addWidget(self.search_combo)

        # Theme setting
        theme_label = QLabel("🎨 Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Auto"])
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_combo)

        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_preferences)
        layout.addWidget(save_btn)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_preferences(self):
        self.home_url = self.home_edit.text()
        # Save other preferences here
        QMessageBox.information(self, "Settings Saved", "Your preferences have been saved!")

    def show_about(self):
        about_text = """
        <h2>Pratik Browser</h2>
        <p><b>Version:</b> 2.0</p>
        <p><b>Modern Web Experience</b></p>
        <p>A beautiful, feature-rich web browser with a liquid glass design.</p>
        <p>Features:</p>
        <ul>
            <li>🪟 Modern glass-like UI</li>
            <li>📑 Tabbed browsing</li>
            <li>⭐ Bookmarks management</li>
            <li>🕐 History tracking</li>
            <li>🔍 Built-in search</li>
            <li>🌓 Dark/Light mode</li>
            <li>📥 Download management</li>
            <li>🔧 Developer tools</li>
        </ul>
        <p>Built with PyQt5 & Python</p>
        """
        QMessageBox.about(self, "About Pratik Browser", about_text)

    def add_to_history(self, url):
        if url and url not in self.history:
            self.history.append(url)
            self.save_history()

    def load_bookmarks(self):
        try:
            with open("bookmarks.txt", "r") as f:
                for line in f:
                    if " | " in line:
                        title, url = line.strip().split(" | ", 1)
                        self.bookmarks.append({"title": title, "url": url})
        except FileNotFoundError:
            pass

    def save_bookmarks(self):
        with open("bookmarks.txt", "w") as f:
            for bookmark in self.bookmarks:
                f.write(f"{bookmark['title']} | {bookmark['url']}\n")

    def load_history(self):
        try:
            with open("history.txt", "r") as f:
                self.history = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            pass

    def save_history(self):
        with open("history.txt", "w") as f:
            for url in self.history:
                f.write(url + "\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Pratik Browser")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Pratik Browser")
    app.setWindowIcon(QIcon())  # Could add an icon here

    # Set application-wide stylesheet for consistency
    app.setStyleSheet("""
        QMessageBox {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }
        QInputDialog {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }
    """)

    window = ModernBrowser()
    sys.exit(app.exec_())