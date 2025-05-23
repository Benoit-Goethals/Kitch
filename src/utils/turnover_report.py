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
from src.utils.report_ABC import Report


class TurnoverReport(Report):
    def __init__(self):
        super().__init__()

    async def get_content(self)-> list[Any]:
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


