# empower-finance-export-util
Simplify extracting net worth data from the Empower (aka Personal Capital) Web API

## Requirements

1. A personalcapital.com account
2. Python 3.x

## Usage

1. Log into [personalcapital.com](https://home.personalcapital.com/).

2. Open Developer Tools, and go to "Network" (Chrome-specific, adjust as needed for other web browsers).

3. Select the desired date range in the "Net Worth" section.

4. There should appear an "getHistories" API call. Save the response to a text file.

5. Run "python empower-finance-export-util.py <text file> [--monthly]".

The script will extract the totalAssets or aggregateBalance for any listed dates, then export this data to a tab-separated file, for easy import into Excel, etc.

The optional "--monthly" argument will only export the first of every month.
