# main.py
from PySide6.QtWidgets import QApplication
import db

from app.ui.login import LoginWindow
from app.ui.register_super_admin import RegisterSuperAdminWindow

from app.ui.super_admin_window import SuperAdminWindow
from app.ui.admin.admin_window import AdminWindow
from app.ui.teller_window import TellerWindow
from app.ui.monitor.monitor_window import MonitorWindow


def open_role_window(user):
    role = user["role"]

    if role == "super_admin":
        win = SuperAdminWindow(user)
    elif role == "admin":
        win = AdminWindow(user)
    elif role == "teller":
        win = TellerWindow(user)
    elif role == "monitor":
        win = MonitorWindow(user)
    else:
        # fallback: unknown role
        win = AdminWindow(user)

    win.show()
    return win


if __name__ == "__main__":
    app = QApplication([])

    windows = []

    def start_login():
        login = LoginWindow(on_login_success=lambda u: windows.append(open_role_window(u)))
        login.show()
        windows.append(login)

    if not db.super_admin_exists():
        setup = RegisterSuperAdminWindow(on_success=start_login)
        setup.show()
        windows.append(setup)
    else:
        start_login()

    app.exec()
