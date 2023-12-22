import datetime

str_default_date = "%Y-%m-%dT%H:%M:%S"


class ReachDateUtils:
    @staticmethod
    def chunk_date_range(start_date, end_date, days_per_chunk):
        """
        Divides the interval between start_date and end_date into blocks of days_to_request days.
        Returns a list of tuples, each representing a date range.
        Each new range starts the day after the end of the previous range.
        """
        ranges = []
        current_start_date = start_date

        while current_start_date < end_date:
            current_end_date = current_start_date + datetime.timedelta(
                days=days_per_chunk - 1
            )

            # Ensure that the final interval does not exceed end_date
            if current_end_date > end_date:
                current_end_date = end_date
            ranges.append((current_start_date, current_end_date))

            # Updating current_start_date to the day after current_end_date
            current_start_date = current_end_date + datetime.timedelta(days=1)

        return ranges

    @staticmethod
    def date_to_str(date: datetime, strf_format: str = None) -> str:
        return date.strftime(strf_format or str_default_date)

    @staticmethod
    def str_to_date(date: str, strf_format: str = None) -> datetime:
        return datetime.datetime.strptime(date, strf_format or str_default_date)
