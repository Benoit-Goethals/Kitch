import datetime
from pathlib import Path
from uuid import uuid4
import matplotlib.pyplot as plt
import pandas as pd

import plotly.express as px
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Image, Table, PageBreak
from src.configurations.configuration_manager import ConfigurationManager
from src.utils.report_ABC import Report


class GanttReport(Report):

    async def get_content(self) -> []:
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
        elements.append(Paragraph("Gantt Projects Reports", style=style_sheet["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(PageBreak())
        projects = await self.db_service.get_all_projects_phases()
        for project in projects:

            temp = []

            if project:
                for d in project.phases:
                    temp.append(dict(Resource=f"{project.client.company.company_name}", Start=project.date_start,
                                     Finish=project.date_end, Task=f"CLient {project}"))
                    temp.append(dict(Resource=f"{project.client.company.company_name}", Start=d.date_start_client,
                                     Finish=d.date_end_client, Task=f"CLient {d.name}"))
                    temp.append(dict(Resource=f"{project.client.company.company_name}", Start=d.date_start_planned,
                                     Finish=d.date_end_planned, Task=f"Planning {d.name}"))
                df = pd.DataFrame(data=temp)
                fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource")
                fig.update_xaxes(tickangle=-45, tickformat="%Y-%m-%d")
                fig.update_yaxes(autorange="reversed")

                fig.update_layout(
                    plot_bgcolor='white',
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='rgba(211,211,211,0.3)',
                        griddash='dash',
                    ),
                )

                for i in range(len(df)):
                    if i % 2:
                        fig.add_shape(
                            type="rect",
                            x0=df['Start'].min(),
                            x1=df['Finish'].max(),
                            y0=i - 0.5,
                            y1=i + 0.5,
                            fillcolor="rgba(242,242,242,0.3)",
                            line_width=0,
                            layer="below"
                        )

                now = datetime.datetime.now().strftime("%Y-%m-%d")
                fig.add_shape(
                    type="line",
                    x0=now, x1=now,
                    y0=0, y1=1,
                    xref="x",
                    yref="paper",
                    line=dict(color="Red", width=2, dash="dash"),
                    name="Now"
                )

                # Update layout to show annotation
                fig.add_annotation(
                    x=now, y=1,
                    text="Now",
                    showarrow=True,
                    arrowhead=2,
                    ax=0, ay=-40,
                    xref="x", yref="paper"
                )


                try:
                    plot_path = str(Path(ConfigurationManager().config_pdf) / f"{uuid4().hex}.png")
                    fig.write_image(plot_path, format="png",engine="kaleido")  # Save as PNG file

                    #plt.close(fig)
                    elements.append(Paragraph(f"Gantt", style_sheet["Title"]))
                    elements.append(Spacer(1, 12))
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
        return "gantt_report"