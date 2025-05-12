import pandas as pd
import plotly.express as px
from shiny import App, ui, render, reactive, Inputs, Outputs
from datetime import date

# Simulated example data (replace with your actual CSV)
data = {
    "orderline_id": [65, 28, 83, 38, 17],
    "date_ordered": ["2023-08-24", "2022-06-08", None, "2022-12-12", None],
    "date_received": ["2024-08-23", "2022-08-30", None, "2022-12-22", None],
    "date_issued": ["2024-11-10", "2022-11-06", None, "2023-05-19", None],
    "date_delivered": ["2024-12-12", "2022-12-28", None, "2023-07-10", None],
    "date_installed": [None, "2023-03-24", None, "2023-07-13", None],
    "date_accepted": [None, "2023-04-03", None, "2023-08-10", None],
    "date_invoiced": [None, "2023-04-26", None, "2023-08-30", None],
    "date_paid": [None, "2023-06-01", None, "2023-09-20", None],
    "date_closed": [None, "2023-07-06", None, "2023-11-18", None]
}

df = pd.DataFrame(data)

# Transform to long format
df_long = df.melt(
    id_vars=["orderline_id"],
    value_vars=[
        "date_ordered", "date_received", "date_issued", "date_delivered",
        "date_installed", "date_accepted", "date_invoiced", "date_paid", "date_closed"
    ],
    var_name="Phase",
    value_name="Date"
)

# Clean date column
df_long["Date"] = pd.to_datetime(df_long["Date"], errors='coerce')
df_long = df_long.dropna(subset=["Date"])

# UI
app_ui = ui.page_fluid(
    ui.h2("📊 Orderline Phase Timeline"),
    ui.input_date_range("date_range", "Filter Date Range",
                        start=date(2022, 1, 1),
                        end=date(2025, 12, 31)
                        ),
    ui.output_ui("timeline_plot")
)


# Server
def server(input: Inputs, output: Outputs, session):
    @reactive.calc
    def filtered_data():
        start_date, end_date = input.date_range()
        mask = (df_long["Date"] >= pd.to_datetime(start_date)) & (df_long["Date"] <= pd.to_datetime(end_date))
        return df_long[mask]

    @output
    @render.ui
    def timeline_plot():
        df_filtered = filtered_data()

        if df_filtered.empty:
            # Empty plot message
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_annotation(text="No data in selected date range",
                               xref="paper", yref="paper", showarrow=False,
                               font=dict(size=20))
        else:
            fig = px.scatter(
                df_filtered,
                x="Date",
                y="orderline_id",
                color="Phase",
                symbol="Phase",
                title="Orderline Phase Timeline",


            )
            fig.update_yaxes(autorange="reversed")
            fig.update_traces(marker=dict(size=12))
            fig.update_layout(
                plot_bgcolor="orange",  # Background of the plotting area
                paper_bgcolor="orange",  # Overall background
                title={
                    "text": "Orderline Phase Timeline",
                    "font": {
                        "size": 24,  # Larger font size
                        "family": "Arial",  # Font family
                        "weight": "bold"  # Makes the title bold
                    },
                    "x": 0.5,  # Centers the title horizontally
                    "xanchor": "center"  # Ensures proper horizontal alignment
                }
            )

            # Embed the Plotly chart as HTML
        from plotly.io import to_html
        fig_html = to_html(fig, full_html=False)

        # Use Shiny's HTML wrapper
        return ui.HTML(fig_html)

# App
app = App(app_ui, server)