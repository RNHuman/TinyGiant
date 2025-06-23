import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QToolBar, QAction, QFileDialog, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl


class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        self.browser.setUrl(QUrl("http://www.google.com"))
        self.browser.urlChanged.connect(self.update_tab_title)

    def update_tab_title(self):
        page_title = self.browser.page().title()
        index = self.parent().parent().indexOf(self)
        self.parent().parent().setTabText(index, page_title if page_title else "#")

    def clear_data(self):
        profile = self.browser.page().profile()
        profile.clearHttpCache()
        profile.clearAllVisitedLinks()
        profile.cookieStore().deleteAllCookies()
        self.browser.history().clear()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Private Web Browser")
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Back & Forward
        back_action = QAction("Back", self)
        back_action.triggered.connect(self.go_back)
        self.toolbar.addAction(back_action)

        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.go_forward)
        self.toolbar.addAction(forward_action)

        # New Tab
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(self.add_new_tab)
        self.toolbar.addAction(new_tab_action)

        # Address bar + Go
        self.address_bar = QLineEdit()
        self.toolbar.addWidget(self.address_bar)

        go_button = QPushButton("Go")
        go_button.clicked.connect(self.navigate_to_url)
        self.toolbar.addWidget(go_button)

        # Download manager
        QWebEngineProfile.defaultProfile().downloadRequested.connect(self.handle_download)

        # Add default tab
        self.add_new_tab()

        # Show Incognito Warning
        self.show_incognito_warning()

    def show_incognito_warning(self):
        QMessageBox.information(
            self,
            "Incognito Mode",
            "You are browsing in incognito mode.\n"
            "No history, cookies, or cache will be saved.\n"
            "All data will be deleted when you close the browser.",
            QMessageBox.Ok
        )

    def add_new_tab(self):
        new_tab = BrowserTab()
        index = self.tabs.addTab(new_tab, "#")
        self.tabs.setCurrentIndex(index)
        self.tabs.currentChanged.connect(self.update_address_bar)

    def navigate_to_url(self):
        current_tab = self.tabs.currentWidget()
        url = self.address_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        current_tab.browser.setUrl(QUrl(url))

    def update_address_bar(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            self.address_bar.setText(current_tab.browser.url().toString())

    def go_back(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.back()

    def go_forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.forward()

    def handle_download(self, download):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", download.path())
        if save_path:
            download.setPath(save_path)
            download.accept()

    def closeEvent(self, event):
        # Full privacy cleanup
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            tab.clear_data()
        profile = QWebEngineProfile.defaultProfile()
        profile.cookieStore().deleteAllCookies()
        profile.clearHttpCache()
        profile.clearAllVisitedLinks()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
