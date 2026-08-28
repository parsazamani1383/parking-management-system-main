from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk
from oci import self

from src.config.settings import DATABASE_PATH

from src.application.services.fee_calculator import (
    FeeCalculator,
)

from src.infrastructure.db.connection import (
    DatabaseConnection,
)

from src.infrastructure.repositories.vehicle_repo_sqlite import (
    VehicleRepositorySQLite,
)

from src.infrastructure.repositories.session_repo_sqlite import (
    SessionRepositorySQLite,
)

from src.infrastructure.repositories.spot_repo_sqlite import (
    SpotRepositorySQLite,
)

from src.infrastructure.repositories.tariff_repo_sqlite import (
    TariffRepositorySQLite,
)

from src.infrastructure.repositories.receipt_repo_sqlite import (
    ReceiptRepositorySQLite,
)

from src.application.use_cases.register_exit_usecase import (
    RegisterExitUseCase,
)

from src.utils.plate_converter import (
    to_database_plate,
    to_persian_plate,
)
import os

from src.utils.receipt_pdf import ReceiptPDF

class RegisterExitWindow(
    ctk.CTkToplevel
):

    def __init__(
            self,
            parent,
            user,
            session_id=None,
    ):

        super().__init__(parent)

        self.transient(parent)

        self.lift()

        self.focus_force()

        self.grab_set()

        self.user = user

        self.selected_vehicle = None
        self.session_id = session_id
        self.current_fee = 0

        self.title(
            "ثبت خروج خودرو"
        )

        self.center_on_parent(parent, 800, 650)

        self.resizable(
            False,
            False,
        )

        self.configure(
            fg_color="#18253a"
        )

        self.build_ui()
        if self.session_id is not None:
            self.load_session(self.session_id)

    def validate_two_digits(self, value):

        if value == "":
            return True

        return value.isdigit() and len(value) <= 2

    def validate_three_digits(self, value):

        if value == "":
            return True

        return value.isdigit() and len(value) <= 3

    def build_ui(self):

        vcmd2 = (self.register(self.validate_two_digits), "%P")
        vcmd3 = (self.register(self.validate_three_digits), "%P")

        title = ctk.CTkLabel(
            self,
            text="ثبت خروج خودرو",
            font=(
                "B Nazanin",
                24,
                "bold",
            ),
        )

        title.pack(
            pady=20
        )

        # =====================
        # پلاک
        # =====================

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
            validatecommand=vcmd2,
        )
        self.right_entry.pack(
            side="right",
            padx=10,
        )

        self.middle_entry = ctk.CTkEntry(
            plate_frame,
            width=90,
            height=45,
            justify="center",
            placeholder_text="123",
            validate="key",
            validatecommand=vcmd3,
        )
        self.middle_entry.pack(
            side="right",
            padx=5,
        )



        self.letter_menu = (
            ctk.CTkOptionMenu(
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
            validatecommand=vcmd2,
        )
        self.left_entry.pack(
            side="right",
            padx=5,
        )

        # =====================
        # جستجو
        # =====================

        search_btn = ctk.CTkButton(
            self,
            text="جستجوی خودرو",
            font = ("B Nazanin", 18, "bold"),
            width=300,
            height=45,
            command=self.search_vehicle,
        )

        search_btn.pack(
            pady=15
        )

        # =====================
        # اطلاعات
        # =====================

        info_frame = ctk.CTkFrame(
            self,
            width=700,
            height=220,
        )

        info_frame.pack(
            pady=20,
            padx=20,
            fill="x",
        )

        self.plate_label = ctk.CTkLabel(
            info_frame,
            text="پلاک: -",
            font=("B Nazanin", 14, "bold"),
        )

        self.plate_label.pack(
            anchor="center",
            padx=20,
            pady=10,
        )

        self.spot_label = ctk.CTkLabel(
            info_frame,
            text="جایگاه: -",
            font=("B Nazanin", 14, "bold"),
        )

        self.spot_label.pack(
            anchor="center",
            padx=20,
            pady=10,
        )

        self.entry_label = ctk.CTkLabel(
            info_frame,
            text="زمان ورود: -",
            font=("B Nazanin", 14, "bold"),
        )

        self.entry_label.pack(
            anchor="center",
            padx=20,
            pady=10,
        )

        self.duration_label = ctk.CTkLabel(
            info_frame,
            text="مدت توقف: -",
            font=("B Nazanin", 14, "bold"),
        )

        self.duration_label.pack(
            anchor="center",
            padx=20,
            pady=10,
        )

        self.fee_label = ctk.CTkLabel(
            info_frame,
            text="مبلغ: -",
            font=(
                "B Nazanin",
                18,
                "bold",
            ),
        )

        self.fee_label.pack(
            anchor="center",
            padx=20,
            pady=15,
        )

        # =====================
        # روش پرداخت
        # =====================

        self.payment_var = (
            ctk.StringVar(
                value="cash"
            )
        )

        payment_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        payment_frame.pack(
            pady=10
        )

        ctk.CTkRadioButton(
            payment_frame,
            text="نقدی",
            font=("B Nazanin", 18, "bold"),
            variable=self.payment_var,
            value="cash",
        ).pack(
            side="right",
            padx=20,
        )

        ctk.CTkRadioButton(
            payment_frame,
            text="کارت",
            font=("B Nazanin", 18, "bold"),
            variable=self.payment_var,
            value="card",
        ).pack(
            side="right",
            padx=20,
        )

        self.exit_btn = ctk.CTkButton(
            self,
            text="ثبت خروج و چاپ رسید",
            font=("B Nazanin", 20, "bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",  # رنگ هنگام Hover
            text_color="white",
            width=350,
            height=80,
            state="disabled",
            command=self.register_exit,
        )

        self.exit_btn.pack(
            pady=22
        )

    def load_session(
            self,
            session_id,
    ):

        db = DatabaseConnection(
            str(DATABASE_PATH)
        )

        session_repo = SessionRepositorySQLite(db)

        info = session_repo.get_active_session_info(
            session_id
        )

        if info is None:
            return

        parts = to_persian_plate(
            info["plate_number"]
        ).split()

        self.left_entry.insert(
            0,
            parts[0],
        )

        self.letter_menu.set(
            parts[1],
        )

        self.middle_entry.insert(
            0,
            parts[2],
        )

        self.right_entry.insert(
            0,
            parts[3],
        )

        self.search_vehicle()

    def search_vehicle(self):

        try:

            plate = (
                f"{self.left_entry.get()} "
                f"{self.letter_menu.get()} "
                f"{self.middle_entry.get()} "
                f"{self.right_entry.get()}"
            )

            db_plate = (
                to_database_plate(
                    plate
                )
            )

            db = DatabaseConnection(
                str(DATABASE_PATH)
            )

            vehicle_repo = (
                VehicleRepositorySQLite(
                    db
                )
            )

            session_repo = (
                SessionRepositorySQLite(
                    db
                )
            )

            tariff_repo = (
                TariffRepositorySQLite(
                    db
                )
            )

            vehicle = (
                vehicle_repo
                .get_by_plate(
                    db_plate
                )
            )

            if vehicle is None:
                messagebox.showerror(
                    "خطا",
                    "خودرو یافت نشد"
                )

                return

            session = (
                session_repo
                .get_active_by_vehicle(
                    vehicle.id
                )
            )

            if session is None:
                messagebox.showerror(
                    "خطا",
                    "خودرو داخل پارکینگ نیست"
                )

                return

            self.selected_vehicle = (
                db_plate
            )

            tariff = (
                tariff_repo
                .get_active_tariff(
                    vehicle.vehicle_type
                )
            )

            exit_time = (
                datetime.now()
            )

            duration = (
                    exit_time
                    - session.entry_time
            )

            hours = (
                    duration.total_seconds()
                    / 3600
            )

            hours = max(
                1,
                int(hours) + 1
            )

            fee = (
                    tariff.base_rate
                    +
                    max(
                        0,
                        hours - 1
                    )
                    *
                    tariff.hourly_rate
            )

            if (
                    tariff.daily_rate > 0
                    and fee >
                    tariff.daily_rate
            ):
                fee = (
                    tariff.daily_rate
                )

            self.current_fee = fee

            self.plate_label.configure(
                text=(
                        "پلاک: "
                        +
                        to_persian_plate(
                            db_plate
                        )
                )
            )

            self.spot_label.configure(
                text=(
                        "جایگاه: "
                        +
                        str(
                            session.spot_id
                        )
                )
            )

            self.entry_label.configure(
                text=(
                        "زمان ورود: "
                        +
                        session.entry_time.strftime(
                            "%Y/%m/%d %H:%M"
                        )
                )
            )

            self.duration_label.configure(
                text=(
                    f"مدت توقف: "
                    f"{hours} ساعت"
                )
            )

            self.fee_label.configure(
                text=(
                    f"مبلغ: "
                    f"{int(fee):,}"
                    f" تومان"
                )
            )

            self.exit_btn.configure(
                state="normal"
            )

        except Exception as ex:

            messagebox.showerror(
                "خطا",
                str(ex)
            )

    def register_exit(self):

        if (
                self.selected_vehicle
                is None
        ):
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

            session_repo = (
                SessionRepositorySQLite(
                    db
                )
            )

            spot_repo = (
                SpotRepositorySQLite(
                    db
                )
            )

            tariff_repo = (
                TariffRepositorySQLite(
                    db
                )
            )

            receipt_repo = (
                ReceiptRepositorySQLite(
                    db
                )
            )

            usecase = (
                RegisterExitUseCase(
                    vehicle_repo,
                    session_repo,
                    spot_repo,
                    receipt_repo,
                    tariff_repo,
                )
            )

            result = (
                usecase.execute(
                    plate_number=
                    self.selected_vehicle,

                    payment_method=
                    self.payment_var.get(),
                )
            )

            receipt = (
                result[
                    "receipt"
                ]
            )

            vehicle = result["vehicle"]
            session = result["session"]

            spot = spot_repo.get_by_id(
                result["session"].spot_id
            )

            pdf_path = ReceiptPDF.create(
                receipt=receipt,
                vehicle=vehicle,
                session=session,
                spot=spot,
            )

            answer = messagebox.askyesno(
                "ثبت خروج",
                "خروج خودرو با موفقیت ثبت شد.\n\n"
                "آیا مایل به مشاهده و چاپ رسید هستید؟"
            )

            if answer:
                os.startfile(pdf_path)

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