import requests
from datetime import datetime, timedelta


class ExchangeRateAPI(object):
    def __init__(
        self, 
        api_base='http://api.exchangeratesapi.io/v1/', # Only http, https forbidden for free plans
        access_key=None
    ):
        self.api_base = api_base.rstrip("/")
        self.access_key = access_key
        
        # Check if app ID is provided
        if not (self.access_key):
            raise ValueError("You must provide a valid access key.")

        self.session = requests.Session()

        
    def get_latest(self):
        """
        This endpoint, depending on your subscription plan will return real-time exchange rate data 
        which gets updated every 60 minutes, every 10 minutes, or every 60 seconds.
        ref. https://exchangeratesapi.io/documentation/#latestrates
        """
        return self.__request("latest")

    
    def get_historical(self, date):
        """
        With this endpoint we have the possibility to see historical rates of the currencies back to 1999,
        most of the currencies data are available until 1999. 
        You can query the Exchangerates API for historical rates 
        by appending a date (format YYYY-MM-DD) to the base URL.
        ref. https://exchangeratesapi.io/documentation/#historicalrates
        """
        return self.__request(date)
    

    def get_historical_time_series(self, start_date_str, end_date_str, verbose=False):
        """
        This function retrieves historical exchange rates for a series of dates.
        It takes start_date_str and end_date_str as string arguments in the format "YYYY-MM-DD",
        converts them to datetime objects, loops over this date range, 
        and calls the get_historical function for each date.
        Returns a dictionary with dates as keys and the corresponding exchange rate data as values.
        
        Args:
            start_date_str (str): The start date for the historical data series in "YYYY-MM-DD" format.
            end_date_str (str): The end date for the historical data series in "YYYY-MM-DD" format.
        """
        # Convert string dates to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("start_date and end_date must be in 'YYYY-MM-DD' format")

        # Validate the date range
        if start_date > end_date:
            raise ValueError("start_date must be before or equal to end_date")

        # Generate the list of dates
        dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        # Dictionary to store historical data
        historical_data = {}

        # Loop over the dates and fetch historical data
        for counter, date in enumerate(dates):
            formatted_date = date.strftime("%Y-%m-%d")
            try:
                historical_data[formatted_date] = self.get_historical(formatted_date)
            except ExchangeRateError as e:
                print(f"Error fetching data for {formatted_date}: {e}")
            
            if counter % 10 == 0:
                progress_percentage = (counter / len(dates)) * 100
                self.verbose_print(verbose, f"Progress: {progress_percentage:.2f}% complete")
        
        return historical_data


    def __request(self, endpoint, payload=None):
        if payload is None:
            payload = {}

        # Include the access_key in the payload
        payload['access_key'] = self.access_key
        url = self.api_base + "/" + endpoint
        request = requests.Request("GET", url, params=payload)
        prepared = request.prepare()

        response = self.session.send(prepared)
        if response.status_code != requests.codes.ok:
            raise ExchangeRateStatusError(request, response)
        json = response.json()
        if json is None:
            raise ExchangeRateDecodeError(request, response)
        return json

    
    @staticmethod
    def verbose_print(verbose, msg):
        if verbose:
            print(msg)
        

class ExchangeRateError(Exception):
    """Exchange Rates Error"""
    def __init__(self, req, resp):
        super(ExchangeRateError, self).__init__()
        self.request = req
        self.response = resp

    def __str__(self):
        return f"Error with request {self.request}: {self.response.content}"


class ExchangeRateStatusError(ExchangeRateError):
    """API status code error"""
    def __str__(self):
        return f"Status Error: Received status code {self.response.status_code} for request {self.request.url}"


class ExchangeRateDecodeError(ExchangeRateError):
    """JSON decode error"""
    def __str__(self):
        return "JSON Decode Error: Unable to parse JSON response."