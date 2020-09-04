from automation import CommandSequence, TaskManager
import pandas as pd

# number of browsers
NUM_BROWSERS = 2
DB_PATH = '~/Documents/MachineLearning/WebCrawler/adblock_sqlite_results/'
LOG_PATH = '~/Documents/MachineLearning/WebCrawler/adblock_logs/'

# retrieve list of sights query from the csv
top_sites = pd.read_csv('~/Downloads/top-1m.csv', nrows=100, header=None)
sites = top_sites.loc[:, 1].values

# Loads the default manager params
# and NUM_BROWSERS copies of the default browser params
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    browser_params[i]['http_instrument'] = True
    # Record cookie changes
    browser_params[i]['cookie_instrument'] = True
    # Record Navigations
    browser_params[i]['navigation_instrument'] = True
    # Record JS Web API calls
    browser_params[i]['js_instrument'] = True
    # Record the callstack of all WebRequests made
    browser_params[i]['callstack_instrument'] = True

    # turn on adblock mode
    browser_params[i]['ublock-origin'] = True

manager_params['data_directory'] = DB_PATH
manager_params['log_directory'] = LOG_PATH

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites
for site in sites:

    site = 'http://' + site

    # Parallelize sites over all number of browsers set above.
    command_sequence = CommandSequence.CommandSequence(
        site, reset=True,
        callback=lambda success, val=site:
        print("CommandSequence {} done".format(val)))

    # Start by visiting the page
    command_sequence.get(sleep=3, timeout=60)

    # Run commands across the three browsers (simple parallelization)
    manager.execute_command_sequence(command_sequence)

# Shuts down the browsers and waits for the data to finish logging
manager.close()
