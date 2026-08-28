from tkinter import messagebox

import customtkinter as ctk

from src.application.use_cases.create_user_usecase import (
    CreateUserUseCase,
)
from src.application.use_cases.create_user_usecase import CreateUserUseCase
from src.application.use_cases.update_user_usecase import UpdateUserUseCase

class AddUserWindow(ctk.CTkToplevel):

    def __init__(
            self,
            parent,
            user_repo,
            user=None,
    ):
        super().__init__(parent)
        self.user = user

        self.create_usecase = CreateUserUseCase(user_repo)
        self.update_usecase = UpdateUserUseCase(user_repo)

        self.title(
            "ویرایش کاربر"
            if user
            else "افزودن کاربر"
        )

        self.center_on_parent(parent, 450, 470)
        self.resizable(False, False)

        self.configure(
            fg_color="#18253a"
        )

        self.transient(parent)
        self.grab_set()
        self.focus_force()

        self.build_ui()

        if self.user:
            self.load_user()

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text=(
                "ویرایش کاربر"
                if self.user
                else "افزودن کاربر جدید"
            ),
            font=("B Nazanin", 24, "bold"),
        ).pack(
            pady=25
        )

        self.fullname_entry = ctk.CTkEntry(
            self,
            width=320,
            height=42,
            placeholder_text="نام و نام خانوادگی",
            font=("B Nazanin", 14),
            justify="right",
        )

        self.fullname_entry.pack(
            pady=10
        )

        self.username_entry = ctk.CTkEntry(
            self,
            width=320,
            height=42,
            placeholder_text="نام کاربری",
            font=("B Nazanin", 14),
            justify="right",
        )

        self.username_entry.pack(
            pady=10
        )

        self.password_entry = ctk.CTkEntry(
            self,
            width=320,
            height=42,
            placeholder_text="رمز عبور",
            font=("B Nazanin", 14),
            show="●",
            justify="right",
        )

        self.password_entry.pack(
            pady=10
        )

        self.role_menu = ctk.CTkOptionMenu(
            self,
            values=[
                "admin",
                "operator",
            ],
            width=320,
        )

        self.role_menu.pack(
            pady=10
        )

        self.active_var = ctk.BooleanVar(
            value=True
        )

        ctk.CTkCheckBox(
            self,
            text="کاربر فعال باشد",
            font=("B Nazanin", 16, "bold"),
            variable=self.active_var,
        ).pack(
            pady=10
        )

        ctk.CTkButton(
            self,
            text=(
                "ذخیره تغییرات"
                if self.user
                else "ثبت کاربر"
            ),
            font=("B Nazanin", 18, "bold"),
            width=320,
            height=45,
            command=self.save_user,
        ).pack(
            pady=25
        )

    def save_user(self):

        full_name = (
            self.fullname_entry
            .get()
            .strip()
        )

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

        if not full_name:

            messagebox.showerror(
                "خطا",
                "نام را وارد کنید."
            )

            return

        if not username:

            messagebox.showerror(
                "خطا",
                "نام کاربری را وارد کنید."
            )

            return

        if not password:

            messagebox.showerror(
                "خطا",
                "رمز عبور را وارد کنید."
            )

            return

        try:

            if self.user is None:

                self.create_usecase.execute(
                    full_name=full_name,
                    username=username,
                    password=password,
                    role=self.role_menu.get(),
                    is_active=self.active_var.get(),
                )

            else:

                self.update_usecase.execute(
                    user_id=self.user.id,
                    full_name=full_name,
                    username=username,
                    password=password,
                    role=self.role_menu.get(),
                    is_active=self.active_var.get(),
                )

            messagebox.showinfo(
                "موفق",
                "کاربر با موفقیت ثبت شد."
            )

            self.destroy()

        except Exception as ex:

            messagebox.showerror(
                "خطا",
                str(ex)
            )

    def load_user(self):

        self.fullname_entry.insert(
            0,
            self.user.full_name,
        )

        self.username_entry.insert(
            0,
            self.user.username,
        )

        self.role_menu.set(
            self.user.role
        )

        self.active_var.set(
            self.user.is_active
        )

    def center_on_parent(self, parent, width, height):
        parent.update_idletasks()

        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")