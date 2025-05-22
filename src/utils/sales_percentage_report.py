from utils.report_ABC import Report
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

class SalesPercentageReport(Report):

    async def get_content(self) ->[]:
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
        return fig

    @staticmethod
    def name_suffix()->str:
        return "sales_percentage"