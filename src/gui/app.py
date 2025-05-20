import asyncio
import logging
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from PIL import Image
from shiny import App, ui, reactive, render
from shiny.types import FileInfo
from shiny.types import ImgData

from src.gui.sidebar_choices_enum import SidebarChoices
from src.database_layer.db_service import DBService
from src.domain.DatabaseModelClasses import Address, Person
from src.domain.person_type import PersonType
from src.utils.map_generator import MapGenerator


def _define_table_styles():
    """
    Define CSS styles for the UI, including the taskbar (sidebar) background color.
    """
    return """
    <style>
        /* Style table for other parts */
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #4CAF50;
            color: black;
            font-weight: bold;
            text-transform: uppercase;
        }

        /* Style navigation panel content */
        .nav-panel-content {
            text-align: center;
        }

        /* Center content */
        .center-content {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        /* Sidebar styling: set background to green */
        .layout-sidebar .sidebar {
            background-color: green !important;
            color: white;
        }

        /* Sidebar text color and spacing */
        .layout-sidebar .sidebar select {
            margin: 10px;
            color: black;
        }
    </style>
    """
    # UI style constants


FLEX_COLUMN_STYLE = "display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;"
BUTTON_STYLE = "width: auto; text-align: center;"


class ShinyApplication:
    def __init__(self):
        self.db_service = DBService()
        self.table_styles = _define_table_styles()
        self.app_ui = self._build_ui()
        self.app_server = self._build_server()
        self.map_generator = MapGenerator(self.db_service)
        self.__logger = logging.getLogger(__name__)

    @staticmethod
    def make_path(save_path)->Path:
        path = ""
        system_name = platform.system()
        if system_name == "Windows":
            path = Path("C:\\ProgramData\\Kitch\\photos").joinpath(save_path)
        elif system_name == "Linux":
            logging.info("Running on Linux")
            path = Path.joinpath(Path.home(), "photos", save_path)

        return path

    def _build_ui(self):
        """
        Build the UI layout for the application.
        """
        return ui.page_fluid(
            ui.HTML(self.table_styles),
            ui.navset_bar(
                title=ui.tags.b(ui.tags.div("Project Kitch", style="text-align: center;")),
                bg="#a89ca3",
            ),

            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_select(
                        "sidebar_menu", "Select a Task:",
                        choices=[choice.value for choice in SidebarChoices],
                        selected="Home", multiple=False, size="10"
                    ),
                    ui.input_action_button("exit_button", "Exit App"),  # Add an "Exit App" button

                    class_="sidebar",
                    bg=" #a89ca3"),
                ui.output_ui("selected_content"),
            )
        )

    def _build_server(self):
        """
        Configure the server logic as part of the Shiny application.
        """

        def server(input, output, session):
            # Assume this is the original DataFrame you're passing into your personnel_grid DataGrid
            # Make the dataframe persist by creating a variable to store its global state.
            global personnel_data_store  # Declare global state for personnel grid data

            @reactive.Effect
            @reactive.event(input.personnel_grid_selected_rows)
            def show_person_modal():
                global personnel_data_store  # Access the global store for the DataGrid's DataFrame

                selected_rows = input.personnel_grid_selected_rows()

                if selected_rows and personnel_data_store is not None:
                    df = personnel_data_store
                    if not df.empty:
                        # Get the first selected row index
                        row_index = selected_rows[0]
                        row_data = df.iloc[row_index]  # Get data for the selected row
                        path = ShinyApplication.make_path(row_data["Photo"])  # Get the image path

                        # If the path exists, open the image
                        if path.exists():

                            # Pass base64 string to the render function
                            @output
                            @render.image
                            def img_output():
                                img: ImgData = {"src": str(path), "width": "300px"}

                                return img

                        # Build the modal's content
                        content = ui.div(
                            ui.h4(f"{row_data['First Name']} {row_data['Last Name']}"),
                            ui.p(f"Email: {row_data['Email']}"),
                            ui.p(f"Phone: {row_data['Phone']}"),
                            ui.output_image("img_output"),  # Reference the output function here

                        )

                        # Display the modal
                        ui.modal_show(
                            ui.modal(
                                content,
                                title="Person Details",
                                easy_close=True,
                                size="m"
                            )
                        )

            @reactive.Effect
            def check_exit():
                if input.exit_button():  # When the "Exit App" button is clicked
                    self.__logger.info("Exiting the app...")
                    sys.exit(1)  # Exit with return code 1

            @reactive.Effect
            async def show_map_companies():
                if input.show_map_companys():
                    await self.map_generator.mark_points_companies()

            @reactive.Effect
            async def show_map_heatmap_sales_project():
                if input.show_map_heatmap_sales_project():
                    await self.map_generator.euros_phases()



            @reactive.Effect
            async def show_projects_between_dates_for_person():
                if input.show_projects_between_dates_for_person():
                    person_id = input.person_select()
                    date_range = input.date_range()
                    if not person_id or not date_range:
                        return
                    start_date, end_date = date_range
                    await self.map_generator.project_phases_between_date_for_person(person_id, start_date, end_date)

            @reactive.Effect
            def add_person_modal():
                if input.add_person_modal():
                    content = ui.tags.div(
                        ui.tags.div(
                            [
                                ui.output_table("add_person_effect", style="grid-column: 1 / -1;"),
                                ui.h3("Add New Person", style="grid-column: 1 / -1; text-align: center;"),
                                ui.input_select(
                                    "select_person_type_modal", "Type of person:",
                                    choices=[person_type.name for person_type in PersonType], multiple=False,


                                ),
                                ui.input_text("input_first_name", label="First Name", placeholder="Enter First Name"),
                                ui.input_text("input_last_name", label="Last Name", placeholder="Enter Last Name"),
                                ui.input_text("input_email", label="Email", placeholder="Enter Email Address"),
                                ui.input_text("input_phone", label="Phone Number", placeholder="Enter Phone Number"),
                                ui.h3("Address Details", style="grid-column: 1 / -1; text-align: left;"),
                                ui.input_text("input_street", label="Street", placeholder="Enter Street"),
                                ui.input_text("input_house_number", label="House Number",
                                              placeholder="Enter House Number"),
                                ui.input_text("input_postal_code", label="Postal Code",
                                              placeholder="Enter Postal Code"),
                                ui.input_text("input_municipality", label="Municipality",
                                              placeholder="Enter Municipality"),
                                ui.input_text("input_country", label="Country",
                                              placeholder="Enter Country (default: BE)"),
                                ui.input_file("file_upload", "Choose picture File", accept=[".jpg", "jpeg"],
                                              multiple=False),
                                ui.tags.div(
                                    ui.input_action_button("add_person_btn", "Add Person"),
                                    style="grid-column: 1 / -1; text-align: center;"
                                ),

                            ],
                            style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; align-items: start; padding: 10px;"
                        ),
                        style="display: flex; justify-content: center; padding: 10px;"
                    )
                    # Display the modal
                    ui.modal_show(
                        ui.modal(
                            content,
                            title="Person Details",
                            easy_close=True,
                            size="l"

                        )
                    )

            @output
            @render.ui
            async def selected_content():
                selected = input.sidebar_menu()
                return await self.handle_sidebar_selection(selected, input)

            @output
            @render.text
            def exit_message():
                return "Click 'Exit App' to terminate the application."

            @output
            @render.ui
            async def selected_content():
                selected = input.sidebar_menu()
                return await self.handle_sidebar_selection(selected, input)

            @output
            @render.data_frame
            async def personnel_grid():
                # This is the initial DataFrame for the grid. Make it available globally.
                global personnel_data_store

                person_type = input.select_person_type()

                try:
                    # Fetch persons by type using your DBService
                    persons = await self.db_service.get_all_persons_type(PersonType(person_type))
                except ValueError:
                    print("Invalid person_type provided!")
                    persons = None

                if not persons:
                    df = pd.DataFrame(columns=["ID", "First Name", "Last Name", "Email", "Phone"])
                    personnel_data_store = df  # Store empty DataFrame
                    return df

                # Prepare data
                data = [
                    {
                        "ID": person.person.person_id,
                        "First Name": person.person.name_first,
                        "Last Name": person.person.name_last,
                        "Email": person.person.email or "N/A",
                        "Phone": person.person.phone_number or "N/A",
                    }
                    for person in persons
                ]

                # Generate and store DataFrame globally
                df = pd.DataFrame(data)
                personnel_data_store = df  # Store it globally for access in other parts

                # Render DataGrid
                return render.DataGrid(
                    df,
                    filters=True,
                    selection_mode="row",
                    styles=[
                        {
                            "headerStyle": {"font-weight": "bold", "color": "black"},
                        },
                        {
                            "class": "text-center",
                        },
                        {
                            "cols": [0],
                            "style": {"font-weight": "bold", "background-color": "#ffdbaf"},
                        },
                    ],
                )

            try:

                self.setup_data_fetching()
                self.setup_plots(output, input)
                self.setup_tables(output)
                self.setup_person_operations(input, output)
                self.setup_datagrid(input,output)
                self.setup_timeline_order_line(input, output)

            except Exception as e:
                # Display an error notification with specific details
                ui.notification_show(
                    f"An error occurred: {str(e)}",
                    type="error",
                    duration=5  # Show the notification for 5 seconds
                )

        return server

    async def handle_sidebar_selection(self, selected, input):
        """Handle the selected menu option and render the appropriate UI component."""
        # Dictionary mapping sidebar choices to their handler methods
        sidebar_handlers = {
            SidebarChoices.HOME.value: self._render_home_view,
            SidebarChoices.PROJECT_PLOT.value: self._render_project_plot_view,
            SidebarChoices.COMPANY_TABLE.value: self._render_company_view,
            SidebarChoices.PERSONS_TABLE.value: lambda: self._render_table_ui("Persons List", "persons_table"),
            SidebarChoices.GANTT.value:self._render_gantt_view,
            SidebarChoices.DATA_GRID_PROJECTS.value: self._render_projects_grid_view,
            SidebarChoices.TIMELINE_ORDERLINE.value: self._render_timeline_view,
            SidebarChoices.FILTERS.value: self._render_filters_view,
            SidebarChoices.PERSONEL_FIRM_TABLE.value: self._render_personnel_view
        }

        # Get and execute the appropriate handler
        handler = sidebar_handlers.get(selected)
        if handler:
            return await handler() if asyncio.iscoroutinefunction(handler) else handler()
        return ui.tags.p("Please select a valid tab from the sidebar.")

    async def _render_home_view(self):
        """Render the home view with year selection and plot."""
        self.fill_years_home()
        return ui.h2("Sales percentages of projects in a year"), ui.tags.div(
            ui.tags.div(
                ui.input_select(
                    "year_select", "Select a year:",
                    choices=[], multiple=False, width="500px"
                )
            ),
            ui.output_plot("home", width="600px", height="600px"),
            style=FLEX_COLUMN_STYLE,
            class_="nav-panel-content"
        )


    async def _render_project_plot_view(self):
        """Render the project plot view."""
        await self.fetch_and_update_project_choices()
        return self._render_project_plot_ui()


    async def _render_gantt_view(self):
        """Render the gantt view."""
        await self.fetch_and_update_project_choices()
        return self._render_gantt_char_ui()


    def _render_company_view(self):
        """Render the company table view with map button."""
        return ui.input_action_button(
            "show_map_companys",
            "Show companies on the map",width="300px"

        ), self._render_table_ui("List of all Companies", "company_table")

    def _render_projects_grid_view(self):
        """Render the projects data grid view."""
        return ui.tags.div(
            ui.h2("List of all Projects"),
            ui.input_action_button("show_map_heatmap_sales_project", "Show on the Euro/project map"),
            ui.output_data_frame("data_grid")
        )

    async def _render_timeline_view(self):
        """Render the timeline view."""
        await self.fetch_and_update_project_choices()
        return self._render_timeline()

    async def _render_filters_view(self):
        """Render the filters view."""
        await self.fetch_and_update_person_choices()
        return self._render_datetime_selection_ui()


    async def _render_personnel_view(self):


        return ui.tags.div(
            ui.h2("Personnel Management"),
            ui.tags.div(
                ui.input_select(
                    "select_person_type", "Type of person:",
                    choices=[person_type.name for person_type in PersonType], multiple=False,

                ),
                ui.input_action_button("add_person_modal", "Add", width="100px"),
                ui.output_data_frame("personnel_grid"),
                style="display: flex; flex-direction: column; gap: 20px;"
            )
        )



    def _render_datetime_selection_ui(self):
        """
        Render the UI for selecting a person and datetime range between two dates.
        """
        return ui.tags.div(
            ui.h2("Location of a worker in a time period"),
            ui.input_select(
                "person_select", "Select a Person:",
                choices=[],  # Choices will be populated dynamically
                multiple=False, width="400px"
            ),
            ui.input_date_range(
                "date_range", "Select Date Range:",

                start=datetime(year=1990, month=1, day=1),
                end=(datetime.now().replace(year=datetime.now().year + 1).date()),  # Convert to a `date` object

                width="400px"
            ),
            ui.input_action_button(
                "show_projects_between_dates_for_person", "Apply Filter",
                style="margin-top: 20px; display: inline-block;"
            ),
            ui.output_ui("filter_results"),
            style="display: flex; flex-direction: column; padding: 10px; gap: 15px;"
        )

    async def fetch_and_update_person_choices(self):
        """
        Fetch all persons and update the dropdown for person selection.
        """
        try:
            persons = await self.db_service.get_all_persons()
            if persons:
                choices_select = {
                    person.person_id: f"{person.name_first} {person.name_last}" for person in persons
                }
                ui.update_select("person_select", choices=choices_select)
        except Exception as e:
            self.__logger.info(f"Error fetching persons for dropdown: {e}")


    def _render_gantt_char_ui(self):

        return ui.tags.div(
            ui.h2("Project turnover in the different phases"),
            ui.input_select(
                "project_select", "Select a Project:", choices=[], multiple=False, width="500px"
            ),
            ui.output_ui("gantt_chart", width="600px", height="600px")
        )




    def _render_project_plot_ui(self):
        """
        Render the UI for the "Project plot" menu.
        """
        return ui.tags.div(
            ui.h2("Project turnover in the different phases"),
            ui.input_select(
                "project_select", "Select a Project:", choices=[], multiple=False, width="500px"
            ),
            ui.output_plot("project_plot", width="600px", height="600px"),
            style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;",
            class_="nav-panel-content"
        )

    def _render_timeline(self):
        return ui.tags.div(
            ui.h2("Phase Order timeline"),
            ui.input_select(
                "project_select", "Select a Project:", choices=[], multiple=False, width="500px"
            ),
            ui.output_ui("timeline_plot", width="600px", height="600px"),
            style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;",
            class_="nav-panel-content"
        )

    def _render_table_ui(self, title, table_id):
        """
        Render UI for tables.
        """
        return ui.tags.div(
            ui.h2(title),
            ui.output_table(table_id)
        )


    def fill_years_home(self):
        choices_select = [year for year in range(1990, datetime.now().year + 1)]
        ui.update_select("year_select", choices=choices_select, selected=str(datetime.now().year - 2))

    async def fetch_and_update_project_choices(self):
        """
        Fetch project data and update the dropdown for "Project plot".
        """
        try:
            projects = await self.db_service.get_all_projects()
            if projects:
                choices_select = {
                    project.project_id: (
                        f"Project: {project.project_id} - "
                        f"Client: {project.client.company.company_name}"
                        if project.client else "Unknown"
                    )
                    for project in projects
                }
                ui.update_select("project_select", choices=choices_select)
        except Exception as e:
            self.__logger.error(f"Error fetching projects for dropdown: {e}")

    # Setup files

    def setup_data_fetching(self):
        """
        Set up reactive data fetching functions.
        """

        @reactive.Calc
        def fetch_companies():
            return self.db_service.get_all_companies()

        @reactive.Calc
        async def fetch_projects():
            return await self.db_service.get_all_projects()


    def setup_plots(self, output, input):
        """
        Set up reactive plots.
        """

        @output
        @render.plot
        async def project_plot():
            selected_project = input.project_select()
            if not selected_project:
                return None
            phases = await self.db_service.get_phases_by_project(selected_project)
            return self._generate_project_plot(phases, selected_project)

        @output
        @render.plot
        async def home():
            selected_year = input.year_select()
            projects_with_phases = await self.db_service.get_all_projects_phases_year(selected_year)
            return self._generate_home_plot(projects_with_phases)


        @output
        @render.ui  # Use render.ui instead of render.plot
        async def gantt_chart():
            temp=[]
            data=await self.db_service.get_phases_by_project(input.project_select())
            if data is not None:
                for d in data:
                    temp.append( dict(Resource=f"{d.project.client.company.company_name}", Start=d.date_end_client, Finish=d.date_start_client, Task=f"CLient {d.name}"))
                    temp.append(dict(Resource=f"{d.project.client.company.company_name}", Start=d.date_end_planned,
                                     Finish=d.date_start_planned, Task=f"Planning {d.name}"))
                    print(f"client start {d.date_start_client}  - end {d.date_start_client}")
                    print(f"planning start {d.date_start_planned}  - end {d.date_end_planned}")


            df = pd.DataFrame(data=temp)

            fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource")
            fig.update_xaxes(tickangle=-45, tickformat="%Y-%m-%d")
            #fig.update_yaxes(autorange="reversed")

            return ui.HTML(fig.to_html(full_html=False))

    def _generate_project_plot(self, phases, project_name):
        """
        Generate the project plot based on fetched data.
        """
        if not phases:
            return None
        data = [
            (phase.name,
             sum(order_line.sales_price for order_line in phase.order_lines if order_line.sales_price is not None))
            for phase in phases
        ]
        df = pd.DataFrame(data, columns=["Phase Name", "Total Sales Price"])
        fig, ax = plt.subplots()
        ax.bar(df["Phase Name"], df["Total Sales Price"])
        ax.set_title(f"Total Sales by {project_name}")
        return fig

    def _generate_home_plot(self, projects_with_phases):
        """
        Generate the home plot based on fetched data.
        """
        if not projects_with_phases:
            return None
        total_projects = []
        for project in projects_with_phases:
            total_sales_price = sum([
                ph.sales_price for phase in project.phases
                for ph in phase.order_lines if ph.sales_price is not None
            ])
            total_projects.append((project.project_id, total_sales_price))

        df = pd.DataFrame(total_projects, columns=["Project ID", "Total Sales"])
        fig, ax = plt.subplots()
        ax.pie(
            df["Total Sales"], labels=df["Project ID"], autopct='%1.1f%%', startangle=140
        )
        return fig

    def setup_tables(self, output):
        """
        Set up reactive outputs for tables.
        """

        @output
        @render.table
        async def company_table():
            companies = await self.db_service.get_all_companies()
            if not companies:
                return pd.DataFrame(columns=["Name", "Address", "Contact Person"])
            return pd.DataFrame([
                {
                    "Name": company.company_name,
                    "Address": company.address.street + " " + company.address.house_number + " " + company.address.municipality if company.address else "N/A",
                    "Contact Person": (
                        f"{company.contactperson.name_first} {company.contactperson.name_last}"
                        if company.contactperson else "N/A"
                    )
                }
                for company in companies
            ])

    def setup_person_operations(self, input, output):
        """
        Set up person-related functionality.
        """

        @reactive.calc
        async def upload_and_verify_file():
            file: list[FileInfo] | None = input.file_upload()  # File uploaded by the user
            print(file)
            if not file:
                return None
            try:
                img = _verify_image_file(file[0]["datapath"])
                if img is None:
                    raise ValueError("Uploaded file is not a valid image.")

                # Save the verified image

                save_path = input.file_upload()[0]["name"]
                path = ShinyApplication.make_path(save_path)

                img.save(str(path))  # Save the verified image


                return True
            except Exception as e:
                print(f"Failed to upload and verify file: {e}")
                return False



        def _verify_image_file(file: str) -> Optional[Image.Image]:

            try:
                # Open the image to verify its integrity
                with Image.open(file) as img:
                    img.verify()  # Verify the integrity of the image
                # Reload the image after verification as verify() closes the file pointer
                with Image.open(file) as img:
                    return img.copy()  # Ensure the object remains valid after the context manager

            except Exception as e:
                 print(f"Image verification failed: {e}")
            return None


        @reactive.Effect
        async def add_person_effect():
            if input.add_person_btn():
                person, address, type_personeel = self._build_person_from_inputs(input)
                success = await self.db_service.add_person(person,type_personeel)
                if  success:
                    success= await upload_and_verify_file()
                self.__logger.info(f"Added person: {success}")
                ui.notification_show(f"Person added successfully: {success}")

        @output
        @render.table
        async def persons_table():
            persons = await self.db_service.get_all_persons_with_address()
            return self._generate_persons_table(persons)

    def _build_person_from_inputs(self, input):
        """
        Collect data from input into Person and Address objects.
        """
        address = Address(
            street=input.input_street(), house_number=input.input_house_number(),
            postal_code=input.input_postal_code(), municipality=input.input_municipality(),
            country=input.input_country()
        )

        person = Person(
            name_first=input.input_first_name(), name_last=input.input_last_name(),
            email=input.input_email(), phone_number=input.input_phone(),photo_url=input.file_upload()[0]["name"],
            address=address
        )
        person_type=""
        type_person_input = input.select_person_type()
        if type_person_input == "WORKER":
            person_type = PersonType.WORKER
        elif type_person_input == "EMPLOYEE":
            person_type = PersonType.EMPLOYEE


        return person, address, person_type

    def _generate_persons_table(self, persons):
        """
        Convert persons into a DataFrame for the table view.
        """
        if not persons:
            return pd.DataFrame(columns=["First Name", "Last Name", "Email", "Phone", "Address"])
        return pd.DataFrame([
            {
                "First Name": person.name_first,
                "Last Name": person.name_last,
                "Email": person.email or "N/A",
                "Phone": person.phone_number or "N/A",
                "Address": (
                    f"{person.address.street}, {person.address.postal_code}, {person.address.municipality}"
                    if person.address else "N/A"
                )
            }
            for person in persons
        ])

    def setup_timeline_order_line(self, input, output):

        @reactive.calc
        async def filtered_data():

            all_phases = []
            phases = await self.db_service.get_phases_by_project(input.project_select())
            count_phases = len(phases)
            for ph in phases:
                data_phases = [
                    {
                        "phase_id": order_line.phase_id,
                        "orderline_id": order_line.orderline_id,
                        "date_ordered": order_line.date_ordered,
                        "date_received": order_line.date_received,
                        "date_issued": order_line.date_issued,
                        "date_delivered": order_line.date_delivered,
                        "date_installed": order_line.date_installed,
                        "date_accepted": order_line.date_accepted,
                        "date_invoiced": order_line.date_invoiced,
                        "date_paid": order_line.date_paid,
                        "date_closed": order_line.date_closed
                    }
                    for order_line in ph.order_lines]

                # Validate fetched data
                if not data_phases:
                    self.__logger.info("No data returned from database.")
                    return pd.DataFrame()

                # Create DataFrame
                df = pd.DataFrame(data_phases)

                # Rename or adjust to match expected column names
                expected_columns = [
                    "phase_id", "orderline_id", "date_ordered", "date_received", "date_issued",
                    "date_delivered", "date_installed", "date_accepted", "date_invoiced",
                    "date_paid", "date_closed"
                ]
                missing_columns = [col for col in expected_columns if col not in df.columns]
                if missing_columns:
                    self.__logger.info(f"Missing columns in DataFrame: {missing_columns}")
                    return pd.DataFrame()

                # Transform to long format
                df_long = df.melt(
                    id_vars=["orderline_id"],
                    value_vars=expected_columns[1:],  # Exclude id_vars
                    var_name="Phase",
                    value_name="Date"
                )

                # Clean date column
                df_long["Date"] = pd.to_datetime(df_long["Date"], errors='coerce')
                df_long = df_long.dropna(subset=["Date"])
                start_date = datetime(year=2023, month=1, day=1)
                end_date = datetime.now()
                mask = (df_long["Date"] >= pd.to_datetime(start_date)) & (df_long["Date"] <= pd.to_datetime(end_date))
                all_phases.append(df_long[mask])
            return all_phases

        @output
        @render.ui
        async def timeline_plot():
            # Get the processed data
            df_filtered = await filtered_data()

            # Placeholder for multiple plots
            figs = []

            if all(df.empty for df in df_filtered):
                # No data message for all empty plots
                import plotly.graph_objects as go
                for d in df_filtered:
                    fig = go.Figure()
                    fig.add_annotation(
                        text=f"No data in selected date range (Plot {d})",
                        xref="paper", yref="paper", showarrow=False,
                        font=dict(size=20),
                    )
                    figs.append(fig)
            else:
                # Create 3 variations of the scatter plot
                for i, d in enumerate(df_filtered, start=1):
                    fig = px.scatter(
                        d,
                        x="Date",
                        y="orderline_id",
                        color="Phase",
                        symbol="Phase",
                        title=f"Orderline Phase Timeline (Plot {i})",
                        category_orders={"orderline_id": d["orderline_id"].unique()},
                    )
                    fig.update_yaxes(autorange="reversed")
                    fig.update_traces(marker=dict(size=12))
                    fig.update_layout(
                        plot_bgcolor="#a89ca3",

                        paper_bgcolor="#a89ca3",
                        title={
                            "text": f"Orderline Phase Timeline (Plot {i})",
                            "font": {"size": 24, "family": "Arial", "weight": "bold"},
                            "x": 0.5,
                            "xanchor": "center",
                        },
                    )
                    figs.append(fig)

            # Create HTML for all plots
            from plotly.io import to_html
            fig_htmls = [f"<div style='margin-bottom: 50px;'>" + to_html(fig, full_html=False) + "</div>'" for fig in
                         figs]

            # Return combined HTML for shiny
            return ui.HTML("".join(fig_htmls))

    def setup_datagrid(self, input,output):
        """
        Set up datagrid for the Data Grid feature.
        """

        @output
        @render.data_frame
        async def data_grid():
            projects = await self.db_service.get_all_projects()
            if not projects:
                return pd.DataFrame(columns=[
                    "ID", "Client", "Calculator", "Salesman", "Project Leader",
                    "Acceptance Date", "Start Date", "End Date"
                ])
            data = [
                {
                    "ID": project.project_id,
                    "Client": (
                        f"{project.client.company.company_name} "
                        if project.client else "N/A"
                    ),
                    "Calculator": (
                        f"{project.calculator.person.name_first} {project.calculator.person.name_last}"
                        if project.calculator else "N/A"
                    ),
                    "Salesman": (
                        f"{project.salesman.person.name_first} {project.salesman.person.name_first}"
                        if project.salesman else "N/A"
                    ),
                    "Project Leader": (
                        f"{project.project_leader.person.name_first} {project.project_leader.person.name_last}"
                        if project.project_leader else "N/A"
                    ),
                    "Acceptance Date": project.date_acceptance or "N/A",
                    "Start Date": project.date_start or "N/A",
                    "End Date": project.date_end or "N/A",
                }
                for project in projects
            ]
            return pd.DataFrame(data)

        @output
        @render.data_frame
        async def personnel_grid():
            # This is the initial DataFrame for the grid. Make it available globally.
            global personnel_data_store

            person_type = input.select_person_type()

            try:
                # Fetch persons by type using your DBService
                persons = await self.db_service.get_all_persons_type(PersonType(person_type))
            except ValueError:
                persons = None

            if not persons:
                df = pd.DataFrame(columns=["ID", "First Name", "Last Name", "Email", "Phone","Photo"])
                personnel_data_store = df  # Store empty DataFrame
                return df

            # Prepare data
            data = [
                {
                    "ID": person.person.person_id,
                    "First Name": person.person.name_first,
                    "Last Name": person.person.name_last,
                    "Email": person.person.email or "N/A",
                    "Phone": person.person.phone_number or "N/A",
                    "Photo" : person.person.photo_url  or "N/A"
                }
                for person in persons
            ]

            # Generate and store DataFrame globally
            df = pd.DataFrame(data)

            personnel_data_store = df  # Store it globally for access in other parts

            # Render DataGrid
            return render.DataGrid(
                df,
                filters=True,
                selection_mode="row",

                styles=[
                    {
                        "headerStyle": {"font-weight": "bold", "color": "black"},
                    },
                    {
                        "class": "text-center",
                    },
                    {
                        "cols": [0],
                        "style": {"font-weight": "bold", "background-color": "#ffdbaf"},
            },
        ],
    )

shiny_app = ShinyApplication()
app = App(shiny_app.app_ui, shiny_app.app_server)