from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4

from src.configurations.configuration_manager import ConfigurationManager
from src.utils.report_ABC import Report
from src.utils.turnover_report import TurnoverReport


class PdfGenerator:


    def generate_pdf(self,report_to_generate:Report):

        try:
            doc = SimpleDocTemplate(ConfigurationManager().config_pdf+"\\test01.pdf", pagesize=A4)
            elements = report_to_generate.get_content()
            doc.build(elements)
        except Exception as e:
            raise RuntimeError(f"Error generating the PDF: {e}")



if __name__ == "__main__":
    # Example usage
    generator = PdfGenerator()
    generator.generate_pdf(TurnoverReport())