import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLineEdit, QPushButton, QToolBar, QAction, QFileDialog
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem, QWebEngineProfile
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

    def clear_history(self):
        # Clear the browser history for this tab
        self.browser.history().clear()

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

        # Add Back and Forward buttons
        back_action = QAction("Back", self)
        back_action.triggered.connect(self.go_back)
        self.toolbar.addAction(back_action)

        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.go_forward)
        self.toolbar.addAction(forward_action)

        # Add a new tab button to the toolbar
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(self.add_new_tab)
        self.toolbar.addAction(new_tab_action)

        # Add Print and Save as PDF button
        print_action = QAction("Print / Save as PDF", self)
        print_action.triggered.connect(self.print_page)
        self.toolbar.addAction(print_action)

        # Create an address bar
        self.address_bar = QLineEdit()
        self.toolbar.addWidget(self.address_bar)

        # Add "Go" button next to the address bar
        go_button = QPushButton("Go")
        go_button.clicked.connect(self.navigate_to_url)
        self.toolbar.addWidget(go_button)

        # Add a default tab
        self.add_new_tab()

        # Set up the download manager
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_download)

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

    def go_back(self):
        # Navigate back in the current tab
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.back()

    def go_forward(self):
        # Navigate forward in the current tab
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.forward()

    def print_page(self):
        # Print the current page or save as PDF
        current_tab = self.tabs.currentWidget()
        if current_tab:
            printer = QWebEngineView()
            file_dialog = QFileDialog.getSaveFileName(self, "Save as PDF", "", "*.pdf")
            if file_dialog[0]:
                current_tab.browser.page().printToPdf(file_dialog[0])

    def handle_download(self, download):
        # Handle file downloads
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", download.path())
        if save_path:
            download.setPath(save_path)
            download.accept()

    def closeEvent(self, event):
        # Clear history for all tabs when closing the application
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            tab.clear_history()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())