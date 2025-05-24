import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer, Image, Table, PageBreak
from src.configurations.configuration_manager import ConfigurationManager
from src.service_layer.report_ABC import Report


class TurnoverReport(Report):
    """
    A specialized class inheriting from `Report` to generate a turnover report
    containing project phases and their respective total sales prices. This
    report includes graphical and tabular representations for better insights.

    This class integrates with a database service to fetch project and phase
    details, processes the results into a format appropriate for PDF
    generation, and creates styled, paginated content. It also dynamically
    generates bar chart visualizations for each project, stores the graphs as
    images, and embeds them into the final report. Errors encountered during
    report generation process are appropriately handled.

    :ivar db_service: A service used to interact with the database for retrieving
                      project and phase data.
    :type db_service: DatabaseService
    """
    def __init__(self):
        super().__init__()

    async def get_content(self)-> list[Any]:
        """
        Asynchronously generates a list of content elements for a PDF report which includes styled text,
        charts, and tables. The function fetches project and phase data from a database service, processes
        it to calculate total sales prices for different phases, creates corresponding visualizations, and
        compiles them into the structure suitable for PDF generation.

        :raises RuntimeError: If an error occurs during report generation this exception is raised with a
            relevant error message.
        :return: A list of elements for the PDF content, including paragraphs, spacers, tables, and images.
        :rtype: list[Any]
        """
        style_sheet = getSampleStyleSheet()
        elements = []
        title = f"Data Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(title, ParagraphStyle(fontName="Helvetica-Bold",
                                                        name="title",
                                                        fontSize=30,
                                                        leading=22,
                                                        alignment=1,
                                                        spaceAfter=6)))
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("Turnover reports", style=style_sheet["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(PageBreak())

        try:
            projects = await self.db_service.get_all_projects_phases()
            for project in projects:
                data = [
                    (phase.name,
                     sum(order_line.sales_price for order_line in phase.order_lines if order_line.sales_price is not None))
                    for phase in project.phases
                ]
                df = pd.DataFrame(data, columns=["Phase Name", "Total Sales Price"])
                fig, ax = plt.subplots()
                ax.bar(df["Phase Name"], df["Total Sales Price"])
                ax.set_title(f"Total Sales by {project.client.company.company_name}")
                ax.set_xlabel("Phase Name")
                ax.set_ylabel("Total Sales Price")
                plt.tight_layout()
                plot_path = str(Path(ConfigurationManager().config_pdf) / f"{uuid4().hex}.png")
                plt.savefig(plot_path)
                plt.close(fig)
                elements.append(Paragraph(f"Turnover pie {project.client.company.company_name}", style=style_sheet["Title"]))
                elements.append(Image(plot_path, width=15 * cm, height=10 * cm))
                elements.append(Spacer(1, 12))
                table_data = [df.columns.tolist()] + df.values.tolist()
                table = Table(table_data)
                elements.append(table)
                elements.append(PageBreak())
                elements.append(Spacer(1, 12))
        except Exception as e:
            raise RuntimeError(f"Error generating the PDF: {e}")
        return elements

    @staticmethod
    def name_suffix()->str:
        return "TurnoverReport"


