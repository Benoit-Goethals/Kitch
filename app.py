from shiny import App, ui, reactive, render
from ipyleaflet import Map, Marker, Icon
from ipywidgets import HTML
from shinywidgets import render_widget
import pandas as pd
import matplotlib.pyplot as plt
from src.database_layer.db_service import DBService
from src.domain.DatabaseModelClasses import Address, Person
import seaborn as sns

db_service = DBService()
# CSS styling for the table
table_styles = """
<style>
    table {
        border-collapse: collapse; /* Removes extra spacing between cell borders */
        width: 100%; /* Makes table full width */
    }
    th, td {
        border: 1px solid black; /* Adds borders to cells */
        text-align: left; /* Aligns text inside cells to the left */
        padding: 8px; /* Adds padding inside cells for readability */
    }
    th {
        background-color: #4CAF50; /* Adds a green background to headers */
        color: black; /* Changes the header text color to white */
        font-weight: bold; /* Makes the header text bold */
        text-transform: uppercase; /* Changes header text to uppercase */
    }
    .nav-panel-content {
                text-align: center;
            }

    .center-content {
    display: flex;
    justify-content: center; /* Horizontally centered */
    align-items: center;    /* Vertically centered */
    height: 100vh;          /* Full browser height */
  }


</style>
"""

# App UI
app_ui = ui.page_fluid(
    ui.HTML(table_styles),  # Insert the CSS styling for the table
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("sidebar_menu", "Select a Tab:",
                            choices=[
                                "Home", "Project plot", "Company Table",
                                "Project Table", "Pivot Table", "Company Map",
                                "Persons Table", "Persons add", "Data Grid"
                            ],
                            selected="Home", multiple=False),
            style="width: 250px; height: 100vh; overflow-y: auto;"  # Sidebar styling
        ),

        ui.output_ui("selected_content")  # Dynamically load content based on selection

    )
)


