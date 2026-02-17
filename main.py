# main.py
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication
import db

from app.ui.login import LoginWindow
from app.ui.register_super_admin import RegisterSuperAdminWindow

from app.ui.super_admin.super_admin_window import SuperAdminWindow
from app.ui.admin.admin_window import AdminWindow
from app.ui.teller.teller_window import TellerWindow
from app.ui.monitor.monitor_window import MonitorWindow


def open_role_window(user, on_logout=None):
    role = user["role"]

    if role == "super_admin":
        win = SuperAdminWindow(user, on_logout=on_logout)
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
    QCoreApplication.setApplicationName("Offline-LAN")
    QCoreApplication.setOrganizationName("Offline-LAN")
    app = QApplication([])

    windows = []

    def start_login():
        def on_login_success(u):
            def do_logout(u=u):
                from app.ui.login import save_remembered_username
                save_remembered_username(u["username"])
                start_login()
            windows.append(open_role_window(u, on_logout=do_logout))

        login = LoginWindow(on_login_success=on_login_success)
        login.show()
        windows.append(login)

    if not db.super_admin_exists():
        setup = RegisterSuperAdminWindow(on_success=start_login)
        setup.show()
        windows.append(setup)
    else:
        start_login()

    app.exec()
