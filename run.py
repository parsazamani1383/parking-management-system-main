import customtkinter as ctk

from src.config.settings import (
    DATABASE_PATH,
)

from src.infrastructure.db.connection import (
    DatabaseConnection,
)

from src.infrastructure.repositories.user_repo_sqlite import (
    UserRepositorySQLite,
)

from src.ui.desktop.login_window import (
    LoginWindow,
)


def main():

    ctk.set_appearance_mode(
        "dark"
    )

    ctk.set_default_color_theme(
        "blue"
    )

    db = DatabaseConnection(
        str(DATABASE_PATH)
    )

    user_repo = (
        UserRepositorySQLite(
            db
        )
    )

    app = LoginWindow(
        user_repo
    )

    app.mainloop()


if __name__ == "__main__":
    main()