# Server Logic for Sidebar
def server(input, output, session):
    @output
    @render.ui
    async def selected_content():
        """Dynamically render content based on sidebar menu selection."""
        selected = input.sidebar_menu()

        if selected == "Home":
            return ui.tags.div(
                ui.output_plot("home", width="800px", height="800px"),
                class_="center-content"
            )
        elif selected == "Project plot":
            await fetch_and_update_project_choices()

            return ui.tags.div(
                ui.h2("Project plot"),
                ui.input_select(
                    "project_select",
                    "Select a Project:",
                    choices=[],

                    multiple=False,
                    width="500px"
                ),

                ui.output_plot("project_plot", width="600px", height="600px"),
                style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%;",
                class_="nav-panel-content"
            )
        elif selected == "Company Table":
            return ui.tags.div(
                ui.h2("Company Table"),
                ui.output_table("company_table")
            )
        elif selected == "Project Table":
            return ui.tags.div(
                ui.h2("Project Table"),
                ui.output_table("project_table")
            )
        elif selected == "Pivot Table":
            return ui.tags.div(
                ui.h2("Pivot Table: Assignments and Sub-Assignments"),
                ui.output_table("pivot_table")
            )
        elif selected == "Company Map":
            return ui.tags.div(
                ui.h2("Company Locations on Map"),
                ui.output_ui("map_ui")
            )
        elif selected == "Persons Table":
            return ui.tags.div(
                ui.h2("Persons Table"),
                ui.output_table("persons_table")
            )
        elif selected == "Persons add":
            return ui.tags.div(
                ui.tags.div(
                    [
                        ui.output_table("add_person_effect", style="grid-column: 1 / -1;"),
                        ui.h3("Add New Person", style="grid-column: 1 / -1; text-align: center;"),
                        ui.input_text("input_first_name", label="First Name", placeholder="Enter First Name"),
                        ui.input_text("input_last_name", label="Last Name", placeholder="Enter Last Name"),
                        ui.input_text("input_email", label="Email", placeholder="Enter Email Address"),
                        ui.input_text("input_phone", label="Phone Number", placeholder="Enter Phone Number"),
                        ui.h3("Address Details", style="grid-column: 1 / -1; text-align: left;"),
                        ui.input_text("input_street", label="Street", placeholder="Enter Street"),
                        ui.input_text("input_house_number", label="House Number", placeholder="Enter House Number"),
                        ui.input_text("input_postal_code", label="Postal Code", placeholder="Enter Postal Code"),
                        ui.input_text("input_municipality", label="Municipality", placeholder="Enter Municipality"),
                        ui.input_text("input_country", label="Country", placeholder="Enter Country (default: BE)"),
                        ui.tags.div(
                            ui.input_action_button("add_person_btn", "Add Person"),
                            style="grid-column: 1 / -1; text-align: center;"
                        ),
                    ],
                    style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; align-items: start; padding: 10px;"
                ),
                style="display: flex; justify-content: center; padding: 10px;"
            )
        elif selected == "Data Grid":
            return ui.tags.div(
                ui.output_data_frame("data_grid"),
                class_="center-content"
            )
        else:
            return ui.tags.p("Please select a valid tab from the sidebar.")

    async def fetch_and_update_project_choices():
        """Fetch projects and update the project_select dropdown."""
        try:
            projects = await db_service.get_all_projects()
            if projects:
                choices_select = {
                    project.project_id: (
                        f"Project : {project.project_id} Name : {project.client.name_first} {project.client.name_last}"
                        if project.client else "Unknown Client"
                    )
                    for project in projects
                }
                print(f"------------->Choices updated: {choices_select}")  # Debug output
                ui.update_select("project_select", choices=choices_select)
            else:
                print("No projects found!")  # Debug output
        except Exception as e:
            print(f"Error fetching projects: {e}")

    # The rest of the server logic remains unchanged
    @reactive.Calc
    def fetch_companies():
        """Fetch all companies asynchronously from the real database using db_service."""
        # Call the read_all_companies method
        return db_service.get_all_companies()

    @reactive.Calc
    async def fetch_projects():
        return await db_service.get_all_projects()

    @reactive.Calc
    async def fetch_projects_with_phases():
        return await db_service.get_all_projects_phases()

    # Add this fetch function to the server logic
    @reactive.Calc
    def fetch_persons():
        """Fetch all persons asynchronously from the database."""
        return db_service.get_all_persons()

    @reactive.Calc
    def fetch_persons_address():
        """Fetch all persons asynchronously from the database."""
        return db_service.get_all_persons_with_address()

    @reactive.Effect()
    async def update_project_choices():
        await fetch_and_update_project_choices()

    # Render plot when a project is selected
    @output
    @render.plot
    async def project_plot():

        print(f"--->project_plot {input.project_select()}")
        selected_project = input.project_select().split()[0]

        if not selected_project:
            print("No project selected!")  # Debug output
            return None

        # Fetch phases and their orderlines for the selected project
        phases = await db_service.get_phases_by_project(selected_project)  # Replace with DB query

        if not phases:
            print("No phases found!")  # Debug output
            return None

        # Process data: Sum up order line sales_price by phase
        total_order_lines = []
        for phase in phases:
            total_order_lines.append((
                phase.name,
                sum([orderline.sales_price for orderline in phase.orderlines if orderline.sales_price is not None])
            ))

        # Convert to DataFrame for plotting
        df = pd.DataFrame(total_order_lines, columns=["Phase Name", "Total Sales Price"])

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(df["Phase Name"], df["Total Sales Price"])
        ax.set_title(f"Total Sales Price by Phase for Project: {selected_project}")
        ax.set_xlabel("Phase Name")
        ax.set_ylabel("Total Sales Price")

        return fig  # Return plot

    @output
    @render.plot
    async def home():
        try:

            data = await fetch_projects_with_phases()
            if not data:
                raise ValueError("No projects found.")

            total_projects = []

            for project in data:
                total_sales_price = sum([
                    ph.sales_price for phase in project.phases
                    for ph in phase.orderlines if ph.sales_price is not None
                ])
                total_projects.append((project.project_id, total_sales_price))

            # Convert to DataFrame
            df = pd.DataFrame(total_projects, columns=["Project Name", "Total Sales Price"])

            # Use Plotly to generate the pie chart

            fig, ax = plt.subplots()

            ax.pie(df["Total Sales Price"], labels=df["Project Name"], startangle=90, autopct='%1.1f%%',
                   textprops={'fontsize': 10},
                   wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
                   pctdistance=1.2,

                   radius=10,
                   counterclock=False,

                   )
            ax.axis('equal')

            ax.set_title('Sales Price Projects', fontsize=15, fontweight='bold', pad=50)
            ax.set_ylabel('Total Sales Price', fontsize=15, fontweight='bold', labelpad=50)

            return fig
        except Exception as e:
            print(f"Error generating chart: {e}")
            return None

    @render.plot(alt="A matplotlib histogram showing sales price by phase.")
    async def home_backup():

        # Fetch data asynchronously
        data = await db_service.get_all_phases()

        if not data:
            print("Data is empty!")  # Debug output
            return None  # Return nothing if there is no data

        # Process data into Total Order Lines
        total_order_lines = []
        for phase in data:
            total_order_lines.append((
                str(phase.project_id) + phase.name,
                sum([ph.sales_price for ph in phase.orderlines if ph.sales_price is not None])
            ))

        # Convert the processed data into a DataFrame
        import pandas as pd
        df = pd.DataFrame(total_order_lines, columns=["name", "sales_price"])

        # Debug output for processed DataFrame
        print("DataFrame for plotting:", df)

        # Create the plot using matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))  # Define figure size
        ax.bar(df["name"], df["sales_price"])  # Use a bar plot to represent the sales price by phase

        # Add labels and title to the plot
        ax.set_title("Sales Price by Phase")
        ax.set_xlabel("Phase Name")
        ax.set_ylabel("Total Sales Price")

        return fig  # Return the figure object to render

    @render.data_frame
    async def data_grid():
        projects = await fetch_projects()
        if not isinstance(projects, list) or not projects:
            return pd.DataFrame(columns=[
                "ID", "Client", "Calculator", "Salesman", "Project Leader",
                "Acceptance Date", "Start Date", "End Date"
            ])

        data = []
        for project in projects:
            try:
                data.append({
                    "ID": project.project_id,
                    "Client": (
                        f"{project.client.name_first} {project.client.name_last}"
                        if project.client else "N/A"
                    ),
                    "Calculator": (
                        f"{project.calculator.name_first} {project.calculator.name_last}"
                        if project.calculator else "N/A"
                    ),
                    "Salesman": (
                        f"{project.salesman.name_first} {project.salesman.name_last}"
                        if project.salesman else "N/A"
                    ),
                    "Project Leader": (
                        f"{project.project_leader.name_first} {project.project_leader.name_last}"
                        if project.project_leader else "N/A"
                    ),
                    "Acceptance Date": project.date_acceptance or "N/A",
                    "Start Date": project.date_start or "N/A",
                    "End Date": project.date_end or "N/A",
                })
            except AttributeError as e:
                print(f"-------------------Error processing project: {e}")
                continue

        return render.DataGrid(pd.DataFrame(data), filters=True,
                               styles=[
                                   {
                                       "headerStyle": {"font-weight": "bold", "color": "black"},
                                   },

                                   # Center the text of each cell (using Bootstrap utility class)
                                   {
                                       "class": "text-center",
                                   },
                                   # Bold the first column
                                   {
                                       "cols": [0, ],
                                       "style": {"font-weight": "bold", "background-color": "#ffdbaf"},
                                   },

                               ],
                               )

    @output
    @render.table
    async def company_table():
        """Render the fetched companies as a table with a grid layout."""
        # Get the list of companies
        companies = await fetch_companies()
        if not companies:
            # If no companies are found, return an empty DataFrame with headers
            return pd.DataFrame(columns=["Name", "Address", "Contact Person"])

        # Convert the fetched companies to a valid Pandas DataFrame
        data = [
            {
                "Name": company.company_name,
                "Address": company.address.street if company.address else "N/A",
                "Contact Person": (
                    f"{company.contact_person.name_first} {company.contact_person.name_last}"
                    if company.contact_person else "N/A"
                ),

            }
            for company in companies
        ]
        return pd.DataFrame(data)

    @output
    @render.table
    async def project_table():
        assignments = await fetch_projects()
        if not assignments:  # Handle empty data
            return pd.DataFrame(
                columns=["ID", "Client", "Calculator", "Salesman", "Project Leader", "Acceptance Date", "Start Date",
                         "End Date"])

        # Format assignments into DataFrame
        data = [
            {
                "ID": assignment.project_id,
                "Client": (
                    f"{assignment.client.name_first} {assignment.client.name_last}"
                    if assignment.client else "N/A"
                ),
                "Calculator": (
                    f"{assignment.calculator.name_first} {assignment.calculator.name_last}"
                    if assignment.calculator else "N/A"
                ),
                "Salesman": (
                    f"{assignment.salesman.name_first} {assignment.salesman.name_last}"
                    if assignment.salesman else "N/A"
                ),
                "Project Leader": (
                    f"{assignment.project_leader.name_first} {assignment.project_leader.name_last}"
                    if assignment.project_leader else "N/A"
                ),
                "Acceptance Date": assignment.date_acceptance,
                "Start Date": assignment.date_start or "N/A",
                "End Date": assignment.date_end or "N/A",
            }
            for assignment in assignments
        ]
        return pd.DataFrame(data)

    @output
    @render.table
    async def pivot_table():
        """Render a pivot table summarizing assignments and sub-assignments."""
        assignments = await fetch_projects()
        if not assignments:
            return pd.DataFrame(
                columns=["Assignment ID", "Sub-Assignment Count", "Total Sub Names", "Total Sub Descriptions"]
            )

        # Prepare data for pivot
        data = []
        for assignment in assignments:
            if assignment.phases:
                sub_assignment_count = len(assignment.phases)
                data.append({
                    "Assignment ID": assignment.project_id,
                    "Sub-Assignment Count": sub_assignment_count,
                    "Client": (
                        f"{assignment.client.name_first} {assignment.client.name_last}"
                        if assignment.client else "N/A"
                    ),
                    "Calculator": (
                        f"{assignment.calculator.name_first} {assignment.calculator.name_last}"
                        if assignment.calculator else "N/A"
                    ),
                    "Total Sub Names": ", ".join(
                        sub.sub_name for sub in assignment.phases if sub.sub_name),
                    "Total Sub Descriptions": ", ".join(
                        sub.sub_description for sub in assignment.phases if sub.sub_description),
                })
            else:
                data.append({
                    "Assignment ID": assignment.project_id,
                    "Sub-Assignment Count": 0,
                    "Client": (
                        f"{assignment.client.name_first} {assignment.client.name_last}"
                        if assignment.client else "N/A"
                    ),
                    "Calculator": (
                        f"{assignment.calculator.name_first} {assignment.calculator.name_last}"
                        if assignment.calculator else "N/A"
                    ),
                    "Total Sub Names": "None",
                    "Total Sub Descriptions": "None",
                })

        # Create the pivot table DataFrame
        pivot_df = pd.DataFrame(data)
        return pivot_df

    # todo Not working
    @output
    @render_widget
    async def map_ui():
        """Render the interactive map showing company locations."""
        companies = await fetch_companies()
        if not companies:
            return ui.tags.p("No companies found to display on the map.")

        # Initialize the map
        center_coords = (50.8503, 4.3517)  # Default center (e.g., Brussels, Belgium)
        leaflet_map = Map(center=center_coords, zoom=8, scroll_wheel_zoom=True)

        # Add markers for each company
        for company in companies:
            if company.address and company.address.latitude and company.address.longitude:
                # Extract coordinates and other details
                latitude = float(company.address.latitude)
                longitude = float(company.address.longitude)
                if latitude == 0 or longitude == 0:
                    continue
                company_name = company.company_name
                address = (
                    f"{company.address.street}, {company.address.postal_code}, {company.address.municipality}"
                )

                # Create an HTML popup for additional company info
                popup_html = HTML(f"<b>{company_name}</b><br>{address}")

                # Create a marker for this company
                marker = Marker(
                    location=(latitude, longitude),
                    draggable=False,
                    icon=Icon(icon="briefcase", marker_color="green"),  # Customize marker icon
                )
                marker.popup = popup_html

                # Add marker to the map
                leaflet_map.add(marker)

        # Return the map as a widget
        return leaflet_map

    # Add this updated output renderer for the persons table
    @output
    @render.table
    async def persons_table():
        """Render person data as a table, including address."""
        persons = await fetch_persons_address()
        if not persons:  # If no persons exist
            return pd.DataFrame(columns=["First Name", "Last Name", "Email", "Phone Number", "Address"])

        # Format persons into a DataFrame
        data = [
            {
                "First Name": person.name_first,
                "Last Name": person.name_last,
                "Email": person.email or "N/A",
                "Phone Number": person.phone_number or "N/A",
                "Address": (
                    f"{person.address.street}, {person.address.postal_code}, {person.address.municipality}"
                    if person.address
                    else "N/A"
                ),
            }
            for person in persons
        ]
        return pd.DataFrame(data)

    # Add this to the server method to handle "Add Person" functionality
    @reactive.Effect
    async def add_person_effect():
        """Handle the button click to add a new person."""
        if input.add_person_btn():
            # Fetch data from form input fields
            first_name = input.input_first_name()
            last_name = input.input_last_name()
            email = input.input_email()
            phone = input.input_phone()
            street = input.input_street()
            house_number = input.input_house_number()
            postal_code = input.input_postal_code()
            municipality = input.input_municipality()
            country = input.input_country() or "BE"  # Default country is "BE"

            # Validate required input fields
            if not first_name or not last_name or not street or not postal_code or not municipality:
                ui.notification_show("Please fill in all required fields.")
                return

            # Create Address and Person instances
            address = Address(
                street=street,
                house_number=house_number,
                postal_code=postal_code,
                municipality=municipality,
                country=country
            )
            person = Person(
                name_first=first_name,
                name_last=last_name,
                email=email,
                phone_number=phone,

            )
            person.address = address

            # Save to database using DBService
            success = await db_service.add_person(person)
            if success:
                ui.notification_show(f"Person '{first_name} {last_name}' added successfully.")
            else:
                ui.notification_show("Failed to add person. Please try again.")

        # Add the logic to render the generated Folium map

    @output
    @render.ui
    async def company_map_html():

        return ui.a("Open Map", href='http://127.0.0.1:8005/companies', target="_blank")


# Create the app

app = App(app_ui, server, debug=True)