from abc import ABC, abstractmethod
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os
from uuid import uuid4

class Report(ABC):

    def __init__(self):
        self.db_service = None

    @abstractmethod
    async def get_content(self)->[]:
        pass

    @staticmethod
    @abstractmethod
    def name_suffix()->str:
        pass

