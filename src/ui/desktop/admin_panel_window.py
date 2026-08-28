import customtkinter as ctk
from tkinter import messagebox
from src.config.settings import DATABASE_PATH
from src.application.use_cases.update_tariff_usecase import (
    UpdateTariffUseCase,
)
from src.infrastructure.db.connection import DatabaseConnection

from src.infrastructure.repositories.user_repo_sqlite import UserRepositorySQLite
from src.infrastructure.repositories.spot_repo_sqlite import SpotRepositorySQLite
from src.infrastructure.repositories.tariff_repo_sqlite import TariffRepositorySQLite

from src.application.use_cases.admin_panel_usecase import AdminPanelUseCase
from src.infrastructure.repositories.session_repo_sqlite import (
    SessionRepositorySQLite,
)
from src.infrastructure.repositories.receipt_repo_sqlite import (
    ReceiptRepositorySQLite,
)
from src.application.use_cases.reports import (
    ReportsUseCase,
)

class AdminPanelWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        user,
    ):
        super().__init__(parent)
        self.center_window(1350, 800)
        self.user = user

        self.selected_user = None
        self.selected_user_row = None

        self.selected_spot = None
        self.selected_spot_row = None

        self.build_usecase()

        self.title("پنل مدیریت")

        self.geometry("1300x750")

        self.configure(
            fg_color="#18253a"
        )

        self.transient(parent)
        self.grab_set()
        self.focus_force()

        self.build_ui()

        self.load_data()
        self.fill_tariff_data()
        self.load_users()

        self.load_spots()
        self.load_report()

    def build_usecase(self):
        db = DatabaseConnection(
            str(DATABASE_PATH)
        )

        user_repo = UserRepositorySQLite(db)

        spot_repo = SpotRepositorySQLite(db)

        tariff_repo = TariffRepositorySQLite(db)

        session_repo = SessionRepositorySQLite(db)

        receipt_repo = ReceiptRepositorySQLite(db)

        self.usecase = AdminPanelUseCase(
            user_repo,
            spot_repo,
            tariff_repo,
        )

        self.update_tariff_usecase = UpdateTariffUseCase(
            tariff_repo
        )

        self.reports_usecase = ReportsUseCase(
            session_repo,
            spot_repo,
            receipt_repo,
        )

    def load_data(self):
        self.data = self.usecase.execute()

    def build_ui(self):
        title = ctk.CTkLabel(
            self,
            text="پنل مدیریت",
            font=("B Nazanin", 28, "bold"),
        )

        title.pack(pady=20)

        self.tabview = ctk.CTkTabview(
            self,
            width=1200,
            height=620,
        )

        self.tabview.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True,
        )

        self.users_tab = self.tabview.add("کاربران")

        self.tariff_tab = self.tabview.add("تعرفه")

        self.spot_tab = self.tabview.add("جایگاه")

        self.report_tab = self.tabview.add("گزارشها")

        self.build_user_tab()
        self.build_tariff_tab()
        self.build_spot_tab()
        self.build_report_tab()

    def load_users(self):
        print("load_users called")

        for widget in self.user_scroll.winfo_children():
            widget.destroy()

        for user in self.data["users"]:

            row = ctk.CTkFrame(
                self.user_scroll,
                fg_color="#243552",
            )

            row.pack(
                fill="x",
                padx=5,
                pady=4,
            )

            values = [
                user.id,
                user.full_name,
                user.username,
                "ادمین" if user.role == "admin" else "اپراتور",
                "فعال" if user.is_active else "غیرفعال",
            ]

            widths = [100, 250, 220, 160, 150]

            for value, width in zip(values, widths):
                ctk.CTkLabel(
                    row,
                    text=str(value),
                    width=width,
                    font=("B Nazanin", 14),
                ).pack(
                    side="right",
                    pady=8,
                )
                row.bind(
                    "<Button-1>",
                    lambda e, r=row, u=user: self.select_user(r, u)
                )

                for child in row.winfo_children():
                    child.bind(
                        "<Button-1>",
                        lambda e, r=row, u=user: self.select_user(r, u)
                    )

    def select_user(
            self,
            row,
            user,
    ):

        if self.selected_user_row is not None:
            self.selected_user_row.configure(
                fg_color="#243552"
            )

        row.configure(
            fg_color="#2563eb"
        )

        self.selected_user_row = row
        self.selected_user = user

    def open_add_user(self):

        from src.ui.desktop.add_user_window import (
            AddUserWindow,
        )

        window = AddUserWindow(
            self,
            self.usecase.user_repo,
        )

        self.wait_window(window)

        self.load_data()

        self.load_users()

    def open_edit_user(self):

        if self.selected_user is None:
            return

        from src.ui.desktop.add_user_window import AddUserWindow

        window = AddUserWindow(
            self,
            self.usecase.user_repo,
            self.selected_user,
        )

        self.wait_window(window)

        self.load_data()
        self.load_users()

    def toggle_user_status(self):

        if self.selected_user is None:
            if self.selected_user.id == self.user.id:
                messagebox.showwarning(
                    "هشدار",
                    "نمی‌توانید حساب خودتان را غیرفعال کنید."
                )

                return
            messagebox.showwarning(
                "هشدار",
                "ابتدا یک کاربر را انتخاب کنید."
            )

            return

        try:

            if self.selected_user.is_active:

                self.selected_user.deactivate()

            else:

                self.selected_user.activate()

            self.usecase.user_repo.update(
                self.selected_user
            )

            self.load_data()

            self.load_users()

            messagebox.showinfo(
                "موفق",
                "وضعیت کاربر بروزرسانی شد."
            )

        except Exception as ex:

            messagebox.showerror(
                "خطا",
                str(ex)
            )

    def build_tariff_tab(self):

        frame = ctk.CTkFrame(
            self.tariff_tab,
            fg_color="transparent",
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30,
        )

        # ==========================
        # تعرفه سواری
        # ==========================

        car_frame = ctk.CTkFrame(frame)

        car_frame.pack(
            side="right",
            expand=True,
            fill="both",
            padx=15,
            pady=15,
        )

        ctk.CTkLabel(
            car_frame,
            text="تعرفه خودرو سواری",
            font=("B Nazanin", 24, "bold"),
        ).pack(
            pady=15
        )

        ctk.CTkLabel(
            car_frame,
            text="هزینه ورودی",
            font=("B Nazanin", 14, "bold"),
        ).pack()
        self.car_base = ctk.CTkEntry(
            car_frame,
            width=250,
            justify="center",
        )

        self.car_base.pack(pady=5)

        ctk.CTkLabel(
            car_frame,
            text="هزینه هر ساعت",
            font=("B Nazanin", 14, "bold"),
        ).pack()
        self.car_hourly = ctk.CTkEntry(
            car_frame,
            width=250,
            justify="center",
        )

        self.car_hourly.pack(pady=5)

        ctk.CTkLabel(
            car_frame,
            text="سقف هزینه روزانه",
            font=("B Nazanin", 14, "bold"),
        ).pack()
        self.car_daily = ctk.CTkEntry(
            car_frame,
            width=250,
            justify="center",
        )

        self.car_daily.pack(pady=5)

        ctk.CTkButton(
            car_frame,
            text="ذخیره تعرفه سواری",
            font=("B Nazanin", 14, "bold"),
            command=self.save_car_tariff,
        ).pack(
            pady=15
        )

        self.car_tariff_info = ctk.CTkLabel(
            car_frame,
            text="",
            justify="right",
            font=("B Nazanin", 18),
        )

        self.car_tariff_info.pack(
            pady=(15, 5)
        )

        # ==========================
        # تعرفه موتور
        # ==========================

        motor_frame = ctk.CTkFrame(frame)

        motor_frame.pack(
            side="right",
            expand=True,
            fill="both",
            padx=15,
            pady=15,
        )

        ctk.CTkLabel(
            motor_frame,
            text="تعرفه موتور",
            font=("B Nazanin", 24, "bold"),
        ).pack(
            pady=15
        )

        ctk.CTkLabel(
            motor_frame,
            text="هزینه ورودی",
            font=("B Nazanin", 14, "bold"),
        ).pack()
        self.motor_base = ctk.CTkEntry(
            motor_frame,
            width=250,
            justify="center",
        )

        self.motor_base.pack(pady=5)

        ctk.CTkLabel(
            motor_frame,
            text="هزینه هر ساعت",
            font=("B Nazanin", 14, "bold"),
        ).pack()
        self.motor_hourly = ctk.CTkEntry(
            motor_frame,
            width=250,
            justify="center",
        )

        self.motor_hourly.pack(pady=5)

        ctk.CTkLabel(
            motor_frame,
            text="سقف هزینه روزانه",
            font=("B Nazanin", 14, "bold"),
        ).pack()
        self.motor_daily = ctk.CTkEntry(
            motor_frame,
            width=250,
            justify="center",
        )

        self.motor_daily.pack(pady=5)

        ctk.CTkButton(
            motor_frame,
            text="ذخیره تعرفه موتور",
            font=("B Nazanin", 14, "bold"),
            command=self.save_motor_tariff,
        ).pack(
            pady=15
        )

        self.motor_tariff_info = ctk.CTkLabel(
            motor_frame,
            text="",
            justify="right",
            font=("B Nazanin", 18),
            fg_color="transparent",
        )

        self.motor_tariff_info.pack(
            pady=(15, 5)
        )

    def fill_tariff_data(self):

        car = self.data["car_tariff"]
        motor = self.data["motorcycle_tariff"]

        self.car_base.delete(0, "end")
        self.car_hourly.delete(0, "end")
        self.car_daily.delete(0, "end")

        self.motor_base.delete(0, "end")
        self.motor_hourly.delete(0, "end")
        self.motor_daily.delete(0, "end")

        if car:
            self.car_tariff_info.configure(
                text=
                f"تعرفه فعلی\n\n"
                f"هزینه ورودی: {car.base_rate:,} تومان\n"
                f"هزینه هر ساعت: {car.hourly_rate:,} تومان\n"
                f"سقف روزانه: {car.daily_rate:,} تومان"
            )

            self.car_base.insert(0, str(car.base_rate))
            self.car_hourly.insert(0, str(car.hourly_rate))
            self.car_daily.insert(0, str(car.daily_rate))

        if motor:
            self.motor_tariff_info.configure(
                text=
                f"تعرفه فعلی\n\n"
                f"هزینه ورودی: {motor.base_rate:,} تومان\n"
                f"هزینه هر ساعت: {motor.hourly_rate:,} تومان\n"
                f"سقف روزانه: {motor.daily_rate:,} تومان"
            )

            self.motor_base.insert(0, str(motor.base_rate))
            self.motor_hourly.insert(0, str(motor.hourly_rate))
            self.motor_daily.insert(0, str(motor.daily_rate))



    def save_car_tariff(self):

        try:
            self.validate_tariff(
                self.car_base.get(),
                self.car_hourly.get(),
                self.car_daily.get(),
            )

            self.update_tariff_usecase.execute(
                tariff=self.data["car_tariff"],
                base_rate=self.car_base.get(),
                hourly_rate=self.car_hourly.get(),
                daily_rate=self.car_daily.get(),
            )

            messagebox.showinfo(
                "موفق",
                "تعرفه خودرو ذخیره شد."
            )

        except Exception as ex:

            messagebox.showerror(
                "خطا",
                str(ex)
            )
        self.load_data()

        self.car_base.delete(0, "end")
        self.car_hourly.delete(0, "end")
        self.car_daily.delete(0, "end")

        self.motor_base.delete(0, "end")
        self.motor_hourly.delete(0, "end")
        self.motor_daily.delete(0, "end")

        self.load_tariffs()

    def save_motor_tariff(self):

        try:
            self.validate_tariff(
                self.motor_base.get(),
                self.motor_hourly.get(),
                self.motor_daily.get(),
            )

            self.update_tariff_usecase.execute(
                tariff=self.data["motorcycle_tariff"],
                base_rate=self.motor_base.get(),
                hourly_rate=self.motor_hourly.get(),
                daily_rate=self.motor_daily.get(),
            )

            messagebox.showinfo(
                "موفق",
                "تعرفه موتور ذخیره شد."
            )

        except Exception as ex:

            messagebox.showerror(
                "خطا",
                str(ex)
            )
        self.load_data()

        self.car_base.delete(0, "end")
        self.car_hourly.delete(0, "end")
        self.car_daily.delete(0, "end")

        self.motor_base.delete(0, "end")
        self.motor_hourly.delete(0, "end")
        self.motor_daily.delete(0, "end")

        self.load_tariffs()

    def validate_tariff(self, base, hourly, daily):

        fields = {
            "هزینه ورودی": base,
            "هزینه هر ساعت": hourly,
            "سقف هزینه روزانه": daily,
        }

        for name, value in fields.items():

            value = value.strip()

            if value == "":
                raise Exception(f"{name} نمی‌تواند خالی باشد.")

            if not value.isdigit():
                raise Exception(f"{name} باید فقط عدد باشد.")

            number = int(value)

            if number < 0:
                raise Exception(f"{name} نمی‌تواند منفی باشد.")

            if number > 10_000_000:
                raise Exception(f"{name} بیش از حد بزرگ است.")

    def build_spot_tab(self):

        toolbar = ctk.CTkFrame(
            self.spot_tab,
            fg_color="transparent",
        )

        toolbar.pack(
            fill="x",
            padx=20,
            pady=15,
        )

        ctk.CTkButton(
            toolbar,
            text=" افزودن جایگاه + ",
            font=("B Nazanin", 16, "bold"),
            fg_color="#16A34A",
            hover_color="#15803D",  # رنگ هنگام Hover
            text_color="white",

            width=150,
            command=self.open_add_spot,
        ).pack(
            side="right",
            padx=5,
        )

        ctk.CTkButton(
            toolbar,
            text="ویرایش",
            font=("B Nazanin", 16, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB", text_color="white",
            width=120,
            command=self.open_edit_spot,
        ).pack(
            side="right",
            padx=5,
        )

        ctk.CTkButton(
            toolbar,
            text="حذف",
            font=("B Nazanin", 16, "bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",  # رنگ هنگام Hover
            text_color="white",

            width=120,
            command=self.delete_spot,
        ).pack(
            side="right",
            padx=5,
        )

        ctk.CTkButton(
            toolbar,
            text="فعال / غیرفعال",
            font=("B Nazanin", 16, "bold"),
            fg_color="#F59E0B",
            hover_color="#D97706",  # رنگ هنگام Hover
            text_color="white",

            width=150,
            command=self.toggle_spot_status,
        ).pack(
            side="right",
            padx=5,
        )

        header = ctk.CTkFrame(
            self.spot_tab,
            fg_color="#162238",
        )

        header.pack(
            fill="x",
            padx=20,
        )

        headers = [
            "شناسه",
            "شماره",
            "نوع",
            "وضعیت",
            "فعال",
        ]

        widths = [
            100,
            180,
            180,
            180,
            120,
        ]

        for text, width in zip(headers, widths):
            ctk.CTkLabel(
                header,
                text=text,
                width=width,
                font=("B Nazanin", 14, "bold"),
            ).pack(
                side="right",
                pady=10,
            )

        self.spot_scroll = ctk.CTkScrollableFrame(
            self.spot_tab,
            fg_color="#1f2d46",
        )

        self.spot_scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10,
        )

    def build_user_tab(self):
        # ==========================
        # نوار ابزار کاربران
        # ==========================

        toolbar = ctk.CTkFrame(
            self.users_tab,
            fg_color="transparent",
        )

        toolbar.pack(
            fill="x",
            padx=20,
            pady=15,
        )

        ctk.CTkButton(
            toolbar,
            text="افزودن کاربر +",
            font=("B Nazanin", 16, "bold"),
            fg_color="#16A34A",
            hover_color="#15803D",  # رنگ هنگام Hover
            text_color="white",
            width=150,
            command=self.open_add_user,
        ).pack(
            side="right",
            padx=5,
        )

        ctk.CTkButton(
            toolbar,
            text="ویرایش",
            font=("B Nazanin", 16, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB", text_color="white",
            width=120,
            command=self.open_edit_user,
        ).pack(
            side="right",
            padx=5,
        )

        ctk.CTkButton(
            toolbar,
            text="فعال / غیرفعال",
            font=("B Nazanin", 16, "bold"),
            fg_color="#F59E0B",
            hover_color="#D97706",  # رنگ هنگام Hover
            text_color="white",
            width=140,
            command=self.toggle_user_status,
        ).pack(
            side="right",
            padx=5,
        )

        # ==========================
        # هدر جدول
        # ==========================

        header = ctk.CTkFrame(
            self.users_tab,
            fg_color="#162238",
        )

        header.pack(
            fill="x",
            padx=20,
        )

        headers = [
            "شناسه",
            "نام",
            "نام کاربری",
            "نقش",
            "وضعیت",
        ]

        widths = [
            100,
            250,
            220,
            160,
            150,
        ]

        for text, width in zip(headers, widths):
            ctk.CTkLabel(
                header,
                text=text,
                width=width,
                font=("B Nazanin", 15, "bold"),
            ).pack(
                side="right",
                pady=10,
            )

        # ==========================
        # لیست کاربران
        # ==========================

        self.user_scroll = ctk.CTkScrollableFrame(
            self.users_tab,
            fg_color="#1f2d46",
        )

        self.user_scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10,
        )

    def open_add_spot(self):

        from src.ui.desktop.add_parking_spot_window import (
            AddParkingSpotWindow,
        )

        window = AddParkingSpotWindow(
            self,
            self.usecase.spot_repo,
        )

        self.wait_window(window)

        self.load_data()
        self.load_spots()

    def open_edit_spot(self):

        if self.selected_spot is None:
            messagebox.showwarning(
                "هشدار",
                "ابتدا یک جایگاه را انتخاب کنید."
            )

            return

        from src.ui.desktop.add_parking_spot_window import (
            AddParkingSpotWindow,
        )

        window = AddParkingSpotWindow(
            self,
            self.usecase.spot_repo,
            self.selected_spot,
        )

        self.wait_window(window)

        self.load_data()
        self.load_spots()

    def open_add_spot(self):

        from src.ui.desktop.add_parking_spot_window import (
            AddParkingSpotWindow,
        )

        window = AddParkingSpotWindow(
            self,
            self.usecase.spot_repo,
        )

        self.wait_window(window)

        self.load_data()
        self.load_spots()

    def open_edit_spot(self):

        if self.selected_spot is None:
            messagebox.showwarning(
                "هشدار",
                "ابتدا یک جایگاه را انتخاب کنید."
            )

            return

        from src.ui.desktop.add_parking_spot_window import (
            AddParkingSpotWindow,
        )

        window = AddParkingSpotWindow(
            self,
            self.usecase.spot_repo,
            self.selected_spot,
        )

        self.wait_window(window)

        self.load_data()
        self.load_spots()

    def load_spots(self):

        for widget in self.spot_scroll.winfo_children():
            widget.destroy()

        for spot in self.data["spots"]:

            row = ctk.CTkFrame(
                self.spot_scroll,
                fg_color="#243552",
            )

            row.pack(
                fill="x",
                padx=5,
                pady=4,
            )

            values = [
                spot.id,
                spot.spot_number,
                "خودرو" if spot.spot_type == "car" else "موتور",
                {
                    "available": "آزاد",
                    "occupied": "اشغال",
                    "reserved": "رزرو",
                    "out_of_service": "خراب",
                }.get(spot.status, spot.status),
                "فعال" if spot.is_active else "غیرفعال",
            ]

            widths = [100, 180, 180, 180, 120]

            for value, width in zip(values, widths):
                ctk.CTkLabel(
                    row,
                    text=str(value),
                    width=width,
                    font=("B Nazanin", 14),
                ).pack(
                    side="right",
                    pady=8,
                )

            row.bind(
                "<Button-1>",
                lambda e, r=row, s=spot: self.select_spot(r, s),
            )

            for child in row.winfo_children():
                child.bind(
                    "<Button-1>",
                    lambda e, r=row, s=spot: self.select_spot(r, s),
                )

    def select_spot(
            self,
            row,
            spot,
    ):

        if self.selected_spot_row is not None:
            self.selected_spot_row.configure(
                fg_color="#243552"
            )

        row.configure(
            fg_color="#2563eb"
        )

        self.selected_spot_row = row
        self.selected_spot = spot

    def toggle_spot_status(self):

        if self.selected_spot is None:
            messagebox.showwarning(
                "هشدار",
                "ابتدا یک جایگاه را انتخاب کنید."
            )

            return

        self.selected_spot.is_active = (
            not self.selected_spot.is_active
        )

        self.usecase.spot_repo.update(
            self.selected_spot
        )

        self.load_data()
        self.load_spots()

        messagebox.showinfo(
            "موفق",
            "وضعیت جایگاه بروزرسانی شد."
        )

    def delete_spot(self):

        if self.selected_spot is None:
            messagebox.showwarning(
                "هشدار",
                "ابتدا یک جایگاه را انتخاب کنید."
            )

            return

        answer = messagebox.askyesno(
            "حذف",
            "آیا از حذف این جایگاه مطمئن هستید؟"
        )

        if not answer:
            return

        self.usecase.spot_repo.delete(
            self.selected_spot.id
        )

        self.selected_spot = None
        self.selected_spot_row = None

        self.load_data()
        self.load_spots()

        messagebox.showinfo(
            "موفق",
            "جایگاه حذف شد."
        )

    def build_report_tab(self):

        top = ctk.CTkFrame(
            self.report_tab,
            fg_color="transparent",
        )

        top.pack(
            fill="x",
            padx=20,
            pady=20,
        )

        ctk.CTkLabel(
            top,
            text="گزارش درآمد",
            font=("B Nazanin", 22, "bold"),
        ).pack(
            side="right",
            padx=10,
        )

        self.days_entry = ctk.CTkEntry(
            top,
            width=80,
            justify="center",
        )

        self.days_entry.insert(
            0,
            "30"
        )

        self.days_entry.pack(
            side="right",
            padx=10,
        )

        ctk.CTkLabel(
            top,
            text="تعداد روز گذشته:",
            font=("B Nazanin", 16),
        ).pack(
            side="right",
            padx=10,
        )


        ctk.CTkButton(
            top,
            text="نمایش گزارش",
            font=("B Nazanin", 16, "bold"),
            fg_color="#16A34A",
            hover_color="#15803D",  # رنگ هنگام Hover
            text_color="white",
            command=self.load_report,
        ).pack(
            side="right",
            padx=10,
        )

        header = ctk.CTkFrame(
            self.report_tab,
            fg_color="#162238",
        )

        header.pack(
            fill="x",
            padx=20,
        )

        headers = [
            "تاریخ",
            "تعداد تردد",
            "درآمد",
        ]

        widths = [
            250,
            250,
            250,
        ]

        for text, width in zip(headers, widths):
            ctk.CTkLabel(
                header,
                text=text,
                width=width,
                font=("B Nazanin", 15, "bold"),
            ).pack(
                side="right",
                pady=10,
            )

        self.report_scroll = ctk.CTkScrollableFrame(
            self.report_tab,
            fg_color="#1f2d46",
        )

        self.report_scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10,
        )

        self.summary_label = ctk.CTkLabel(
            self.report_tab,
            text="",
            font=("B Nazanin", 18, "bold"),
        )

        self.summary_label.pack(
            pady=15,
        )

    def load_report(self):

        for widget in self.report_scroll.winfo_children():
            widget.destroy()

        value = self.days_entry.get().strip()

        if not value.isdigit():
            messagebox.showwarning(
                "ورودی نامعتبر",
                "تعداد روز باید فقط عدد باشد."
            )
            return

        days = int(value)

        if days < 1 or days > 365:
            messagebox.showwarning(
                "ورودی نامعتبر",
                "تعداد روز باید بین 1 تا 365 باشد."
            )
            return

        reports = self.reports_usecase.daily_revenue_report(
            days
        )
        if not reports:
            messagebox.showinfo(
                "گزارش",
                "هیچ اطلاعاتی برای این بازه زمانی وجود ندارد."
            )
            self.summary_label.configure(text="")
            return

        total_sessions = 0
        total_revenue = 0

        for report in reports:

            row = ctk.CTkFrame(
                self.report_scroll,
                fg_color="#243552",
            )

            row.pack(
                fill="x",
                padx=5,
                pady=4,
            )

            values = [
                report["date"],
                report["sessions"],
                f'{report["revenue"]:,.0f}',
            ]

            widths = [
                250,
                250,
                250,
            ]

            for value, width in zip(values, widths):
                ctk.CTkLabel(
                    row,
                    text=str(value),
                    width=width,
                    font=("B Nazanin", 14),
                ).pack(
                    side="right",
                    pady=8,
                )

            total_sessions += report["sessions"]
            total_revenue += report["revenue"]

        self.summary_label.configure(
            text=
            f"جمع تردد: {total_sessions}        "
            f"جمع درآمد: {total_revenue:,.0f} تومان"
        )

    def center_window(self, width, height):
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")