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

from src.database_layer.db_service import DBService
from src.configurations.configuration_manager import ConfigurationManager
from src.utils.report_ABC import Report


class SalesPercentageReport(Report):

    async def get_content(self) ->[]:
        style_sheet = getSampleStyleSheet()
        elements = []
        title = f"Data Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        elements.append(Paragraph(title, style_sheet["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Report turn around summary", style_sheet["BodyText"]))
        elements.append(Spacer(1, 12))
        projects_with_phases= await self.db_service.get_all_projects_phases()
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
            plt.tight_layout()
            try:
                plot_path = str(Path(ConfigurationManager().config_pdf) / f"{uuid4().hex}.png")
                plt.savefig(plot_path)
                plt.close(fig)
                elements.append(Image(plot_path))
                elements.append(Spacer(1, 12))
                table_data = [df.columns.tolist()] + df.values.tolist()
                table = Table(table_data)
                elements.append(table)
                elements.append(Spacer(1, 12))
            except Exception as e:
                raise RuntimeError(f"Error generating the PDF: {e}")
        return elements

    @staticmethod
    def name_suffix()->str:
        return "sales_percentage"