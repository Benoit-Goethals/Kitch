import flet as ft
from database_layer.db_service import DBService
import asyncio


class AssignmentApp:
    def __init__(self):
        self.db_service = DBService()

    async def fetch_assignments(self):
        # Fetch assignments asynchronously from DBService
        return await self.db_service.read_all_assignment()

    def create_grid(self, assignments):
        # Create a DataTable for grid-like structure
        grid = ft.DataTable(
            border=ft.border.all(1, "black"),  # Add borders to the table
            bgcolor="#f9f9f9",  # Light background color for the grid
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Client ID")),
                ft.DataColumn(ft.Text("Calculator ID")),
                ft.DataColumn(ft.Text("Salesman ID")),
                ft.DataColumn(ft.Text("Project Leader ID")),
                ft.DataColumn(ft.Text("Scheduling")),
                ft.DataColumn(ft.Text("Date Acceptance")),
                ft.DataColumn(ft.Text("Date Start")),
                ft.DataColumn(ft.Text("Date End")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(assign.assignment_id))),
                        ft.DataCell(ft.Text(str(assign.client_id))),
                        ft.DataCell(ft.Text(str(assign.calculator_id))),
                        ft.DataCell(ft.Text(str(assign.salesman_id))),
                        ft.DataCell(ft.Text(str(assign.project_leader_id))),
                        ft.DataCell(ft.Text(str(assign.scheduling))),
                        ft.DataCell(ft.Text(str(assign.date_acceptance))),
                        ft.DataCell(ft.Text(str(assign.date_start))),
                        ft.DataCell(ft.Text(str(assign.date_end))),
                    ]
                )
                for assign in assignments
            ],
        )
        return grid

    def main(self, page: ft.Page):
        page.title = "Assignment Grid"
        page.scroll = "auto"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.padding = 10

        async def load_assignments():
            # Display a loading message while data is loading
            page.add(ft.Text("Fetching assignments...", size=20))
            await asyncio.sleep(0.1)  # Allow the UI to update
            assignments = await self.fetch_assignments()
            page.controls.clear()  # Clear loading message
            if assignments:
                # Add the grid to the page
                page.add(self.create_grid(assignments))
            else:
                page.add(ft.Text("No assignments found", size=20))

        asyncio.run(load_assignments())


if __name__ == "__main__":
    AssignmentApp().main(ft.app(target=AssignmentApp().main))