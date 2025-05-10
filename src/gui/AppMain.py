from shiny import App, ui, reactive, render
import matplotlib.pyplot as plt
import numpy as np

class AppMain:
    def __init__(self):
        # Initialize Shiny app UI and server
        self.app_ui = self._create_ui()  # Define UI
        self.server = self._create_server()  # Define server logic
        self.app = App(self.app_ui, self.server, debug=True)  # Create Shiny app instance

    def _create_ui(self):
        """
        Define the User Interface (UI) with a Blue Theme.
        """
        blue_theme_css = """
        <style>
            body {
                background-color: #f8f9fa; /* Light background for the body */
                font-family: Arial, sans-serif;
                margin: 0;
            }
            .blue-sidebar {
                background-color: #007BFF; /* Bright blue sidebar */
                color: white; /* White text for contrast */
                padding: 15px;
                height: 100%;
                font-size: 14px;
                border-right: 2px solid #0056b3; /* Slightly darker border */
            }
            .blue-sidebar h3, .blue-sidebar label {
                color: white;
            }
            .blue-header {
                background-color: #0056b3; /* Dark blue header */
                color: white;
                padding: 10px;
                text-align: center;
                border-bottom: 4px solid #00408a; /* Accent border */
            }
            .main-content {
                background-color: #ffffff; /* White background for contrast */
                padding: 20px;
                border-radius: 8px; /* Smooth corners */
                margin: 20px;
            }
            .btn-primary {
                background-color: #0056b3; /* Button blue */
                border-color: #0056b3;
                color: white;
            }
            .btn-primary:hover {
                background-color: #003f7f; /* Darker blue on hover */
                border-color: #003f7f;
            }
            h2, h3, h5 {
                color: #0056b3; /* Blue headers */
            }
        </style>
        """

        # Define the UI layout using Shiny
        ui_layout = ui.page_sidebar(

            # Sidebar Panel
            ui.sidebar(
                ui.tags.div(
                    [
                        ui.h3("Sidebar Menu"),
                        ui.input_slider("num_input", "Select a Number", 0, 100, value=50),
                        ui.input_action_button("btn_click", "Click Me", class_="btn-primary"),  # Styled button
                        ui.tags.hr(),  # Horizontal divider
                        ui.h5("Additional Controls"),
                        ui.input_select(
                            "select_input", "Choose an Option:", ["Option 1", "Option 2", "Option 3"]
                        ),
                    ],
                    class_="blue-sidebar"  # Apply the sidebar styles
                )
            ),
            # Main Panel
            ui.sidebar(
                ui.tags.div(
                    [
                        ui.tags.div(
                            ui.h2("Main Panel"),  # Header for the main panel
                            class_="blue-header"
                        ),
                        ui.tags.div(
                            [
                                ui.output_text("output_text"),
                                ui.output_plot("output_plot"),
                            ],
                            class_="main-content"  # Stylish light content area
                        )
                    ]
                )
            )
        )
        return ui_layout

    def _create_server(self):
        """
        Define the server logic for the Shiny application.
        """
        def server(input, output, session):
            @output
            @render.text
            def output_text():
                return f"You selected number: {input.num_input()}"

            @output
            @render.plot
            def output_plot():
                x = np.linspace(0, 10, 100)
                y = np.sin(x) * input.num_input() / 100  # Scale SIN curve based on slider input

                # Configure plot with blue theme
                fig, ax = plt.subplots()
                ax.plot(x, y, color="#007BFF", label="Sine Wave")
                ax.set_title("Scaled Sine Wave", color="#0056b3", fontsize=14, fontweight="bold")
                ax.set_xlabel("x-axis", color="#0056b3")
                ax.set_ylabel("y-axis", color="#0056b3")
                ax.legend(loc="upper right", fontsize="small", frameon=False)
                ax.grid(color="lightgray", linestyle="--", linewidth=0.5)
                return fig

        return server

# Expose the Shiny app object at the module level
app = AppMain().app