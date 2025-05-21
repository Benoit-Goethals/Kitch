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
from src.utils.Configuration import Configuration


def _define_table_styles():
    """
    Defines and returns a block of CSS styles for various UI components, including
    table styling, navigation panel content alignment, centered content layout, and
    sidebar customization.

    :return: A string containing CSS styles to be applied for UI elements.
    :rtype: str
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
    """
    This class represents the main application that integrates UI and server functionalities along with
    database interaction and additional utility tools for a Shiny-based application. It is responsible
    for building the user interface, configuring server logic, and managing asynchronous data and
    user interactions via its components.

    :ivar db_service: Service instance for interacting with the application's database.
    :type db_service: DBService
    :ivar table_styles: Pre-defined styles for HTML tables used in the UI.
    :type table_styles: str
    :ivar app_ui: Represents the user interface for the application.
    :type app_ui: Shiny UI object
    :ivar app_server: Represents the server logic for the Shiny application.
    :type app_server: Callable
    :ivar map_generator: Utility to generate maps, using `MapGenerator`.
    :type map_generator: MapGenerator
    :ivar __logger: Logger instance for logging application events.
    :type __logger: logging.Logger
    """
    def __init__(self):
        Configuration.configuration_files_check()
        self.db_service = DBService()
        self.table_styles = _define_table_styles()
        self.app_ui = self._build_ui()
        self.app_server = self._build_server()
        self.map_generator = MapGenerator(self.db_service)
        self.__logger = logging.getLogger(__name__)




    @staticmethod
    def make_path(save_path)->Path:
        """
        Generates a platform-specific file path for saving photos, based on the
        save path provided. For Windows, it creates the path under
        'C:\\ProgramData\\Kitch\\photos', while on Linux, it appends the save path to a
        directory located in the user's home folder.

        :param save_path: The relative file path or name to append to the platform-
            specific root directory for photos.
        :type save_path: str
        :return: A complete platform-specific file path as a Path object, pointing to
            the location for saving the specified resource.
        :rtype: Path
        """
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
        Builds and returns the UI structure for the application. This method constructs
        a fluid page layout using various modules from the `ui` package. The layout
        consists of a styled navigation bar, a sidebar for menu selection, and the main
        content area dynamically updated based on user interaction. The sidebar also
        includes an "Exit App" button for convenient application closure.

        :return: An assembled UI layout object that contains a navigation bar, sidebar,
            and main content display area.
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
                    ui.input_action_button("exit_button", "Exit App"),

                    class_="sidebar",
                    bg=" #a89ca3"),
                ui.output_ui("selected_content"),
            )
        )

    def _build_server(self):
        """
        Builds the server logic for a Shiny application.

        This function defines the server logic, including its effects and outputs,
        for a Shiny application. It handles data interaction, modal management,
        dynamic content rendering, and user interactions through reactive inputs
        and event-driven executions.

        The server includes several functionalities like showing a personnel modal
        with detailed information, displaying maps for companies, adding a person
        modal, and representing project details within specified date ranges. The
        outputs include rendering UI elements, data tables, images, and text content.

        Some parts of the server logic involve external integrations such as database
        fetching and map generation, while others handle reactive user inputs and
        output rendering seamlessly.

        :return: A callable representing the server logic.
        :rtype: Callable
        """
        def server(input, output, session):
            global personnel_data_store  #

            @reactive.Effect
            @reactive.event(input.personnel_grid_selected_rows)
            def show_person_modal():
                """
                This function initializes a server for a reactive Shiny application. The server is responsible
                for handling and rendering the UI based on user interactions, particularly showing a modal
                window with personnel details based on the selected row in a data grid.

                :param input: Reactive input object containing user input and interaction values from the UI.
                :param output: Reactive output object used to define and wire rendering operations for UI elements.
                :param session: Session object managing state and interaction for the current user session.

                :raises KeyError: Raised if expected keys such as 'First Name', 'Last Name', 'Email', or 'Phone'
                    are missing from the data frame indexed by `personnel_data_store`.

                :return: None, this function is intended to set up reactive behavior and define output rendering logic.
                """
                global personnel_data_store
                selected_rows = input.personnel_grid_selected_rows()
                if selected_rows and personnel_data_store is not None:
                    df = personnel_data_store
                    if not df.empty:
                        row_index = selected_rows[0]
                        row_data = df.iloc[row_index]
                        path = ShinyApplication.make_path(row_data["Photo"])
                        if path.exists():
                            @output
                            @render.image
                            def img_output():
                                img: ImgData = {"src": str(path), "width": "300px"}

                                return img

                        content = ui.div(
                            ui.h4(f"{row_data['First Name']} {row_data['Last Name']}"),
                            ui.p(f"Email: {row_data['Email']}"),
                            ui.p(f"Phone: {row_data['Phone']}"),
                            ui.output_image("img_output"),

                        )
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
                """
                Handles the server-side operations, including reactive effects
                to check and handle app exit events triggered through the
                UI.

                This function works within a reactive environment to monitor
                user input and execute defined reactive effects. It ensures
                the app can gracefully shut down when an exit event is triggered.

                :param input: An object representing reactive input bindings.
                :param output: An object representing reactive output bindings.
                :param session: An object representing the active reactive
                    session information.

                :return: None
                """
                if input.exit_button():
                    self.__logger.info("Exiting the app...")
                    sys.exit(1)

            @reactive.Effect
            async def show_map_companies():
                """
                Asynchronous function to interact with the server and manage user sessions
                and data updates. It includes reactive effects for managing user interface
                updates and handling asynchronous company-related map data operations.

                Parameters
                ----------
                input : Any
                    Input object that provides interaction states or data provided by the user.
                output : Any
                    Output object used to send responses or updates to the front-end.
                session : Any
                    Session object containing current session details and states.

                :return: None
                """
                if input.show_map_companys():
                    await self.map_generator.mark_points_companies()

            @reactive.Effect
            async def show_map_heatmap_sales_project():
                """
                Handles the server behavior associated with the reactive effect for displaying
                a heatmap of sales projects on a map. This function leverages a reactive
                programming paradigm to dynamically generate and update the map display based
                on user input.

                Parameters
                ----------
                input : Any
                    Represents the input object which provides access to user inputs or
                    events.
                output : Any
                    Represents the output object responsible for handling dynamic UI updates.
                session : Any
                    Represents the session object, holding the state and context for the
                    server-side execution.

                Raises
                ------
                ValueError
                    If invalid inputs are provided or required keys are missing.

                :return: None
                """
                if input.show_map_heatmap_sales_project():
                    await self.map_generator.euros_phases()



            @reactive.Effect
            async def show_projects_between_dates_for_person():
                """
                Handles server-side logic utilizing user input for generating and displaying
                project phases for a specific person within a defined date range. The function
                reacts to specific user-triggered events and performs asynchronous operations
                when required.

                :param input: Reactivity-enabled input interface allowing retrieval of user
                              selections and input values such as person and date range.
                :param output: Reactivity-enabled output interface enabling dynamic response
                               updates based on input changes.
                :param session: Holds client-specific session information enabling isolated
                                handling of user requests.

                :return: None
                """
                if input.show_projects_between_dates_for_person():
                    person_id = input.person_select()
                    date_range = input.date_range()
                    if not person_id or not date_range:
                        return
                    start_date, end_date = date_range
                    await self.map_generator.project_phases_between_date_for_person(person_id, start_date, end_date)

            @reactive.Effect
            def add_person_modal():
                """
                This function manages server-side logic for handling input, output, and session in a Shiny application.
                It includes the creation and management of a modal dialog for adding a new person. Users can interact
                with various input fields in the modal to provide personal and address details.

                :param input: Reactive inputs that trigger server-side logic when their values change.
                :param output: Server-side objects to display reactive output elements in the UI.
                :param session: Session-specific information, such as input/output bindings for a single user.

                :raises TypeError: If an invalid type is used for any parameter based on expected usage.
                :raises ValueError: If values provided to the modal do not meet validation criteria.

                :returns: None. The function acts as a reactive server logic handler.
                """
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
                                    style="grid-column: 1 / -1; text-align: center;"                                ),

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
                """
                Handles server logic for processing input and rendering output.

                The server function is responsible for managing the communication between
                input components and output rendering. It listens for changes in inputs,
                processes them as necessary, and updates the output accordingly. In this
                function, an asynchronous task is defined to render the UI based on user
                interactions with a sidebar menu.

                :param input: Input object that provides user interaction data.
                :type input: object
                :param output: Output object to expose rendering capabilities.
                :type output: object
                :param session: Session object providing information about the current user
                    session.
                :type session: object
                :return: None
                :rtype: None
                """
                selected = input.sidebar_menu()
                return await self.handle_sidebar_selection(selected, input)

            @output
            @render.text
            def exit_message():
                """
                Defines the server logic for handling user interactions within a
                shiny application. Provides a mechanism to terminate the
                application gracefully by rendering an informational exit message.

                :param input: Represents input values provided to the server logic.
                    These inputs are reactive and are updated dynamically based
                    on user interaction.
                :type input: reactive

                :param output: Manages the output rendering system of the
                    application. This is used to display results or messages back
                    to the user. The output objects are updated reactively when
                    dependent input changes.
                :type output: reactive

                :param session: Represents the active session within the
                    application, facilitating communication between the client
                    and server. Allows for session-specific configurations or
                    features.
                :type session: reactive.Session

                :return: No explicit return value. Implements UI rendering and
                    response generation functionality through embedded logic.
                """
                return "Click 'Exit App' to terminate the application."

            @output
            @render.ui
            async def selected_content():
                """
                Handles server-side operations related to input, output, and session in a web or
                dashboard application framework. This function defines and integrates reactive
                output elements based on input interactions and session context.

                :param input: Dynamic reactive inputs handled by the server function.
                :type input: Any
                :param output: Reactive outputs that are rendered and updated based on inputs.
                :type output: Any
                :param session: Session-specific data, context, and state for the server function.
                :type session: Any

                :return: None
                """
                selected = input.sidebar_menu()
                return await self.handle_sidebar_selection(selected, input)

            @output
            @render.data_frame
            async def personnel_grid():
                """
                Handles server-side functionality for rendering a personnel grid in a web framework. The function
                binds reactive input, output, and session aspects, enabling a dynamic table that displays a list of
                personnel based on the user-selected type. It interacts with a database to fetch relevant personnel
                information and formats it into a DataFrame, which can be displayed as a styled data grid.

                :param input: Reactive input for the server function. Expected to provide access to user selections.
                :param output: Reactive output for the server function. Used to render outputs dynamically.
                :param session: Reactive session context. Provides session-specific behavioral control.
                :type input: Input (or similar reactive module)
                :type output: Output (or similar reactive module)
                :type session: Session (or similar reactive module)

                :raises ValueError: If the person_type provided by the user is invalid.
                :raises AnyException: Reraised exception if issues occur in data fetching or formatting.

                :return: None. The function defines reactive output components within the server context.
                """
                global personnel_data_store
                person_type = input.select_person_type()
                try:
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
                        "ID": p.person.person_id,
                        "First Name": p.person.name_first,
                        "Last Name": p.person.name_last,
                        "Email": p.person.email or "N/A",
                        "Phone": p.person.phone_number or "N/A",
                    }
                    for p in persons
                ]
                df = pd.DataFrame(data)
                personnel_data_store = df

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

                ui.notification_show(
                    f"An error occurred: {str(e)}",
                    type="error",
                    duration=5  # Show the notification for 5 seconds
                )

        return server

    async def handle_sidebar_selection(self, selected, input):
        """
        Handles user selection from the sidebar and invokes the appropriate rendering
        function based on the selected option.

        The method maps user-selected sidebar options to their respective rendering
        functions, including views for sales, project plots, company data, personnel
        tables, Gantt charts, and more. If the selected option corresponds to a valid
        view, it renders the appropriate UI. If no valid selection matches, it returns
        a message prompting the user to select a valid tab.

        :param selected: The user selection from the sidebar.
        :type selected: SidebarChoices
        :param input: The input or additional data required for processing.
        :type input: Any
        :return: The output from the invoked handler or a fallback prompt message.
        :rtype: Any
        """
        sidebar_handlers = {
            SidebarChoices.HOME.value: self._render_sales_view,
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

    async def _render_sales_view(self):
        """
        Renders the sales view for displaying sales percentages of projects for a specific year.
        This method initializes the UI elements with the required structure and styling and
        calls supplemental methods to populate additional interface components. The view includes
        a dropdown for year selection and a plot for visualizing sales percentages.

        :return: A tuple containing an H2 header element for the title of the sales view and
                 a div element containing the UI layout with a dropdown and plot components.
        :rtype: tuple
        """
        self.fill_years_sales()
        return ui.h2("Sales percentages of projects in a year"), ui.tags.div(
            ui.tags.div(
                ui.input_select(
                    "year_select", "Select a year:",
                    choices=[], multiple=False, width="500px"
                )
            ),
            ui.output_plot("sales_plot", width="600px", height="600px"),
            style=FLEX_COLUMN_STYLE,
            class_="nav-panel-content"
        )


    async def _render_project_plot_view(self):
        """
        Fetches and updates project choices asynchronously, then renders the project plot UI.

        This method handles the process of asynchronously fetching project choices
        required for rendering the project plot user interface (UI). After the project
        choices are updated, it proceeds to render the UI.

        :return: The rendered project plot UI.
        :rtype: Any
        """
        await self.fetch_and_update_project_choices()
        return self._render_project_plot_ui()


    async def _render_gantt_view(self):
        """
        Asynchronously renders the Gantt view for the current instance.

        This method fetches and updates the project choices and subsequently
        renders the Gantt chart user interface.

        :return: The rendered Gantt chart UI
        :rtype: Any
        """
        await self.fetch_and_update_project_choices()
        return self._render_gantt_char_ui()


    def _render_company_view(self):
        """
        Renders the company view interface including a button for displaying companies
        on a map and a UI table listing all companies.

        :return: A tuple containing a UI input action button and a rendered table UI.
        :rtype: tuple
        """
        return ui.input_action_button(
            "show_map_companys",
            "Show companies on the map",width="300px"

        ), self._render_table_ui("List of all Companies", "company_table")

    def _render_projects_grid_view(self):
        """
        Renders the grid view for displaying a list of all projects.

        This function creates a user interface element containing a
        header, a button for displaying the projects on a map, and
        a data grid to display the list of projects in a tabular
        format. The rendered grid view is returned as an HTML
        component.

        :return: The rendered HTML component containing the grid view
                 for all projects.
        :rtype: Any
        """
        return ui.tags.div(
            ui.h2("List of all Projects"),
            ui.input_action_button("show_map_heatmap_sales_project", "Show on the Euro/project map"),
            ui.output_data_frame("data_grid")
        )

    async def _render_timeline_view(self):
        """
        Render the timeline view asynchronously.

        This private coroutine method ensures that project choices are fetched
        and updated prior to rendering the timeline. It acts as a preparatory
        step consolidating the necessary data updates before invoking the
        rendering logic of the timeline.

        :return: The rendered timeline view
        :rtype: Any
        """
        await self.fetch_and_update_project_choices()
        return self._render_timeline()

    async def _render_filters_view(self):
        """
        Fetches and updates person choices and renders the datetime selection UI.

        This method is asynchronous and performs two main actions:
        1. Fetches data and updates the person-related choices available for
           filtering.
        2. Renders the datetime selection UI based on the updated choices.

        :raises SomeSpecificError: Indicates specific issues encountered
                                    during data fetching or UI rendering.
        :return: The rendered datetime selection UI.
        :rtype: SomeSpecificType
        """
        await self.fetch_and_update_person_choices()
        return self._render_datetime_selection_ui()


    async def _render_personnel_view(self):
        """
        Renders the personnel management view asynchronously.

        This method creates and returns a user interface layout for managing personnel data.
        The layout includes a section header, a dropdown to select the type of person, a button
        to add new personnel, and a data frame to display the personnel information. Additionally,
        styling is applied to ensure proper spacing and alignment in the layout.

        :return: A UI element representing the personnel management view
        :rtype: ui.tags.div
        """
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
        Constructs and returns a user interface section for selecting a date range
        and an individual person to filter and display relevant information.

        The UI includes:
        - A heading to indicate the purpose of the section.
        - A dropdown for selecting a person.
        - A date range picker for specifying a time period.
        - An action button to apply the filter.
        - An output area for displaying filter results.

        :return: A constructed UI element representing the datetime selection interface.
        :rtype: ui.tags.div
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
        Fetches all persons from the database and updates the UI dropdown choices with the retrieved data.

        This asynchronous method retrieves a list of person records from the database through
        the DB service and processes them to construct a dictionary, where the keys are person IDs
        and the values are their corresponding full names. The processed dictionary is then used
        to update the UI select element named "person_select" with new choices. Logs any exception
        encountered during this process.

        :raises Exception: If any error occurs while fetching person data or updating the UI.

        :return: None
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
        """
        Renders the Gantt chart user interface component for project turnover.

        This function generates a UI element that includes a title,
        a project selection dropdown, and an output area for displaying
        the Gantt chart. The project selection dropdown allows the user
        to choose from available project options, and the Gantt chart
        visualizes the turnover in various project phases.

        :return: A UI component containing a title, project selection dropdown, and a Gantt chart output area.
        :rtype: ui.tags.div
        """
        return ui.tags.div(
            ui.h2("Project turnover in the different phases"),
            ui.input_select(
                "project_select", "Select a Project:", choices=[], multiple=False, width="500px"
            ),
            ui.output_ui("gantt_chart", width="600px", height="600px")
        )




    def _render_project_plot_ui(self):
        """
        Renders the UI layout for displaying a project's turnover in different phases. The layout includes a
        header, a dropdown selection menu for choosing a project, and an output plot to visualize the data.
        The design ensures a vertically centered and column-aligned structure for user interaction.

        :rtype: Tag
        :return: A Tag object representing the constructed UI layout for the project plot.
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
        """
        Renders the timeline UI component for a phase order visualization. This includes
        a header, a project selection dropdown, and a timeline plot. The UI elements
        are arranged using a flexbox layout.

        :return: A div containing the timeline UI elements, organized and styled for
                 display within the navigation panel.
        :rtype: ui.tags.div
        """
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
        Renders a UI component consisting of a title header and an output table.

        This method generates a UI structure using the specified title and table
        identifier. The resulting UI component includes a header displaying the title
        and an interactive output table linked to the provided table identifier.

        :param title: The string representing the title that appears above the table.
        :type title: str
        :param table_id: The table's unique identifier used for rendering and
            interaction.
        :type table_id: str
        :return: A rendered UI component containing a header and an output table.
        :rtype: `Tag`
        """
        return ui.tags.div(
            ui.h2(title),
            ui.output_table(table_id)
        )


    def fill_years_sales(self):
        """
        Fills the sales year selection dropdown with a range of years starting from 1990 up to the current year, inclusive.
        The default selected year in the dropdown is set to two years prior to the current year.

        :return: None
        """
        choices_select = [year for year in range(1990, datetime.now().year + 1)]
        ui.update_select("year_select", choices=choices_select, selected=str(datetime.now().year - 2))

    async def fetch_and_update_project_choices(self):
        """
        Fetches project data asynchronously, updates the project selection dropdown
        menu in the UI with the available project choices.

        This method retrieves all projects from the database using the provided
        database service. For each project retrieved, it generates a readable display
        label containing the project ID and the client's company name, if available.
        These choices are then used to update a dropdown selection field in the
        user interface. Any exceptions encountered during this process are logged.

        :raises Exception: If an error occurs while fetching projects or updating
            the UI.
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
        Sets up the data fetching mechanism for the instance by defining reactive
        calculations to fetch companies and projects.

        :raises Exception: If there is an error within the reactive computations due
            to issues in fetching data.
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
        async def sales_plot():
            """
            Represents the main Shiny application for configuring and rendering plots.

            This class encapsulates the necessary methods and attributes to render
            plots within a Shiny application. It interacts with input/output handlers
            and external database services to retrieve and visualize data dynamically.

            Attributes
            ----------
            db_service : Any
                A service object responsible for interfacing with the database. Used
                to fetch relevant data required for plotting.

            Methods
            -------
            setup_plots(output, input)
                Configures output render logic using the Shiny application's provided
                `output` and `input` handlers.
            """
            selected_year = input.year_select()
            projects_with_phases = await self.db_service.get_all_projects_phases_year(selected_year)
            return self._generate_sales_plot(projects_with_phases)


        @output
        @render.ui
        async def gantt_chart():
            """
            A class representing a Shiny application. This class is responsible for
            setting up plot outputs and managing input-output bindings for visualization
            in a web-based interface. It interfaces with external database services to
            fetch necessary data and render interactive charts.

            Attributes
            ----------
            db_service : Any
                The database service used to retrieve data.

            Methods
            -------
            setup_plots(output, input)
                Configures the plots and binds them to the UI, rendering an interactive
                Gantt chart based on the provided data.
            """
            temp=[]
            data=await self.db_service.get_phases_by_project(input.project_select())
            if data is not None:
                for d in data:
                    temp.append(dict(Resource=f"{d.project.client.company.company_name}", Start=d.project.date_start,
                                     Finish=d.project.date_end, Task=f"CLient {d.project}"))
                    temp.append( dict(Resource=f"{d.project.client.company.company_name}", Start=d.date_start_client, Finish=d.date_end_client, Task=f"CLient {d.name}"))
                    temp.append(dict(Resource=f"{d.project.client.company.company_name}", Start=d.date_start_planned,
                                     Finish=d.date_end_planned, Task=f"Planning {d.name}"))
            df = pd.DataFrame(data=temp)
            fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource")
            fig.update_xaxes(tickangle=-45, tickformat="%Y-%m-%d")
            fig.update_yaxes(autorange="reversed")

            fig.update_layout(
                plot_bgcolor='white',
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(211,211,211,0.3)',
                    griddash='dash',
                ),
            )

            for i in range(len(df)):
                if i % 2:
                    fig.add_shape(
                        type="rect",
                        x0=df['Start'].min(),
                        x1=df['Finish'].max(),
                        y0=i - 0.5,
                        y1=i + 0.5,
                        fillcolor="rgba(242,242,242,0.3)",
                        line_width=0,
                        layer="below"
                    )


            now = datetime.now().strftime("%Y-%m-%d")
            fig.add_shape(
                type="line",
                x0=now, x1=now,
                y0=0, y1=1,
                xref="x",
                yref="paper",
                line=dict(color="Red", width=2, dash="dash"),
                name="Now"
            )

            # Update layout to show annotation
            fig.add_annotation(
                x=now, y=1,
                text="Now",
                showarrow=True,
                arrowhead=2,
                ax=0, ay=-40,
                xref="x", yref="paper"
            )
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

    def _generate_sales_plot(self, projects_with_phases):
        """
        Generates a pie chart that visualizes the total sales price for projects.

        This function calculates the total sales price for each project based on the
        sales price of their respective phases order lines. It then creates a pie chart
        to visualize the total sales for all projects.

        :param projects_with_phases: List of projects, where each project contains its
            associated phases and each phase contains order lines with a sales price.
        :type projects_with_phases: list
        :return: A matplotlib pie chart figure that visualizes the total sales price
            distribution across projects, or None if no projects are provided.
        :rtype: matplotlib.figure.Figure or None
        """
        if not projects_with_phases:
            return None
        total_projects = []
        for project in projects_with_phases:
            total_sales_price = sum([
                ph.sales_price for phase in project.phases
                for ph in phase.order_lines if ph.sales_price is not None
            ])
            total_projects.append((project.client.company.company_name, total_sales_price))

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
            """
            Represents an application for rendering and managing various UI components.
            Primarily responsible for configuring data tables to be displayed using the
            provided output rendering framework.

            :Attributes:
                None
            """
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
        Represents a module for handling and managing operations related to persons, including file
        uploads, image verification, database interactions, and rendering a table of person data.

        This module combines reactive calculations and effects to provide a seamless user experience
        for person-related workflows, utilizing file processing tools, an integrated database service,
        and UI notifications to maintain and display data efficiently.

        :param input: Input object providing reactive inputs from the UI, such as buttons or uploaded files.
        :type input: reactive.Input
        :param output: Output object to manage and populate reactive UI outputs like rendered tables.
        :type output: reactive.Output
        """

        @reactive.calc
        async def upload_and_verify_file():
            """
            Represents an application to handle user interactions, including file uploads
            and validation for person-specific operations. Provides methods to
            process, verify, and save uploaded files.

            :ivar __logger: Logger instance for logging messages and errors.
            """
            file: list[FileInfo] | None = input.file_upload()
            if not file:
                return None
            try:
                img = _verify_image_file(file[0]["datapath"])
                if img is None:
                    raise ValueError("Uploaded file is not a valid image.")
                save_path = input.file_upload()[0]["name"]
                path = ShinyApplication.make_path(save_path)
                img.save(str(path))

                return True
            except Exception as e:
                self.__logger.error(f"Error uploading file: {e}")
                return False



        def _verify_image_file(file: str) -> Optional[Image.Image]:
            """
            Represents a Shiny application that facilitates setting up and managing
            person-related operations, including image file verification.

            This class manages the lifecycle and execution of various processes
            related to the application's operations. It includes methods to validate
            and process file inputs for specific use cases. Logger functionality is
            integrated to ensure errors during operations are logged.
            """
            try:
                with Image.open(file) as img:
                    img.verify()
                with Image.open(file) as img:
                    return img.copy()
            except Exception as e:
                 self.__logger.error(f"Error verifying image file: {e}")
            return None


        @reactive.Effect
        async def add_person_effect():
            """
            Represents the ShinyApplication class responsible for setting up operations
            related to person management in the application.

            ...

            Attributes:
            -----------
            None

            Methods:
            --------
            setup_person_operations(input, output)
                Configures reactive effects to handle person-related operations.
            """
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
            """
            A class representing the Shiny application setup, allowing initialization
            of operations and rendering of a table for displaying person data with
            associated addresses.
            """
            persons = await self.db_service.get_all_persons_with_address()
            return self._generate_persons_table(persons)

    def _build_person_from_inputs(self, input):
        """
        Builds a `Person` object along with the associated `Address` and `PersonType`
        based on the provided input object.

        :param input: A source input interface from which the required data is
                      fetched to construct `Person`, `Address`, and determine
                      `PersonType`.
        :type input: InputInterface

        :return: A tuple containing:
                 - `person` (Person): The constructed instance of `Person`.
                 - `address` (Address): The corresponding address instance created
                                        for the `Person`.
                 - `person_type` (PersonType): The type of the person as
                                               determined from input.
        :rtype: tuple[Person, Address, PersonType]
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
        Generates a DataFrame representation of a list of person objects. Each person in the
        list is converted into a table row containing their first name, last name, email,
        phone number, and address. If no persons are provided, an empty DataFrame with the
        appropriate column headers is returned.

        :param persons: List of person objects to be transformed into table rows.
        :type persons: list
        :return: A DataFrame with columns 'First Name', 'Last Name', 'Email', 'Phone', and
            'Address' representing the details of each person. If no persons are provided,
            an empty DataFrame with column headers is returned.
        :rtype: pandas.DataFrame
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
        """
        Sets up the logic for fetching, filtering, and rendering orderline phase data for visualization in a
        Shiny application. The method constructs a timeline of phases associated with orderlines for a specific
        project, filters the results based on date constraints, and dynamically generates interactive scatter plots.

        :param input: Provides the project selection input required for data fetching.
        :param output: Used for displaying the generated visualizations as part of a Shiny application.
        :return: A timeline of filtered and formatted orderline phase data for visualization.
        """
        @reactive.calc
        async def filtered_data():
            """
            A class representing a Shiny application to manage and process
            timeline order lines.

            This class is designed to set up and manage filtered data for
            timeline order lines using data retrieved from a database.
            It performs calculations on the data, ensuring validity and
            filtering it by specific date ranges.

            :ivar db_service: An external database service used for querying data.
            :ivar __logger: A logger instance for logging informative messages or issues.
            """
            all_phases = []
            phases = await self.db_service.get_phases_by_project(input.project_select())
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

                if not data_phases:
                    self.__logger.info("No data returned from database.")
                    return pd.DataFrame()

                df = pd.DataFrame(data_phases)
                expected_columns = [
                    "phase_id", "orderline_id", "date_ordered", "date_received", "date_issued",
                    "date_delivered", "date_installed", "date_accepted", "date_invoiced",
                    "date_paid", "date_closed"
                ]
                missing_columns = [col for col in expected_columns if col not in df.columns]
                if missing_columns:
                    self.__logger.info(f"Missing columns in DataFrame: {missing_columns}")
                    return pd.DataFrame()

                df_long = df.melt(
                    id_vars=["orderline_id"],
                    value_vars=expected_columns[1:],  # Exclude id_vars
                    var_name="Phase",
                    value_name="Date"
                )
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
            """
            Represents the Shiny application logic and functionality. This class is designed
            to manage and render interactive plots for an orderline phase timeline, based on
            asynchronous data fetching and dynamic plot creation.

            Methods:
                setup_timeline_order_line: Sets up the logic for rendering the orderline phase
                timeline, including filtering data, creating interactive scatter plots, and
                generating the HTML output for Shiny.

            Attributes:
                None
            """
            df_filtered = await filtered_data()
            figs = []
            if all(df.empty for df in df_filtered):
                import plotly.graph_objects as go
                for d in df_filtered:
                    fig = go.Figure()
                    fig.add_annotation(
                        text=f"No data in selected date",
                        xref="paper", yref="paper", showarrow=False,
                        font=dict(size=20),
                    )
                    figs.append(fig)
            else:
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
            fig_htmls = ["<div style='margin-bottom: 50px;'>" + to_html(fig, full_html=False) + "</div>'" for fig in
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
            """
            A class responsible for setting up and managing the data grid functionality
            within the Shiny application. The data grid retrieves data from the database
            and presents it in a structured tabular format.

            Attributes:
                db_service: A service instance used to fetch project data from the database.
            """
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
            """
            Handles the creation and setup of a data grid interface using personnel data. Manages
            the retrieval, preparation, and rendering of a personnel data set into a data grid
            component for user interaction. It integrates with a database service to fetch person
            records based on the selected type, processes these records into a structured
            data frame, and provides both styling and filtering capabilities for the resulting grid.

            Attributes
            ----------
            db_service : object
                A database service object used to retrieve and manage personnel data from an
                external data source.

            Methods
            -------
            setup_datagrid(input, output)
                Configures the personnel data grid with data retrieval, formatting, and rendering.

            Raises
            ------
            ValueError
                When the selected person type input is invalid or leads to an error in data retrieval.
            """
            global personnel_data_store
            person_type = input.select_person_type()
            try:
                persons = await self.db_service.get_all_persons_type(PersonType(person_type))
            except ValueError:
                persons = None
            if not persons:
                df = pd.DataFrame(columns=["ID", "First Name", "Last Name", "Email", "Phone","Photo"])
                personnel_data_store = df
                return df

            # Prepare data
            data = [
                {
                    "ID": p.person.person_id,
                    "First Name": p.person.name_first,
                    "Last Name": p.person.name_last,
                    "Email": p.person.email or "N/A",
                    "Phone": p.person.phone_number or "N/A",
                    "Photo" : p.person.photo_url  or "N/A"
                }
                for p in persons
            ]
            df = pd.DataFrame(data)
            personnel_data_store = df
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