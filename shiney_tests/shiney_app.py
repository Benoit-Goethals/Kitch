from shiny import App, reactive, render, ui
import pandas as pd
import datetime
import io
from pandas.api.types import is_numeric_dtype

# Initial empty DataFrame
person_data = pd.DataFrame(columns=[
    "person_id", "address_id", "name_first", "name_last", "name_title",
    "job_description", "date_of_birth", "phone_number", "email"
])

app_ui = ui.page_fluid(
    ui.h2("Person CRUD Dashboard"),

    ui.navset_tab(
        ui.nav_panel(
            "View Persons",
            ui.input_text("search_filter", "Search by Last Name", ""),
            ui.download_button("download_csv", "Download CSV"),
            ui.output_table("view_person_table"),
        ),
        ui.nav_panel(
            "Add Person",
            ui.layout_columns(
                ui.input_numeric("person_id", "Person ID", value=1, min=1),
                ui.input_numeric("address_id", "Address ID", value=1, min=1),
                ui.input_text("name_first", "First Name", ""),
                ui.input_text("name_last", "Last Name", ""),
                ui.input_text("name_title", "Title", ""),
                ui.input_text("job_description", "Job Description", ""),
                ui.input_date("date_of_birth", "Date of Birth", value=datetime.date.today()),
                ui.input_text("phone_number", "Phone Number", ""),
                ui.input_text("email", "Email", ""),
                ui.input_text("address", "Address", ""),   # Added Address Field
            ),
            ui.input_action_button("add_person", "Add Person"),
        ),
        ui.nav_panel(
            "Update Person",
            ui.input_numeric("update_person_id", "Person ID (to Update)", value=1, min=1),
            ui.input_text("update_column", "Column to Update", ""),
            ui.input_text("update_value", "New Value", ""),
            ui.input_action_button("update_person", "Update"),
        ),
        ui.nav_panel(
            "Delete Person",
            ui.input_numeric("delete_person_id", "Person ID (to Delete)", value=1, min=1),
            ui.input_action_button("delete_person", "Delete"),
        ),
    )
)

def server(input, output, session):
    reactive_person_data = reactive.Value(person_data)

    # ADD
    @reactive.Effect
    @reactive.event(input.add_person)
    def _():
        nonlocal reactive_person_data
        df = reactive_person_data.get()
        if input.person_id() in df["person_id"].values:
            ui.notification_show(f"Person ID {input.person_id()} already exists!", type="warning")
            return

        new_person = {
            "person_id": input.person_id(),
            "address_id": input.address_id(),
            "name_first": input.name_first(),
            "name_last": input.name_last(),
            "name_title": input.name_title(),
            "job_description": input.job_description(),
            "date_of_birth": input.date_of_birth(),
            "phone_number": input.phone_number(),
            "email": input.email(),
        }
        updated_df = pd.concat([df, pd.DataFrame([new_person])], ignore_index=True)
        reactive_person_data.set(updated_df)
        ui.notification_show("Person added successfully!", type="message")

    # UPDATE
    @reactive.Effect
    @reactive.event(input.update_person)
    def _():
        nonlocal reactive_person_data
        df = reactive_person_data.get()
        person_id = input.update_person_id()
        column = input.update_column()
        new_value = input.update_value()

        if person_id not in df["person_id"].values:
            ui.notification_show(f"No person with ID {person_id}", type="warning")
            return

        if column not in df.columns:
            ui.notification_show(f"Column '{column}' doesn't exist.", type="warning")
            return

        # Typecasting
        if is_numeric_dtype(df[column]):
            try:
                new_value = float(new_value)
            except ValueError:
                ui.notification_show("Invalid numeric value", type="warning")
                return

        df.loc[df["person_id"] == person_id, column] = new_value
        reactive_person_data.set(df)
        ui.notification_show("Person updated successfully!", type="message")

    # DELETE
    @reactive.Effect
    @reactive.event(input.delete_person)
    def _():
        nonlocal reactive_person_data
        df = reactive_person_data.get()
        person_id = input.delete_person_id()

        if person_id not in df["person_id"].values:
            ui.notification_show(f"No person with ID {person_id}", type="warning")
            return

        df = df[df["person_id"] != person_id]
        reactive_person_data.set(df)
        ui.notification_show(f"Person ID {person_id} deleted.", type="message")

    # TABLE with search
    @output
    @render.table
    def view_person_table():
        df = reactive_person_data.get()
        keyword = input.search_filter().strip().lower()
        if keyword:
            df = df[df["name_last"].str.lower().str.contains(keyword, na=False)]
        return df

    # CSV DOWNLOAD
    @output
    @render.download(filename="persons.csv")
    def download_csv():
        def writer():
            df = reactive_person_data.get()
            with io.StringIO() as buf:
                df.to_csv(buf, index=False)

        return writer

app = App(app_ui, server)