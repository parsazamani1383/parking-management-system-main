from tkinter import messagebox

import customtkinter as ctk

from src.application.use_cases.create_parking_spot_usecase import (
    CreateParkingSpotUseCase,
)

from src.application.use_cases.update_parking_spot_usecase import (
    UpdateParkingSpotUseCase,
)


class AddParkingSpotWindow(ctk.CTkToplevel):

    def __init__(
            self,
            parent,
            spot_repo,
            spot=None,
    ):
        super().__init__(parent)

        self.spot = spot

        self.create_usecase = CreateParkingSpotUseCase(
            spot_repo
        )

        self.update_usecase = UpdateParkingSpotUseCase(
            spot_repo
        )

        self.title("مدیریت جایگاه")

        self.center_on_parent(parent, 450, 470)
        self.resizable(False, False)

        self.configure(
            fg_color="#18253a"
        )

        self.transient(parent)
        self.grab_set()
        self.focus_force()

        self.build_ui()

        if self.spot:
            self.load_spot()

    def build_ui(self):

        title = (
            "ویرایش جایگاه"
            if self.spot
            else
            "افزودن جایگاه"
        )

        ctk.CTkLabel(
            self,
            text=title,
            font=("B Nazanin", 24, "bold"),
        ).pack(
            pady=25
        )

        self.number_entry = ctk.CTkEntry(
            self,
            width=320,
            height=42,
            placeholder_text="شماره جایگاه",
            justify="center",
            font=("B Nazanin", 14),
        )

        self.number_entry.pack(
            pady=10
        )

        self.type_menu = ctk.CTkOptionMenu(
            self,
            values=[
                "car",
                "motorcycle",
            ],
            width=320,
        )

        self.type_menu.pack(
            pady=10
        )

        self.level_entry = ctk.CTkEntry(
            self,
            width=320,
            height=42,
            placeholder_text="طبقه (اختیاری)",
            font=("B Nazanin", 14),
            justify="center",
        )

        self.level_entry.pack(
            pady=10
        )

        self.section_entry = ctk.CTkEntry(
            self,
            width=320,
            height=42,
            placeholder_text="بخش (اختیاری)",
            font=("B Nazanin", 14),
            justify="center",
        )

        self.section_entry.pack(
            pady=10
        )

        self.active_var = ctk.BooleanVar(
            value=True
        )

        ctk.CTkCheckBox(
            self,
            text="جایگاه فعال باشد",
            font=("B Nazanin", 14),
            variable=self.active_var,
        ).pack(
            pady=10
        )

        ctk.CTkButton(
            self,
            text="ذخیره",
            font=("B Nazanin", 18, "bold"),
            width=320,
            height=45,
            command=self.save_spot,
        ).pack(
            pady=25
        )

    def load_spot(self):

        self.number_entry.insert(
            0,
            self.spot.spot_number,
        )

        self.type_menu.set(
            self.spot.spot_type,
        )

        if self.spot.level_label:
            self.level_entry.insert(
                0,
                self.spot.level_label,
            )

        if self.spot.section_label:
            self.section_entry.insert(
                0,
                self.spot.section_label,
            )

        self.active_var.set(
            self.spot.is_active,
        )

    def save_spot(self):

        try:

            if self.spot is None:

                self.create_usecase.execute(
                    spot_number=self.number_entry.get().strip(),
                    spot_type=self.type_menu.get(),
                    level_label=self.level_entry.get().strip() or None,
                    section_label=self.section_entry.get().strip() or None,
                )

            else:

                self.update_usecase.execute(
                    spot=self.spot,
                    spot_number=self.number_entry.get().strip(),
                    spot_type=self.type_menu.get(),
                    level_label=self.level_entry.get().strip() or None,
                    section_label=self.section_entry.get().strip() or None,
                    is_active=self.active_var.get(),
                )

            messagebox.showinfo(
                "موفق",
                "اطلاعات ذخیره شد."
            )

            self.destroy()

        except Exception as ex:

            messagebox.showerror(
                "خطا",
                str(ex),
            )

    def center_on_parent(self, parent, width, height):
        parent.update_idletasks()

        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")