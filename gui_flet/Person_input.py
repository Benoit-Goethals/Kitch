import flet as ft
from datetime import datetime

from pygments.lexers.tablegen import KEYWORDS_TYPE


class PersonForm:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Person Input Form"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20

        title = ft.Text(
            "Person Registration Form",
            size=32,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            color=ft.colors.BLUE_700,
        )


        self.name_first = ft.TextField(label="First Name*", width=400)
        self.name_last = ft.TextField(label="Last Name*", width=400)
        self.name_title = ft.TextField(label="Title", width=400)
        self.job_description = ft.TextField(label="Job Description", width=400)
        self.date_of_birth = ft.DatePicker(
            on_change=self.date_changed,
            first_date=datetime(1900, 1, 1),
            last_date=datetime.now()
        )
        self.date_button = ft.ElevatedButton(
            "Pick date of birth",
            icon=ft.icons.CALENDAR_TODAY,
            on_click=lambda _: self.date_of_birth.value,
            width=400
        )
        self.phone_number = ft.TextField(label="Phone Number", width=400)
        self.email = ft.TextField(label="Email", width=400)

        self.submit_button = ft.ElevatedButton(
            text="Submit",
            on_click=self.submit_form,
            width=400,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE_700,
            )
        )

        form_container = ft.Container(
            content=ft.Column(
                [
                    title,
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),

                    self.name_first,
                    self.name_last,
                    self.name_title,
                    self.job_description,
                    self.date_button,
                    self.date_of_birth,
                    self.phone_number,
                    self.email,
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    self.submit_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=20,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_100,
            )
        )

        self.page.add(form_container)

    def date_changed(self, e):
        if self.date_of_birth.value:
            self.date_button.text = self.date_of_birth.value.strftime("%Y-%m-%d")
        self.page.update()

    def validate_form(self):
        if not self.name_first.value or not self.name_last.value:
            return False
        return True

    def submit_form(self, e):
        if self.validate_form():
            person_data = {

                'name_first': self.name_first.value,
                'name_last': self.name_last.value,
                'name_title': self.name_title.value,
                'job_description': self.job_description.value,
                'date_of_birth': self.date_of_birth.value.strftime("%Y-%m-%d") if self.date_of_birth.value else None,
                'phone_number': self.phone_number.value,
                'email': self.email.value
            }
            # Here you can add logic to save the person data
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Form submitted successfully!"))
        else:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Please check your input!"))

        self.page.snack_bar.open = True
        self.page.update()


def main(page: ft.Page):
    PersonForm(page)


if __name__ == '__main__':
    ft.app(target=main)
