import flet as ft
from database_layer.db_service import DBService
from domain.DatabaseModelClasses import Assignment
import asyncio


class AssignmentApp:
    def __init__(self):
        self.db_service = DBService()

    async def fetch_assignments(self):
        # Fetch assignments asynchronously from DBService
        assignments = await self.db_service.read_all_assignment()
        return assignments

    def create_grid(self, assignments):
        # Create a grid view to display assignments
        grid = ft.DataTable(
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

        async def load_assignments():
            page.add(ft.Text("Fetching assignments...", size=20))
            await asyncio.sleep(0.1)  # Allow UI updates
            assignments = await self.fetch_assignments()
            if assignments:
                # Remove the loading message and display the grid
                page.controls.clear()
                page.add(self.create_grid(assignments))
            else:
                page.add(ft.Text("No assignments found", size=20))

        async def main():
            await load_assignments()

        asyncio.run(main())


if __name__ == "__main__":
    AssignmentApp().main(ft.app(target=AssignmentApp().main))