import os
import flet as ft
from src.analyze_deps import *


def main(page: ft.Page):
    def go_back(e):
        update_appbar(False)
        page.window_width = 500
        page.clean()
        page.add(main_view)

    t = ft.Text(
        value="Welcome 😊\nPlease paste your pubspec.yaml file content below!",
        color="black",
        text_align=ft.TextAlign.CENTER,
    )

    tb = ft.TextField(
        label="Pubspec YAML",
        multiline=True,
        min_lines=5,
        max_lines=5,
        hint_text='Paste here ...',
    )

    def show_snack_bar(msg: str):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
            action="Alright!",
        )
        page.snack_bar.open = True
        page.update()

    def analyze(e):
        if tb.value == '':
            show_snack_bar('You should paste you pubspec first!')
            return

        update_appbar(True)
        page.update()

        page.remove(main_view)

        loading = ft.Container(
            width=500,
            height=260,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.ProgressRing(),
                ],
            ),
        )
        page.add(loading)

        table_data = packages_to_df(parse_yaml(tb.value)['dependencies'])

        page.remove(loading)

        page.window_min_width = page.window_width = 800
        page.window_min_height = page.window_height = 600

        page.add(
            ft.DataTable(
                width=800,
                border=ft.border.all(2, "red"),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(3, "blue"),
                horizontal_lines=ft.border.BorderSide(1, "white"),
                heading_row_color=ft.colors.BLACK12,
                heading_row_height=75,
                data_row_height=39,
                # data_row_color={
                #     ft.MaterialState.HOVERED: ft.colors.RED,
                # },
                divider_thickness=0,
                columns=[
                    ft.DataColumn(ft.Text("Packages")),
                    ft.DataColumn(ft.Text("Android")),
                    ft.DataColumn(ft.Text("iOS")),
                    ft.DataColumn(ft.Text("Linux")),
                    ft.DataColumn(ft.Text("Windows")),
                    ft.DataColumn(ft.Text("macOS")),
                    ft.DataColumn(ft.Text("Web")),
                ],
                rows=table_data.apply(
                    lambda x: ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(x['package'])),
                            ft.DataCell(ft.Text(x['android'])),
                            ft.DataCell(ft.Text(x['ios'])),
                            ft.DataCell(ft.Text(x['linux'])),
                            ft.DataCell(ft.Text(x['windows'])),
                            ft.DataCell(ft.Text(x['macos'])),
                            ft.DataCell(ft.Text(x['web'])),
                        ],
                    ),
                    axis=1,
                ),
            ),
        )

    btn = ft.ElevatedButton(
        "Analyze Pubspec.YAML",
        on_click=analyze,
    )

    # def clear_textfield(_):
    #     tb.value = ''
    #
    # clear_btn = ft.ElevatedButton(
    #     "Clear ❌",
    #     on_click=lambda _: clear_textfield,
    #     style=ft.ButtonStyle(
    #         bgcolor='white',
    #         overlay_color='transparent',
    #     ),
    #     elevation=0,
    # )

    def page_resize(_):
        pass

    page.window_min_width = page.window_width = 500
    page.window_min_height = page.window_height = 500
    page.window_center()
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.window_resizable = True
    page.on_resize = page_resize

    main_view = ft.Container(
        width=500,
        height=260,
        content=ft.Stack(
            [
                ft.Column(
                    controls=[
                        t,
                        tb,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            btn,
                            # clear_btn,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    bottom=7,
                    width=450,
                ),
            ],
        ),
    )

    def toggle_banner(_):
        page.banner.open = not page.banner.open
        main_view.height = 260 if page.banner.open else 385
        tb.max_lines = 5 if page.banner.open else 10
        tb.min_lines = 5 if page.banner.open else 10
        page.update()

    def open_dlg_modal(_):
        def close_dlg(_):
            dlg_modal.open = False
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Exit app"),
            content=ft.Text("Do you really want to skip this amazing app?"),
            actions=[
                ft.TextButton("No", on_click=close_dlg),
                ft.TextButton("Yes", on_click=lambda _: page.window_close()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    page.banner = ft.Banner(
        open=True,
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(
            ft.icons.WARNING_AMBER_ROUNDED,
            color=ft.colors.AMBER,
            size=40
        ),
        content=ft.Text(
            "This is an experimental project!"
        ),
        actions=[
            ft.TextButton("No 😒", on_click=open_dlg_modal),
            ft.TextButton("Yes sir!", on_click=toggle_banner),
        ],
    )

    def update_appbar(is_leading):
        page.appbar = ft.AppBar(
            leading=None if not is_leading else ft.IconButton(
                icon=ft.icons.ARROW_BACK_IOS_NEW,
                on_click=go_back,
            ),
            title=ft.Text("Pubspec Analyzer"),
            center_title=True,
            # bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(icon=ft.icons.WARNING_ROUNDED,
                              on_click=toggle_banner),
            ],
        )

    update_appbar(False)
    page.add(main_view)


ft.app(target=main)

# DEFAULT_FLET_PATH = ''  # or 'ui/path'
# DEFAULT_FLET_PORT = 8502
# if __name__ == "__main__":
#     flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
#     flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))
#     ft.app(name=flet_path, target=main, view=None, port=flet_port)
