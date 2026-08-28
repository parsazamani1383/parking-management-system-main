from datetime import datetime

import customtkinter as ctk

from src.config.settings import DATABASE_PATH

from src.infrastructure.db.connection import DatabaseConnection

from src.infrastructure.repositories.session_repo_sqlite import (
    SessionRepositorySQLite,
)

from src.application.use_cases.show_active_vehicles import (
    ShowActiveVehiclesUseCase,
)

from src.utils.plate_converter import (
    to_persian_plate,
)


class ActiveVehiclesWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        user,
    ):
        super().__init__(parent)
        self.center_window(1200, 700)
        self.user = user

        self.title("خودروهای داخل پارکینگ")

        self.geometry("1200x700")

        self.configure(
            fg_color="#18253a"
        )

        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.lift()

        self.build_usecase()

        self.build_ui()

        self.load_data()

        self.after(
            15000,
            self.auto_refresh,
        )

    # -----------------------------------

    def build_usecase(self):

        db = DatabaseConnection(
            str(DATABASE_PATH)
        )

        repo = SessionRepositorySQLite(db)

        self.usecase = ShowActiveVehiclesUseCase(
            repo
        )

    # -----------------------------------

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="خودروهای داخل پارکینگ",
            font=("B Nazanin", 24, "bold"),
        )

        title.pack(
            pady=(20, 10)
        )

        # Search

        self.search_var = ctk.StringVar()

        self.search_entry = ctk.CTkEntry(
            self,
            width=450,
            height=42,
            textvariable=self.search_var,
            justify="right",
            placeholder_text="جستجوی پلاک...",
            font=("B Nazanin", 24, "bold"),
        )

        self.search_entry.pack(
            pady=10
        )

        self.search_var.trace_add(
            "write",
            lambda *args: self.load_data()
        )

        # Info

        self.info_label = ctk.CTkLabel(
            self,
            text="",
            font=("Tahoma", 14),
        )

        self.info_label.pack(
            pady=(0, 15)
        )
        header = ctk.CTkFrame(
            self,
            fg_color="#162238",
        )

        header.pack(
            fill="x",
            padx=20,
        )

        headers = [
            "پلاک",
            "نوع",
            "جایگاه",
            "ورود",
            "مدت توقف",
            "عملیات",
        ]

        widths = [
            450,
            160,
            120,
            110,
            180,
            160,
        ]

        for text, width in zip(
                headers,
                widths,
        ):
            ctk.CTkLabel(
                header,
                text=text,
                width=width,
                font=("B Nazanin", 18, "bold"),
            ).pack(
                side="right",
                pady=10,
            )

        # Scroll

        self.scroll = ctk.CTkScrollableFrame(
            self,
            width=1120,
            height=520,
            fg_color="#1f2d46",
        )

        self.scroll.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True,
        )

        # Status

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=("B Nazanin", 13),
        )

        self.status_label.pack(
            pady=10
        )

    # -----------------------------------

    def load_data(self):

        for widget in self.scroll.winfo_children():
            widget.destroy()

        sessions = self.usecase.execute(
            self.search_var.get().strip()
        )

        self.info_label.configure(
            text=f"تعداد خودروهای داخل پارکینگ : {len(sessions)}",
            font = ("B Nazanin", 14, "bold"),
        )

        for session in sessions:

            self.add_row(session)

        self.status_label.configure(
            text=f"آخرین بروزرسانی : {datetime.now().strftime('%H:%M:%S')}",
            font = ("B Nazanin", 14, "bold"),
        )

    # -----------------------------------

    def add_row(
        self,
        session,
    plate=None):

        entry = datetime.fromisoformat(
            session["entry_time"]
        )

        row = ctk.CTkFrame(
            self.scroll,
            fg_color=self.get_row_color(entry),
            height=55,
        )

        row.pack(
            fill="x",
            padx=10,
            pady=6,
        )

        row.grid_columnconfigure(0, minsize=250)
        row.grid_columnconfigure(1, minsize=130)
        row.grid_columnconfigure(2, minsize=100)
        row.grid_columnconfigure(3, minsize=120)
        row.grid_columnconfigure(4, minsize=180)
        row.grid_columnconfigure(5, minsize=160)

        plate_frame = ctk.CTkFrame(
            row,
            fg_color="transparent",
            width=240,
        )

        plate_frame.pack(
            side="right",
        )

        self.create_plate_widget(
            plate_frame,
            session["plate_number"],
        ).pack()

        ctk.CTkLabel(
            row,
            text= plate,
            width=230,
            font=("Tahoma", 15),
        ).pack(
            side="right",
            padx=8,
        )

        ctk.CTkLabel(
            row,
            text="سواری"
            if session["vehicle_type"] == "car"
            else "موتور",
            width=120,
        ).pack(
            side="right",
            padx=8,
        )

        ctk.CTkLabel(
            row,
            text=session["spot_number"],
            width=100,
        ).pack(
            side="right",
            padx=8,
        )

        entry = datetime.fromisoformat(
            session["entry_time"]
        )

        ctk.CTkLabel(
            row,
            text=entry.strftime("%H:%M"),
            width=120,
        ).pack(
            side="right",
            padx=8,
        )

        duration = datetime.now() - entry

        hours = duration.seconds // 3600

        minutes = (duration.seconds % 3600) // 60

        ctk.CTkLabel(
            row,
            text=f"{hours}h {minutes}m",
            width=120,
        ).pack(
            side="right",
            padx=8,
        )

        exit_btn = ctk.CTkButton(
            row,
            text=" خروج ثبت ",
            font=("B Nazanin", 14, "bold"),
            width=120,
            command=lambda sid=session["session_id"]:
            self.open_exit(sid),
        )

        exit_btn.pack(
            side="left",
            padx=15,
        )

    # -----------------------------------

    def open_exit(
        self,
        session_id,
    ):
        print(session_id)

        from src.ui.desktop.register_exit_window import (
            RegisterExitWindow,
        )

        window = RegisterExitWindow(
            self,
            self.user,
            session_id=session_id,
        )

        self.wait_window(
            window
        )

        self.load_data()

    def create_plate_widget(
            self,
            parent,
            plate_number,
    ):

        parts = to_persian_plate(
            plate_number
        ).split()

        frame = ctk.CTkFrame(
            parent,
            fg_color="white",
            border_width=1,
            border_color="#222",
            corner_radius=8,
            height=38,
        )

        widths = [
            45,
            35,
            60,
            45,
        ]

        for i, part in enumerate(parts):
            ctk.CTkLabel(
                frame,
                text=part,
                width=widths[i],
                text_color="black",
                font=("Tahoma", 13, "bold"),
            ).pack(
                side="right",
                padx=2,
                pady=5,
            )

        return frame

    def format_duration(
            self,
            entry_time,
    entry=None):

        delta = datetime.now() - entry_time

        days = delta.days

        hours = delta.seconds // 3600

        minutes = (
                          delta.seconds % 3600
                  ) // 60

        if days:
            return f"{days} روز {hours} ساعت"

        if hours:
            return self.format_duration(entry)

        return f"{minutes} دقیقه"

    def get_row_color(
            self,
            entry_time,
    ):

        delta = datetime.now() - entry_time

        hours = delta.total_seconds() / 3600

        if hours >= 24:
            return "#7f1d1d"

        if hours >= 12:
            return "#92400e"

        return "#243552"

    def auto_refresh(self):

        if not self.winfo_exists():
            return

        self.load_data()

        self.after(
            15000,
            self.auto_refresh,
        )

    def center_window(self, width, height):
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")