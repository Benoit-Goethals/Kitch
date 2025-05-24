import datetime
from pathlib import Path
from uuid import uuid4
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter, date2num
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Image, Table, PageBreak
from src.configurations.configuration_manager import ConfigurationManager
from src.service_layer.report_ABC import Report


class GanttReport(Report):
    """
    Generates a Gantt report based on project and phase data.

    This class is responsible for retrieving project and phase details,
    generating a Gantt chart visualization, and preparing contents for
    a report in PDF format. It helps in visualizing timelines, phases,
    and task durations within projects in a structured format.

    :ivar db_service: The database service used to fetch project and phase details. This is
        required to gather all necessary data for the report generation.
    :type db_service: typing.Any
    """
    async def get_content(self) -> list:
        """
        Generate PDF content elements for a Gantt Report.

        This asynchronous function compiles PDF content elements, including formatted text, Gantt charts,
        and tables, representing project and phase timelines. The content is dynamically created based on
        data retrieved from a database service and is designed for sequential rendering in a PDF document.
        The function supports multiple projects and their respective phases.

        :raises Exception: If there is an error while generating charts or tables.
        :raises Exception: If an error occurs with data comparison or timestamp conversions during plotting.

        :rtype: list
        :return: A list of report content elements for rendering into a PDF.
        """
        style_sheet = getSampleStyleSheet()
        elements = []
        title = f"Gantt Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        elements.append(Paragraph(title, ParagraphStyle(fontName="Helvetica-Bold",
                                                        name="title",
                                                        fontSize=24,
                                                        leading=22,
                                                        alignment=1,
                                                        spaceAfter=30)))

        projects = await self.db_service.get_all_projects_phases()
        for project in projects:
            if not project or not project.phases:
                continue

            # Collect data for the project
            tasks = []
            for phase in project.phases:
                # Project level task
                tasks.append({
                    'Task': f"Project: {project.client.company.company_name}",
                    'Start': project.date_start,
                    'Finish': project.date_end,
                    'Type': 'Project'
                })
                # Phase level tasks
                tasks.append({
                    'Task': f"Phase: {phase.name} (Client)",
                    'Start': phase.date_start_client,
                    'Finish': phase.date_end_client,
                    'Type': 'Client Phase'
                })
                tasks.append({
                    'Task': f"Phase: {phase.name} (Planned)",
                    'Start': phase.date_start_planned,
                    'Finish': phase.date_end_planned,
                    'Type': 'Planned Phase'
                })

            df = pd.DataFrame(tasks)
            df['Start'] = pd.to_datetime(df['Start'])
            df['Finish'] = pd.to_datetime(df['Finish'])
            df['Duration'] = (df['Finish'] - df['Start']).dt.days

            # Create Gantt chart
            fig, ax = plt.subplots(figsize=(15, len(tasks) * 0.5 + 2))

            colors = {'Project': '#FF9999', 'Client Phase': '#66B2FF', 'Planned Phase': '#99FF99'}

            for idx, task in df.iterrows():
                ax.barh(idx, task['Duration'],
                        left=task['Start'],
                        color=colors[task['Type']],
                        height=0.3,
                        alpha=0.8)
                ax.text(task['Start'], idx, f' {task["Task"]}', va='center')

            # Customize the chart
            ax.grid(True, alpha=0.3, axis='x')
            ax.set_yticks([])
            ax.set_title(f"Project Gantt: {project.client.company.company_name}")

            # Format dates on x-axis
            plt.xticks(rotation=45)
            ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

            ax.set_ylim(
                -0.5, len(tasks) - 0.5
            )

            # Add today's marker
            # Then replace the today marker code with:

            # Make sure all timestamps are timezone-aware
            df_start = pd.Timestamp(df['Start'].min(), tz=datetime.timezone.utc)
            df_end = pd.Timestamp(df['Finish'].max(), tz=datetime.timezone.utc)
            now = pd.Timestamp.now(tz=datetime.timezone.utc)

            # Make sure all timestamps are timezone-aware before comparison
            if pd.notnull(df_start) and pd.notnull(df_end):
                try:
                    if df_start <= now <= df_end:
                        # Convert to naive datetime for matplotlib
                        now_plot = date2num(now.tz_localize(None))

                        ax.axvline(x=now_plot, color='red', linestyle='--', alpha=0.7, label='Today')
                        ax.text(now_plot, ax.get_ylim()[1], 'Today',
                                rotation=90, va='bottom', color='red', ha='right')
                except TypeError as e:
                    print(f"Date comparison error: {e}")

            # Add legend
            handles = [plt.Rectangle((0, 0), 1, 1, color=color, alpha=0.8)
                       for color in colors.values()]
            ax.yaxis.set_inverted(True)
            ax.legend(handles, colors.keys(), loc='upper right')

            plt.tight_layout()

            try:
                # Save the chart
                plot_path = str(Path(ConfigurationManager().config_pdf) / f"gantt_{uuid4().hex}.png")
                plt.savefig(plot_path, bbox_inches='tight', dpi=300)
                plt.close(fig)

                # Add to PDF elements
                elements.append(Paragraph(f"Timeline for {project.client.company.company_name}", style_sheet["Heading1"]))
                elements.append(Spacer(1, 12))
                elements.append(Image(plot_path, width=500, height=300))
                elements.append(Spacer(1, 20))

                # Add table with dates
                table_data = [["Task", "Start Date", "End Date", "Duration (days)"]]
                for _, row in df.iterrows():
                    table_data.append([
                        row['Task'],
                        row['Start'].strftime('%Y-%m-%d'),
                        row['Finish'].strftime('%Y-%m-%d'),
                        f"{row['Duration']} days"
                    ])
                elements.append(Table(table_data, repeatRows=1))
                elements.append(PageBreak())

            except Exception as e:
                print(f"Error generating chart for project {project.name}: {e}")
                continue



        return elements

    @staticmethod
    def name_suffix() -> str:
        return "gantt_report"