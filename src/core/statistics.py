import logging
from itertools import count

from src.database_layer.db_service import DBService
import statistics


class Statistics:

    def __init__(self,db_service:DBService):
        self.__db_service=db_service
        self.__logger = logging.getLogger(__name__)

    async def workers_Assignments(self):
        """
        Generates statistical analysis of workers' assignments based on data retrieved
        from a database service. The analysis includes metrics such as the total number
        of assignments per worker, average count of assignments, maximum and minimum
        assignments, as well as lists of over-tasked and under-utilized workers.

        This function processes data related to workers and their assignments, calculating
        aggregated statistics for both individual and overall levels. This data is organized
        in a dictionary format for streamlined reporting and analysis.

        :param self: Instance of the class calling this method.

        :raises Exception: If an error occurs during the execution of database operations or
                           calculations.

        :return: A dictionary containing statistical analysis of workers' assignments,
                 including:
                 - CountAssigmentPerWorker: A list of dictionaries mapping workers' names to
                   their total assignment counts.
                 - avgCountAssigment: Average number of assignments among all workers.
                 - maxCountAssignment: Maximum number of assignments assigned to a single worker.
                 - minCountAssignment: Minimum number of assignments assigned to a single worker.
                 - overTaskedWorkers: A list of worker names with assignments exceeding the average.
                 - underUtilizedWorkers: A list of worker names with zero assignments.
        :rtype: dict
        """
        dict_stat={}
        try:
            data_wa = await self.__db_service.get_workers_and_there_assignments()
            # Calculate total assignments for each worker
            count_ass = [{a.person.name_first + a.person.name_last: len(a.assignments)} for a in data_wa]
            dict_stat["CountAssigmentPerWorker"]=count_ass

            # Calculate the average number of assignments
            avg_ass = [len(a.assignments) for a in data_wa]
            average_assignments = (
                statistics.mean(avg_ass) if avg_ass else 0  # Prevent division by zero if the list is empty
            )
            dict_stat["avgCountAssigment"] = average_assignments

            max_assignments = max(avg_ass, default=0)  # Max tasks assigned to a worker
            min_assignments = min(avg_ass, default=0)  # Min tasks assigned to a worker

            # Identify over-tasked and under-utilized workers
            over_tasked_workers = [
                worker.person.name_first for worker in data_wa if len(worker.assignments) > average_assignments
            ]
            under_utilized_workers = [
                worker.person.name_first for worker in data_wa if len(worker.assignments) == 0
            ]

            dict_stat["maxCountAssignment"] = max_assignments
            dict_stat["minCountAssignment"] = min_assignments
            dict_stat["overTaskedWorkers"] = over_tasked_workers
            dict_stat["underUtilizedWorkers"] = under_utilized_workers

            return dict_stat

        except Exception as e:
            self.__logger.error(f"An error occurred: {e}")
            return []


    async def articles_statics(self):
        """
        Asynchronously computes statistical data regarding articles and suppliers from a database.

        The method fetches supplier data and performs multiple computations:
        - Counts articles grouped by suppliers and identifies the top contributors.
        - Computes the frequency of article purchases, determines the most popular articles,
          and limits the result set to the top 10 articles.
        - Groups purchases by companies and identifies the top 10 purchasing companies.
        - Analyzes pricing information of the articles to calculate average, minimum, and
          maximum price values.

        The results are returned as a dictionary containing the computed statistics.

        :param self: An instance containing a database service used for querying data.

        :return: A dictionary containing statistical information including article counts
            by suppliers, top articles, top purchasing companies, and pricing statistics.
        :rtype: Dict[str, Any]
        :raises Exception: If any error occurs during the database fetch operation or
            calculations.
        """
        dict_stat = {}
        try:
            data_wa = await self.__db_service.get_suppliers()
            count_ass = [{a.company.company_name: len(a.articles)} for a in data_wa]
            dict_stat["SupplerCountArticles"] = count_ass

            # Most Frequently Purchased Articles (Grouped by Article Name)
            article_counter = {}
            for a in data_wa:
                for article in a.articles:
                    article_counter[article.description] = article_counter.get(article.description, 0) + 1

            # Sort articles by frequency and get top results
            sorted_articles = sorted(article_counter.items(), key=lambda x: x[1], reverse=True)
            dict_stat["Top_Articles"] = sorted_articles[:10]

            # Additionally Group by Companies
            company_wise_purchase = {}
            for a in data_wa:
                company = a.company.company_name
                company_wise_purchase[company] = company_wise_purchase.get(company, 0) + len(a.articles)

            # Get top companies
            sorted_companies = sorted(company_wise_purchase.items(), key=lambda x: x[1], reverse=True)
            dict_stat["Top_Companies"] = sorted_companies[:10]  # Top 10 companies

            prices = [
                article.purchase_price for person in data_wa for article in person.articles if article.purchase_price is not None
            ]

            # Calculate average, min, max
            average_price = statistics.mean(prices) if prices else 0
            min_price = min(prices, default=0)
            max_price = max(prices, default=0)
            dict_stat["AveragePrice"]= average_price
            dict_stat["MinPrice"]= min_price,
            dict_stat["MaxPrice"]= max_price

            return dict_stat

        except Exception as e:
            self.__logger.error(f"An error occurred: {e}")
            return []

