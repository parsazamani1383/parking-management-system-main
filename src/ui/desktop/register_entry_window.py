from tkinter import messagebox

import customtkinter as ctk

from src.config.settings import (
    DATABASE_PATH,
)

from src.infrastructure.db.connection import (
    DatabaseConnection,
)

from src.infrastructure.repositories.vehicle_repo_sqlite import (
    VehicleRepositorySQLite,
)

from src.infrastructure.repositories.spot_repo_sqlite import (
    SpotRepositorySQLite,
)

from src.infrastructure.repositories.session_repo_sqlite import (
    SessionRepositorySQLite,
)

from src.application.use_cases.register_entry import (
    RegisterEntryUseCase,
)
from src.utils.plate_converter import (
    to_database_plate,
)

class RegisterEntryWindow(
    ctk.CTkToplevel
):

    def __init__(
        self,
        parent,
        user,
    ):

        super().__init__(parent)

        self.transient(parent)

        self.lift()

        self.focus_force()

        self.grab_set()

        self.user = user

        self.title(
            "ثبت ورود خودرو"
        )

        self.center_on_parent(parent, 450, 350)

        self.resizable(
            False,
            False,
        )

        self.configure(
            fg_color="#18253a"
        )


        self.two_digit_validator = (
            self.register(self.validate_two_digits),
            "%P",
        )

        self.three_digit_validator = (
            self.register(self.validate_three_digits),
            "%P",
        )
        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="ثبت ورود خودرو",
            font=("B Nazanin", 24, "bold"),
        )

        title.pack(
            pady=20
        )
        plate_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        plate_frame.pack(
            pady=15
        )

        self.right_entry = ctk.CTkEntry(
            plate_frame,
            width=70,
            height=45,
            justify="center",
            placeholder_text="88",
            validate="key",
            validatecommand=self.two_digit_validator,
        )

        self.right_entry.pack(
            side="right",
            padx=5,
        )

        self.middle_entry = ctk.CTkEntry(
            plate_frame,
            width=90,
            height=45,
            justify="center",
            placeholder_text="123",
            validate="key",
            validatecommand=self.three_digit_validator,
        )

        self.middle_entry.pack(
            side="right",
            padx=5,
        )

        self.letter_menu = ctk.CTkOptionMenu(
            plate_frame,
            values=[
                "الف",
                "ب",
                "پ",
                "ت",
                "ج",
                "د",
                "س",
                "ط",
                "ل",
                "م",
                "ن",
                "و",
                "ه",
                "ی",
            ],
            width=80,
            height=45,
        )

        self.letter_menu.pack(
            side="right",
            padx=5,
        )

        self.left_entry = ctk.CTkEntry(
            plate_frame,
            width=70,
            height=45,
            justify="center",
            placeholder_text="44",
            validate="key",
            validatecommand=self.two_digit_validator,
        )

        self.left_entry.pack(
            side="right",
            padx=5,
        )

        self.vehicle_type = ctk.CTkOptionMenu(
            self,
            values=[
                "car",
                "motorcycle",
            ],
            width=350,
            height=45,
        )

        self.vehicle_type.pack(
            pady=15
        )

        save_btn = ctk.CTkButton(
            self,
            text="ثبت ورود",
            font=("B Nazanin", 18
                      , "bold"),
            fg_color="#16A34A",
            hover_color="#15803D",  # رنگ هنگام Hover
            text_color="white",
            width=350,
            height=45,
            command=self.register_entry,
        )

        save_btn.pack(
            pady=25
        )

    def register_entry(self):

        left = self.left_entry.get().strip()
        middle = self.middle_entry.get().strip()
        right = self.right_entry.get().strip()

        if not left.isdigit() or len(left) != 2:
            messagebox.showerror(
                "خطا",
                "دو رقم سمت چپ پلاک باید دقیقاً ۲ رقم باشد."
            )
            return

        if not middle.isdigit() or len(middle) != 3:
            messagebox.showerror(
                "خطا",
                "سه رقم وسط پلاک باید دقیقاً ۳ رقم باشد."
            )
            return

        if not right.isdigit() or len(right) != 2:
            messagebox.showerror(
                "خطا",
                "دو رقم سمت راست پلاک باید دقیقاً ۲ رقم باشد."
            )
            return

        plate = (
            f"{self.left_entry.get()} "
            f"{self.letter_menu.get()} "
            f"{self.middle_entry.get()} "
            f"{self.right_entry.get()}"
        )

        plate = to_database_plate(plate)

        if not plate:

            messagebox.showerror(
                "خطا",
                "پلاک را وارد کنید"
            )

            return

        try:

            db = DatabaseConnection(
                str(DATABASE_PATH)
            )

            vehicle_repo = (
                VehicleRepositorySQLite(
                    db
                )
            )

            spot_repo = (
                SpotRepositorySQLite(
                    db
                )
            )

            session_repo = (
                SessionRepositorySQLite(
                    db
                )
            )

            usecase = (
                RegisterEntryUseCase(
                    vehicle_repo,
                    spot_repo,
                    session_repo,
                )
            )

            session = usecase.execute(
                plate_number=plate,
                vehicle_type=self.vehicle_type.get(),
                shift_id=self.user.id,
            )

            messagebox.showinfo(
                "موفق",
                f"ورود خودرو ثبت شد\n"
                f"شماره نشست: {session.id}"
            )

            self.destroy()

        except Exception as ex:

            messagebox.showerror(
                "خطا",
                str(ex)
            )

    def center_on_parent(self, parent, width, height):
        parent.update_idletasks()

        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

    def validate_two_digits(self, value):

        if value == "":
            return True

        return value.isdigit() and len(value) <= 2

    def validate_three_digits(self, value):

        if value == "":
            return True

        return value.isdigit() and len(value) <= 3