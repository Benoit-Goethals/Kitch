import flet as ft
from datetime import datetime
import re

from pygments.lexers.tablegen import KEYWORDS_TYPE


class PersonForm:
    PICK_DATE_TEXT = "Pick date"

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
        self.job_description = ft.TextField(label="Job Description", width=400,hint_text="Niet grotot",multiline=True,
        min_lines = 1,
        max_lines = 3,
        )
        self.date_of_birth = ft.DatePicker(
            on_change=self.date_changed,
            first_date=datetime(1900, 1, 1),
            last_date=datetime.now()
        )
        self.pick_date_button = ft.ElevatedButton(
            self.PICK_DATE_TEXT,
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=self.open_date_picker
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
                    self.pick_date_button,
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

    def open_date_picker(self, e):
        self.page.open(self.date_of_birth)

    def date_changed(self, e):
        if self.date_of_birth.value:
            self.pick_date_button.text = self.date_of_birth.value.strftime("%Y-%m-%d")
        self.page.update()

    def validate_email(self, email: str) -> bool:
        """Validate the given email address using a regex."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def validate_form(self) -> bool:
        """Validate the form fields and show errors on invalid inputs."""
        is_valid = True

        # Validate First Name
        if not self.name_first.value:
            self.name_first.error_text = "First Name is required"
            is_valid = False
        else:
            self.name_first.error_text = None  # Clear the error if valid

        # Validate Last Name
        if not self.name_last.value:
            self.name_last.error_text = "Last Name is required"
            is_valid = False
        else:
            self.name_last.error_text = None

        # Validate Email
        if not self.email.value:
            self.email.error_text = "Email is required"
            is_valid = False
        elif not self.validate_email(self.email.value):
            self.email.error_text = "Invalid email format"
            is_valid = False
        else:
            self.email.error_text = None

        # Update the page to reflect error messages
        self.page.update()

        return is_valid

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
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Please correct the highlighted errors."))

        self.page.snack_bar.open = True
        self.page.update()


def main(page: ft.Page):
    PersonForm(page)


if __name__ == '__main__':
    ft.app(target=main)