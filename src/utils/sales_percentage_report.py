import datetime
from pathlib import Path
from uuid import uuid4
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Image, Table, PageBreak
from src.configurations.configuration_manager import ConfigurationManager
from src.utils.report_ABC import Report


class SalesPercentageReport(Report):

    async def get_content(self) -> []:
        style_sheet = getSampleStyleSheet()
        elements = []
        title = f"Data Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        elements.append(Paragraph(title, style_sheet["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Sales Percentage Report", style_sheet["BodyText"]))
        elements.append(Spacer(1, 12))

        for year in range(1990, 2026):
            projects = await self.db_service.get_all_projects_phases_year(str(year))
            if projects:  # Check if we got any projects
                total_projects = []
                for project in projects:  # Iterate through the list of projects
                    if project.phases:  # Check if this project has phases
                        total_sales_price = sum([
                            ph.sales_price for phase in project.phases
                            for ph in phase.order_lines if ph.sales_price is not None
                        ])
                        total_projects.append((project.client.company.company_name, total_sales_price))
                
                if total_projects:  # Only create visualization if we have data
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
                        elements.append(PageBreak())
                        elements.append(Spacer(1, 12))
                    except Exception as e:
                        raise RuntimeError(f"Error generating the PDF: {e}")
        return elements

    @staticmethod
    def name_suffix() -> str:
        return "sales_percentage"