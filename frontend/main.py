from PyQt5.QtWidgets import QApplication, QStackedWidget
from login_ui import LoginWindow
from vote_ui import VoteWindow
import sys

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize screens
        self.login_screen = LoginWindow(self)
        self.vote_screen = VoteWindow(self)

        # Add screens to stacked widget
        self.addWidget(self.login_screen)
        self.addWidget(self.vote_screen)

        # Show login screen first
        self.setCurrentWidget(self.login_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.setWindowTitle("Blockchain Voting System")
    main_app.resize(600, 400)
    main_app.show()
    sys.exit(app.exec_())
