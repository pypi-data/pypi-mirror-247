from . import QueryNotify,QueryStatus

class QueryNotifyDict(QueryNotify):
    def __init__(self,result=None):
        """Create Query Notify Print Object.

        Contains information about a specific method of notifying the results
        of a query.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.
        print_all              -- Boolean indicating whether to only print all sites, including not found.
        browse                 -- Boolean indicating whether to open found sites in a web browser.

        Return Value:
        Nothing.
        """

        super().__init__(result)
        self.data = dict()

        return
        

    def start(self, message=None):
        pass

    def countResults(self):
        """This function counts the number of results. Every time the function is called,
        the number of results is increasing.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        The number of results by the time we call the function.
        """
        global globvar
        globvar += 1
        return globvar

    def update(self, result):

        self.result = result
        
        if result.status == QueryStatus.CLAIMED:
            self.data[self.result.site_name] = self.result.site_url_user

    def finish(self):
        return self.data
