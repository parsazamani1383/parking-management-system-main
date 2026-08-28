from datetime import datetime
from idlelib.configdialog import font_sample_text

import customtkinter as ctk

from src.utils.plate_converter import (
    to_persian_plate,
)


class DashboardWindow(ctk.CTk):

    def __init__(
        self,
        user,
        dashboard_usecase,
    ):
        super().__init__()

        self.user = user
        self.dashboard_usecase = dashboard_usecase
        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_dashboard
        )
        ctk.set_appearance_mode(
            "dark"
        )

        self.title(
            "سیستم مدیریت پارکینگ"
        )

        #فقط برای سیستم عامل ویندروز
        self.after(0, lambda: self.state("zoomed"))

        self.configure(
            fg_color="#18253a"
        )

        self.load_data()

        self.build_ui()

    def load_data(self):

        self.data = (
            self.dashboard_usecase
            .execute()
        )

    def build_ui(self):

        # =====================
        # HEADER
        # =====================

        header = ctk.CTkFrame(
            self,
            fg_color="#1f2d46",
            corner_radius=12,
        )

        header.pack(
            fill="x",
            padx=20,
            pady=20,
        )

        ctk.CTkLabel(
            header,
            text=f" اپراتور : {self.user.full_name}",
            font=("B Nazanin", 18, "bold"),
        ).pack(
            side="right",
            padx=20,
            pady=15,
        )

        ctk.CTkLabel(
            header,
            text=datetime.now().strftime(
                "%Y/%m/%d"
            ),
            font=("Tomaha", 18),
        ).pack(
            pady=15
        )

        # =====================
        # STATISTICS
        # =====================

        stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        stats_frame.pack(
            fill="x",
            padx=20,
        )

        self.create_stat_card(
            stats_frame,
            "ظرفیت کل",

            str(
                self.data[
                    "total_capacity"
                ]
            ),
        ).pack(
            side="right",
            padx=10,
            pady=10,
            expand=True,
            fill="x",
        )

        self.create_stat_card(
            stats_frame,
            "جایگاه پر",
            str(
                self.data[
                    "occupied_count"
                ]
            ),
        ).pack(
            side="right",
            padx=10,
            pady=10,
            expand=True,
            fill="x",
        )

        self.create_stat_card(
            stats_frame,
            "جایگاه خالی",
            str(
                self.data[
                    "available_count"
                ]
            ),
        ).pack(
            side="right",
            padx=10,
            pady=10,
            expand=True,
            fill="x",
        )

        self.create_stat_card(
            stats_frame,
            "درآمد امروز",
            f"{int(self.data['today_revenue']):,}",
        ).pack(
            side="right",
            padx=10,
            pady=10,
            expand=True,
            fill="x",
        )

        # =====================
        # QUICK MENU
        # =====================

        menu_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        menu_frame.pack(
            fill="x",
            padx=20,
            pady=20,
        )

        ctk.CTkButton(
            menu_frame,
            text="ثبت ورود خودرو +",
            font=("B Nazanin", 18, "bold"),
            fg_color="#16A34A",
            hover_color="#15803D",  # رنگ هنگام Hover
            text_color="white",
            width=220,
            height=50,
            command=self.open_register_entry,
        ).pack(
            side="right",
            padx=10,
        )

        ctk.CTkButton(
            menu_frame,
            text="ثبت خروج خودرو",
            font=("B Nazanin", 18, "bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",  # رنگ هنگام Hover
            text_color="white",
            width=220,
            height=50,
            command=self.open_register_exit,
        ).pack(
            side="right",
            padx=10,
        )

        ctk.CTkButton(
            menu_frame,
            text="خودروهای داخل پارکینگ",
            font=("B Nazanin", 18, "bold"),
            width=220,
            height=50,
            command=self.open_active_vehicles,
        ).pack(
            side="right",
            padx=10,
        )

        if self.user.role == "admin":
            ctk.CTkButton(
                menu_frame,
                text="پنل مدیریت",
                font=("B Nazanin", 18, "bold"),
                fg_color="#7C3AED",
                hover_color="#6D28D9",
                text_color="white",
                width=220,
                height=50,
                command=self.open_admin_panel,
            ).pack(
                side="right",
                padx=10,
            )

        # =====================
        # TABLE
        # =====================

        table_frame = ctk.CTkFrame(
            self,
            fg_color="#1f2d46",
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        ctk.CTkLabel(
            table_frame,
            text="آخرین ترددها",
            font=(
                "B Nazanin",
                22,
                "bold",
            ),
        ).pack(
            pady=20
        )

        headers = [
            "شناسه",
            "پلاک",
            "نوع خودرو",
            "جایگاه",
            "وضعیت",
        ]

        header_row = ctk.CTkFrame(
            table_frame,
            fg_color="#162238",
        )

        header_row.pack(
            fill="x",
            padx=10,
        )

        for item in headers:

            ctk.CTkLabel(
                header_row,
                text=item,
                width=190,
                font=(
                    "B Nazanin",
                    18,
                    "bold",
                ),
            ).pack(
                side="right",
                pady=10,
            )

        for session in self.data[
            "recent_sessions"
        ]:

            row = ctk.CTkFrame(
                table_frame,
                fg_color="#243552",
            )

            row.pack(
                fill="x",
                padx=10,
                pady=5,
            )

            # شناسه

            ctk.CTkLabel(
                row,
                text=str(
                    session["id"]
                ),
                width=180,
                font=("B Nazanin", 14, "bold"),
            ).pack(
                side="right",
                pady=10,
            )

            # پلاک

            plate_container = (
                ctk.CTkFrame(
                    row,
                    fg_color="transparent",
                    width=180,
                )
            )

            plate_container.pack(
                side="right",
                pady=5,
            )

            self.create_plate_widget(
                plate_container,
                session[
                    "plate_number"
                ],
            ).pack()

            # نوع خودرو

            ctk.CTkLabel(
                row,
                text=(
                    "سواری"
                    if session[
                        "vehicle_type"
                    ] == "car"
                    else "موتور"
                ),
                width=180,
                font=("B Nazanin", 16),
            ).pack(
                side="right",
                pady=10,
            )

            # جایگاه

            ctk.CTkLabel(
                row,
                text=session[
                    "spot_number"
                ],
                width=180,
                font=("Tomaha", 14,),
            ).pack(
                side="right",
                pady=10,
            )

            # وضعیت

            ctk.CTkLabel(
                row,
                text=(
                    "فعال"
                    if session[
                        "session_status"
                    ] == "active"
                    else "خروج شده"
                ),
                width=180,
                font=("B Nazanin", 16,'bold'),
            ).pack(
                side="right",
                pady=10,
            )

    def create_stat_card(
        self,
        parent,
        title,
        value,
    ):

        card = ctk.CTkFrame(
            parent,
            height=120,
            fg_color="#1f2d46",
            corner_radius=12,
        )

        card.pack_propagate(
            False
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("B Nazanin", 24, "bold"),
            text_color="#FBBF24",  # رنگ دلخواه
        ).pack(
            pady=(20, 10)
        )

        ctk.CTkLabel(
            card,
            text=value,
            font=(
                "B Nazanin",
                28,
                "bold",
            ),
            text_color="#22D3EE",
        ).pack()

        return card

    def create_plate_widget(
        self,
        parent,
        plate_number,
    ):

        plate = (
            to_persian_plate(
                plate_number
            )
        )

        parts = plate.split()

        frame = ctk.CTkFrame(
            parent,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#1a1a1a",
            height=42,
        )

        widths = [
            50,
            40,
            70,
            50,
        ]

        for i, part in enumerate(parts):

            ctk.CTkLabel(
                frame,
                text=part,
                width=widths[i],
                text_color="black",
                font=(
                    "B Nazanin",
                    18,
                    "bold",
                ),
            ).pack(
                side="right",
                padx=2,
                pady=6,
            )

        return frame

    def open_register_entry(self):

        from src.ui.desktop.register_entry_window import (
            RegisterEntryWindow,
        )

        window = RegisterEntryWindow(
            self,
            self.user,
        )

        self.wait_window(window)

        self.refresh_dashboard()

    def open_register_exit(self):

        from src.ui.desktop.register_exit_window import (
            RegisterExitWindow,
        )

        window = RegisterExitWindow(
            self,
            self.user,
        )

        self.wait_window(window)

        self.refresh_dashboard()

    def refresh_dashboard(self):

        self.load_data()

        for widget in self.winfo_children():
            widget.destroy()

        self.build_ui()

    def close_dashboard(self):

        self.destroy()

    def open_active_vehicles(self):

        from src.ui.desktop.active_vehicles_window import (
            ActiveVehiclesWindow,
        )

        window = ActiveVehiclesWindow(
            self,
            self.user,
        )

        self.wait_window(window)

        self.refresh_dashboard()

    def open_admin_panel(self):

        from src.ui.desktop.admin_panel_window import (
            AdminPanelWindow,
        )

        window = AdminPanelWindow(
            self,
            self.user,
        )

        self.wait_window(window)

        self.refresh_dashboard()