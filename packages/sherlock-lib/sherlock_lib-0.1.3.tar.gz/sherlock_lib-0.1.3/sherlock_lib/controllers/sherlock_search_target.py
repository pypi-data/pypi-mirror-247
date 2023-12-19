import sys
import re
import requests

from ..models import QueryNotifyDict
from ..models import SitesInformation

from . import sherlock


module_name = "Sherlock: Find Usernames Across Social Networks"
__version__ = "0.14.3"


def search_target(username,timeout=60,sfw=False):

    # Check for newer version of Sherlock. If it exists, let the user know about it
    try:
        r = requests.get(
            "https://raw.githubusercontent.com/sherlock-project/sherlock/master/sherlock/sherlock.py")

        remote_version = str(re.findall('__version__ = "(.*)"', r.text)[0])
        local_version = __version__

        if remote_version != local_version:
            print("Update Available!\n" +
                  f"You are running version {local_version}. Version {remote_version} is available at https://github.com/sherlock-project/sherlock")

    except Exception as error:
        print(f"A problem occurred while checking for an update: {error}")

    try:
        sites = SitesInformation(None)
    except Exception as error:
        print(f"ERROR:  {error}")
        sys.exit(1)

    if sfw:
        sites.remove_nsfw_sites()

    # Create original dictionary from SitesInformation() object.
    # Eventually, the rest of the code will be updated to use the new object
    # directly, but this will glue the two pieces together.
    site_data_all = {site.name: site.information for site in sites}
    site_data = site_data_all


    if not site_data:
        sys.exit(1)

    # Create notify object for query results.
    query_notify = QueryNotifyDict()



    results = sherlock(username,
                        site_data,
                        query_notify,
                        timeout=timeout)

    return query_notify.finish()