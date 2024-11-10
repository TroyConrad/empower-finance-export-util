# empower-finance-export-util
Simplify extracting net worth data from the Empower (aka Personal Capital) Web API

This script requires Python 3.x.

Log into personalcapital.com in Chrome.

Open Developer Tools, and go to "Network".

Select the desired date range in the "Net Worth" section.

There should appear an "getHistories" API call. Save the response to a text file.

Run "python empower-finance-export-util.py <text file> [--monthly]"

The script will extract the totalAssets or aggregateBalance for any listed dates, then export this data to a tab-seperated file, for easy import into Excel, etc.

The optional "--monthly" argument will only export the first of every month.
