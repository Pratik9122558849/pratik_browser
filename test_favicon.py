#!/usr/bin/env python3
"""
Test script to verify favicon loading functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QPixmap, QIcon

def test_favicon_loading():
    """Test favicon loading from Google's service"""
    print("🧪 Testing favicon loading...")

    app = QApplication(sys.argv)

    def download_favicon():
        manager = QNetworkAccessManager()

        def on_finished(reply):
            print(f"📡 Network reply error: {reply.error()}")
            if reply.error() == 0:
                data = reply.readAll()
                print(f"📦 Downloaded {len(data)} bytes")

                pixmap = QPixmap()
                if pixmap.loadFromData(data):
                    print(f"✅ Pixmap created: {pixmap.width()}x{pixmap.height()}")
                    scaled = pixmap.scaled(16, 16, aspectRatioMode=1, transformationMode=1)
                    icon = QIcon(scaled)
                    print(f"✅ Icon created with {len(icon.availableSizes())} available sizes")
                    print("🎉 Favicon loading works!")
                else:
                    print("❌ Failed to create pixmap from downloaded data")
            else:
                print(f"❌ Network error: {reply.errorString()}")

            app.quit()

        manager.finished.connect(on_finished)

        # Test with Google's favicon service
        url = "https://www.google.com/s2/favicons?domain=google.com&sz=32"
        print(f"🌐 Requesting: {url}")
        request = QNetworkRequest(QUrl(url))
        manager.get(request)

    QTimer.singleShot(100, download_favicon)
    app.exec_()

if __name__ == "__main__":
    test_favicon_loading()