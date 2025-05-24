import datetime
import logging
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from src.configurations.configuration_manager import ConfigurationManager
from src.database_layer.db_service import DBService
from src.service_layer.report_ABC import Report
from src.service_layer.gantt_report import GanttReport


class PdfGenerationError(Exception):
    """
    Exception raised when an error occurs during PDF generation.

    This custom exception is intended to handle errors related to PDF generation
    processes. It logs the error message using Python's standard logging library
    when the exception is instantiated.

    :ivar __logger: Logger instance used to log error messages.
    :type __logger: logging.Logger
    """
    def __init__(self, message):
        super().__init__(message)
        self.__logger = logging.getLogger(__name__)
        self.__logger.error(message)


class PdfGenerator:
    def __init__(self, config_manager: ConfigurationManager = None,db_service=None):
        self.config_manager = config_manager or ConfigurationManager()
        self.db_service=db_service

    async def generate_pdf(self, report_to_generate: Report) -> Path:
        """
        Generates a PDF file for the given report.

        This method takes a report object, generates its content using the specified
        service, and saves the resulting PDF file in a configured directory. It also
        handles cleanup of temporary files such as PNG images used during generation.
        Any issues during the process will raise custom errors to indicate specific
        problems encountered, such as I/O errors or unexpected exceptions during the
        PDF generation process.

        :param report_to_generate: The report object to generate the PDF for.
        :type report_to_generate: Report
        :return: A Path object pointing to the generated PDF file.
        :rtype: Path
        :raises PdfGenerationError: If there is an issue creating the PDF directory,
            generating the document, or during cleanup of temporary files.
        """
        report_to_generate.db_service=self.db_service
        pdf_dir = Path(self.config_manager.config_pdf)
        if not pdf_dir.exists():
            try:
                pdf_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                raise PdfGenerationError(f"Cannot create PDF directory: {e}")
        pdf_path = pdf_dir.joinpath(f"{report_to_generate.name_suffix()}{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}.pdf")

        try:
            doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
            elements = await report_to_generate.get_content()
            doc.build(elements)
            for file in pdf_dir.glob("*.png"):
                try:
                    file.unlink()  # Delete the file
                except Exception as e:
                    raise PdfGenerationError(f"IO error while deleting png: {e}")

            return pdf_path
        except (OSError, IOError) as e:
            raise PdfGenerationError(f"IO error while generating PDF: {e}")
        except Exception as e:
            raise PdfGenerationError(f"Unexpected error generating PDF: {e}")


if __name__ == "__main__":
    import asyncio


    async def main():
        generator = PdfGenerator()
        generator.db_service=DBService()
        #pdf_path = await generator.generate_pdf(SalesPercentageReport())
        #pdf_path = await generator.generate_pdf(TurnoverReport())
        pdf_path = await generator.generate_pdf(GanttReport())
        print(f"Generated PDF at: {pdf_path}")


    asyncio.run(main())