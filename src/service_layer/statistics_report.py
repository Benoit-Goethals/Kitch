from typing import Any
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

from src.core.statistics import Statistics
from src.service_layer.report_ABC import Report


class StatisticsReport(Report):

    def __init__(self):
        super().__init__()

    async def get_content(self) -> list[Any]:
        try:
            st=Statistics(self.db_service)
            data_workers = await st.workers_Assignments()
            data_articles = await st.articles_statics()
            data_projects = await st.projects_statics()

            # Define styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "Title",
                parent=styles["Title"],
                fontSize=16,
                spaceAfter=12,
                alignment=1
            )
            heading_style = ParagraphStyle(
                "Heading",
                parent=styles["Heading2"],
                fontSize=12,
                spaceAfter=8,
                textColor=colors.darkblue,
            )
            normal_style = styles["BodyText"]

            elements = []

            # Title
            elements.append(Paragraph("Statistics Report", title_style))
            elements.append(Spacer(1, 12))

            # Worker Statistics
            elements.append(Paragraph("Worker Statistics", heading_style))
            elements.append(Spacer(1, 6))
            worker_stats = [
                f"Average Assignments: {data_workers.get('avgCountAssigment', 0)}",
                f"Max Assignments: {data_workers.get('maxCountAssignment', 0)}",
                f"Min Assignments: {data_workers.get('minCountAssignment', 0)}",
            ]
            elements.extend([Paragraph(stat, normal_style) for stat in worker_stats])
            elements.append(Spacer(1, 12))

            # Over-tasked Workers
            if data_workers.get("overTaskedWorkers"):
                elements.append(Paragraph("Over-tasked Workers", heading_style))
                over_tasked = [
                    Paragraph(f"- {worker}", normal_style)
                    for worker in data_workers["overTaskedWorkers"]
                ]
                elements.extend(over_tasked)
            elements.append(Spacer(1, 12))

            # Under-utilized Workers
            if data_workers.get("underUtilizedWorkers"):
                elements.append(Paragraph("Under-utilized Workers", heading_style))
                under_utilized = [
                    Paragraph(f"- {worker}", normal_style)
                    for worker in data_workers["underUtilizedWorkers"]
                ]
                elements.extend(under_utilized)
            elements.append(PageBreak())

            # Article Statistics
            elements.append(Paragraph("Article Statistics", heading_style))
            article_stats = [
                f"Average Price: {data_articles.get('AveragePrice', 0):.2f} euro",
                f"Minimum Price: {data_articles.get('MinPrice', [0])[0]:.2f} euro",
                f"Maximum Price: {data_articles.get('MaxPrice', [0]):.2f} euro",
            ]
            elements.extend([Paragraph(stat, normal_style) for stat in article_stats])
            elements.append(Spacer(1, 12))

            # Top Articles
            if data_articles.get("Top_Articles"):
                elements.append(Paragraph("Top Articles", heading_style))
                top_articles = [
                    (article[0], f"{article[1]} purchases")
                    for article in data_articles["Top_Articles"]
                ]
                table_data = [["Article", "Purchases"]] + top_articles
                table = Table(table_data, style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)
            elements.append(Spacer(1, 12))

            # Top Companies
            if data_articles.get("Top_Companies"):
                elements.append(Paragraph("Top Purchasing Companies", heading_style))
                top_companies = [
                    (company[0], f"{company[1]} articles")
                    for company in data_articles["Top_Companies"]
                ]
                table_data = [["Company", "Articles"]] + top_companies
                table = Table(table_data, style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)
            elements.append(PageBreak())

            # Project Statistics
            elements.append(Paragraph("Project Statistics", heading_style))
            project_stats = [
                f"Total of all projects: {data_projects.get('TotalPrice', 0):.2f} euro",
                f"Average: {data_projects.get('AveragePrice', 0):.2f} euro",
                f"Minimum: {data_projects.get('MinPrice', [0]):.2f} euro",
                f"Maximum: {data_projects.get('MaxPrice', [0]):.2f} euro",
            ]
            elements.extend([Paragraph(stat, normal_style) for stat in project_stats])
            elements.append(Spacer(1, 12))

            return elements

        except Exception as e:
            raise RuntimeError(f"Error generating the PDF: {e}")

    @staticmethod
    def name_suffix() -> str:
        return "StatisticsReport"