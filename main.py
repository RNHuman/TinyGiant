import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLineEdit, QPushButton, QToolBar, QAction
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QVBoxLayout for each tab
        layout = QVBoxLayout(self)

        # Create a web engine view
        self.browser = QWebEngineView()

        # Add the web engine view to the layout
        layout.addWidget(self.browser)

        # Open Google's home page by default
        self.browser.setUrl(QUrl("http://www.google.com"))

        # Track the page load event to update the tab title
        self.browser.urlChanged.connect(self.update_tab_title)

    def update_tab_title(self):
        # Get the current page title
        page_title = self.browser.page().title()
        if page_title:
            # Update the tab title with the page title
            index = self.parent().parent().indexOf(self)
            self.parent().parent().setTabText(index, page_title)
        else:
            # If the title isn't available, set it as "#"
            index = self.parent().parent().indexOf(self)
            self.parent().parent().setTabText(index, "#")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Basic Web Browser")

        # Create a QTabWidget for multiple tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create toolbar for the browser
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Add a new tab button to the toolbar
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(self.add_new_tab)
        self.toolbar.addAction(new_tab_action)

        # Create an address bar
        self.address_bar = QLineEdit()
        self.toolbar.addWidget(self.address_bar)

        # Add "Go" button next to the address bar
        go_button = QPushButton("Go")
        go_button.clicked.connect(self.navigate_to_url)
        self.toolbar.addWidget(go_button)

        # Add a default tab
        self.add_new_tab()

    def add_new_tab(self):
        # Create a new tab with a BrowserTab widget
        new_tab = BrowserTab()
        index = self.tabs.addTab(new_tab, "#")  # Default tab title is "#"
        self.tabs.setCurrentIndex(index)

        # When a new tab is selected, update the address bar
        self.tabs.currentChanged.connect(self.update_address_bar)

    def navigate_to_url(self):
        # Get the current tab
        current_tab = self.tabs.currentWidget()

        # Navigate to the URL in the address bar
        url = self.address_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        current_tab.browser.setUrl(QUrl(url))

    def update_address_bar(self):
        # Update the address bar with the URL of the current tab
        current_tab = self.tabs.currentWidget()
        if current_tab is not None:
            url = current_tab.browser.url().toString()
            self.address_bar.setText(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
