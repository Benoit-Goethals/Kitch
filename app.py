from shiny import App, ui, reactive, render
from ipyleaflet import Map, Marker, Icon
from ipywidgets import HTML
from shinywidgets import render_widget
import pandas as pd

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

</style>
"""

# App UI
app_ui = ui.page_fluid(
    ui.HTML(table_styles),  # Insert the CSS styling for the table
    ui.navset_tab(  # Add tabbed navigation
        ui.nav_panel(
            "Home",
            ui.tags.div(
                ui.h2("Welcome to the App"),

                ui.output_plot("home"),
                class_="nav-panel-content"  # This will center everything inside
            ),
        ),

        ui.nav_panel(
            "Company Table",  # Second tab
            ui.h2("Company Table"),
            ui.output_table("company_table")  # Render company table here
        ),
        ui.nav_panel(
            "Project Table",  # Third tab
            ui.h2("Project Table"),
            ui.output_table("project_table")  # Render assignment table here
        ),
        ui.nav_panel(
            "Pivot Table",  # Fourth tab for pivot table
            ui.h2("Pivot Table: Assignments and Sub-Assignments"),
            ui.output_table("pivot_table"),  # Render the pivot table here
        ),

        ui.nav_panel(
            "Company Map",  # Third tab for the interactive map
            ui.h2("Company Locations on Map"),
            ui.output_ui("map_ui"),  # Render the interactive map here
        ),

        ui.nav_panel(
            "Persons Table",  # New tab for displaying persons
            ui.h2("Persons Table"),
            ui.output_table("persons_table")  # Render persons table here
        ),
        # Additional tab in the user interface for persons
        ui.nav_panel(
            "Persons add",  # Persons tab
            ui.tags.div(  # Outer container for keeping the form horizontally centered
                ui.tags.div(  # Main container for the form
                    [
                        # Center the title across both columns
                        ui.output_table("add_person_effect", style="grid-column: 1 / -1;"),  # Table spans both columns
                        ui.h3("Add New Person", style="grid-column: 1 / -1; text-align: center;"),  # Header spans both columns
                        # First Column
                        ui.input_text("input_first_name", label="First Name", placeholder="Enter First Name"),
                        ui.input_text("input_last_name", label="Last Name", placeholder="Enter Last Name"),
                        ui.input_text("input_email", label="Email", placeholder="Enter Email Address"),
                        ui.input_text("input_phone", label="Phone Number", placeholder="Enter Phone Number"),
                        # Second Column
                        ui.h3("Address Details", style="grid-column: 1 / -1; text-align: left;"),  # Align header to left
                        ui.input_text("input_street", label="Street", placeholder="Enter Street"),
                        ui.input_text("input_house_number", label="House Number", placeholder="Enter House Number"),
                        ui.input_text("input_postal_code", label="Postal Code", placeholder="Enter Postal Code"),
                        ui.input_text("input_municipality", label="Municipality", placeholder="Enter Municipality"),
                        ui.input_text("input_country", label="Country", placeholder="Enter Country (default: BE)"),
                        # Submit Button Spans Both Columns
                        ui.tags.div(
                            ui.input_action_button("add_person_btn", "Add Person"),
                            style="grid-column: 1 / -1; text-align: center;"  # Center the button
                        ),
                    ],
                    style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; align-items: start; padding: 10px;"  # Reduced spacing
                ),
                style="display: flex; justify-content: center; padding: 10px;"  # Remove vertical centering
            )
        ),
        ui.nav_panel(
            "Company Map",  # Tab for the created map
            ui.h2("Generated Folium Map with Company Locations"),
            ui.output_ui("company_map_html")  # Render the Folium map as HTML file
        ),
        ui.nav_panel(
            "Data Grid",
            ui.tags.div(
                ui.h2("Project Data Grid"),
                ui.output_data_frame("data_grid"),
                class_="nav-panel-content"
            ),



        )

    )
)


# Server Logic
def server(input, output, session):
    @reactive.Calc
    def fetch_companies():
        """Fetch all companies asynchronously from the real database using db_service."""
        # Call the read_all_companies method
        return db_service.get_all_companies()

    @reactive.Calc
    async def fetch_projects():
        return await db_service.get_all_projects()

    # Add this fetch function to the server logic
    @reactive.Calc
    def fetch_persons():
        """Fetch all persons asynchronously from the database."""
        return db_service.get_all_persons()

    @reactive.Calc
    def fetch_persons_address():
        """Fetch all persons asynchronously from the database."""
        return db_service.get_all_persons_with_address()

    @render.plot(alt="A Seaborn histogram on penguin body mass in grams.")
    async def home():
        data = await db_service.get_all_phases()

        if not data:
            print("Data is empty!")
            return None  # No data, so no plot to show.

        total_order_lines = []
        for phase in data:
            total_order_lines.append((phase.name, sum([ph.sales_price for ph in phase.orderlines if ph.sales_price is not None])))

        # Convert the list to a DataFrame

        df = pd.DataFrame(total_order_lines, columns=["name", "sales_price"])

        # Plot using sns.histplot
        ax = sns.histplot(data=df, x="name", bins=input.n())
        ax.set_title("Sales Price by Phase")
        ax.set_xlabel("Phase")
        ax.set_ylabel("Total Sales Price")

        return ax

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
                                       "cols": [0,],
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

    #todo Not working
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

app = App(app_ui, server)