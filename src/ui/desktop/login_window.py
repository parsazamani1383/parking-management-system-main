import customtkinter as ctk

from pathlib import Path
from tkinter import messagebox

from PIL import Image

from src.ui.desktop.dashboard_window import (
    DashboardWindow,
)

from src.infrastructure.db.connection import (
    DatabaseConnection
)

from src.infrastructure.repositories.spot_repo_sqlite import (
    SpotRepositorySQLite
)

from src.infrastructure.repositories.session_repo_sqlite import (
    SessionRepositorySQLite
)

from src.application.use_cases.dashboard_usecase import (
    DashboardUseCase
)

from src.config.settings import (
    DATABASE_PATH
)

from src.infrastructure.repositories.receipt_repo_sqlite import (
    ReceiptRepositorySQLite,
)

class LoginWindow(ctk.CTk):

    def __init__(
        self,
        user_repo,
    ):
        super().__init__()

        self._user_repo = user_repo
        self.center_window()
        ctk.set_appearance_mode(
            "dark"
        )

        ctk.set_default_color_theme(
            "blue"
        )

        self.title(
            "سیستم مدیریت پارکینگ"
        )

        self.geometry(
            "650x550"
        )

        self.resizable(
            False,
            False,
        )

        self.build_ui()
        # ورود با کلید Enter
        self.bind("<Return>", lambda event: self.login_clicked())

    def build_ui(self):

        main_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30,
        )

        assets_path = (
            Path(__file__).parent.parent
            / "assets"
            / "logo.png"
        )

        if assets_path.exists():

            self.logo_image = ctk.CTkImage(
                light_image=Image.open(
                    assets_path
                ),
                dark_image=Image.open(
                    assets_path
                ),
                size=(220, 120),
            )

            self.logo_label = ctk.CTkLabel(
                main_frame,
                image=self.logo_image,
                text="",
            )

            self.logo_label.pack(
                pady=(20, 10)
            )

        title = ctk.CTkLabel(
            main_frame,
            text="سیستم مدیریت پارکینگ راپـــا",
            font=(
                "B Nazanin",
                32,
                "bold",
            ),
            text_color= "#60A5FA",
        )

        title.pack(
            pady=(10, 5)
        )

        subtitle = ctk.CTkLabel(
            main_frame,
            text="لطفاً وارد حساب کاربری خود شوید",
            font=(
                "B Nazanin",
                14,
            ),
        )

        subtitle.pack(
            pady=(0, 30)
        )

        self.username_entry = (
            ctk.CTkEntry(
                main_frame,
                width=320,
                height=45,
                justify="right",
                placeholder_text="نام کاربری",
                font=(
                    "B Nazanin",14,
                )
            )
        )

        self.username_entry.pack(
            pady=10
        )

        self.password_entry = (
            ctk.CTkEntry(
                main_frame,
                width=320,
                height=45,
                justify="right",
                show="●",
                placeholder_text="رمز عبور",
                font=('B Nazanin', 14),
            )
        )

        self.password_entry.pack(
            pady=10
        )

        login_button = (
            ctk.CTkButton(
                main_frame,
                text="ورود به سیســتم",
                width=320,
                height=45,
                command=self.login_clicked,
                font=(
                    "B Nazanin",18,'bold',
                )
            )
        )

        login_button.pack(
            pady=25
        )

        footer = ctk.CTkLabel(
            main_frame,
            text="Parking Management System(RAPA) v1.0",
            font=(
                "Arial",
                11,
            ),
        )

        footer.pack(
            side="bottom",
            pady=15,
        )

    def login_clicked(self):

        username = (
            self.username_entry
            .get()
            .strip()
        )

        password = (
            self.password_entry
            .get()
            .strip()
        )

        if not username:

            messagebox.showerror(
                "خطا",
                "نام کاربری را وارد کنید",
            )

            return

        if not password:

            messagebox.showerror(
                "خطا",
                "رمز عبور را وارد کنید",
            )

            return

        user = (
            self._user_repo
            .get_by_username(
                username
            )
        )

        if user is None:

            messagebox.showerror(
                "خطا",
                "کاربر یافت نشد",
            )

            return

        if not user.is_active:

            messagebox.showerror(
                "خطا",
                "کاربر غیرفعال است",
            )

            return

        if user.password_hash != password:

            messagebox.showerror(
                "خطا",
                "رمز عبور اشتباه است",
            )

            return

        messagebox.showinfo(
            "خوش آمدید",
            f"{user.full_name}"
        )

        self.destroy()

        db = DatabaseConnection(
            str(DATABASE_PATH)
        )

        spot_repo = SpotRepositorySQLite(
            db
        )

        session_repo = SessionRepositorySQLite(
            db
        )

        receipt_repo = ReceiptRepositorySQLite(
            db
        )

        dashboard_usecase = DashboardUseCase(
            spot_repo,
            session_repo,
            receipt_repo,
        )

        dashboard = DashboardWindow(
            user,
            dashboard_usecase,
        )

        dashboard.mainloop()

    def center_window(self):
        self.update_idletasks()

        width = 450
        height = 550

        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")