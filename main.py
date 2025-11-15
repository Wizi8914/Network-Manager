from login_ui import LoginApp

if __name__ == "__main__":
    login_app = LoginApp()
    login_app.protocol("WM_DELETE_WINDOW", login_app.on_closing)
    login_app.mainloop()
    