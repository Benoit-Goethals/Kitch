from pathlib import Path
from typing import Any

from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os
from uuid import uuid4

from src.configurations.configuration_manager import ConfigurationManager
from src.utils.report_ABC import Report


class TurnoverReport(Report):

    def get_content(self)-> list[Any]:

        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        # Validate dataframe
        if not isinstance(df, pd.DataFrame):
            raise ValueError("df must be a pandas DataFrame.")


        # Get styles and start creating document elements
        style_sheet = getSampleStyleSheet()
        elements = []

        # Title
        title = f"Data Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        elements.append(Paragraph(title, style_sheet["Title"]))
        elements.append(Spacer(1, 12))

        # Summary
        elements.append(Paragraph("test summary", style_sheet["BodyText"]))
        elements.append(Spacer(1, 12))

        # Generate and Insert Plot
        print("--->"+ConfigurationManager().config_pdf)

        try:
            plot_path = str(Path(ConfigurationManager().config_pdf) / f"{uuid4().hex}.png")

            self.create_sample_plot({'x': df['x'], 'y': df['y']}, plot_path)
            elements.append(Image(plot_path, width=15 * cm, height=10 * cm))
            elements.append(Spacer(1, 12))

            # Insert Table
            table_data = [df.columns.tolist()] + df.values.tolist()
            table = Table(table_data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            elements.append(table)
        except Exception as e:
            raise RuntimeError(f"Error generating the PDF: {e}")

        return elements


    def create_sample_plot(self, data, filename):
        """
        Creates a sample plot from the given data and saves it to a file.
        """
        # Validate data
        if not isinstance(data, dict) or 'x' not in data or 'y' not in data:
            raise ValueError("Data must be a dictionary with 'x' and 'y' keys.")

        # Validate filename
        if not filename or not isinstance(filename, str):
            raise ValueError("A valid filename must be provided.")
        if not os.path.exists(os.path.dirname(filename)) and os.path.dirname(filename):
            raise FileNotFoundError(f"Directory '{os.path.dirname(filename)}' does not exist.")

        try:
            # Create the plot
            plt.figure(figsize=(6, 4))
            plt.plot(data['x'], data['y'], label='Trend')
            plt.title("Trend over Time")
            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.legend()
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
        except Exception as e:
            raise RuntimeError(f"Error creating the plot: {e}")
