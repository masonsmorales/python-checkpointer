# Description: Python script with a date-based checkpoint function, useful for pulling data from APIs
# Author: Mason Morales
# Date: November 4, 2018
# To test this script, try running: cat checkpoint && python checkpoint.py && cat checkpoint 
from datetime import datetime  
from datetime import timedelta  
import os.path
import requests

# Define a default fromDate to pull data from to use if the script has never ran before
defaultFromDate="2018-10-01T00:00:00"
# Define the filename to use when storing our timestamp used in the checkpoint function
checkpointFile="checktime"

# Function to format the date to our API's requirements
def formatDate(timestamp):
    timestamp=str('{:%Y-%m-%dT%H:%M:%S}'.format(timestamp))
    return(timestamp);

# Function to pull data from the API, but this is a test script so we'll just print the results here when we run our checkpoint function
def pullAPI(fromDate,toDate):

    # Define a new variable called requestExample with the URL that you could use in a get from the requests library
    requestExample = "https://www.myapiurl.com/get/fromDate=" + fromDate + "&toDate=" + toDate

    # Print the requestExample URL
    print(requestExample)

    #################################################################################
    # Insert code for authentication, GET API Request, Response Handling, etc. here #
    #################################################################################
    #################################################################################
    # Insert code to verify that a 200 response code from the API was received here #
    ################################################################################# 
    # Now that we've completed our API calls and have done something with the data, let's update the checkpoint file
    # Call the writeCheckpointFile function and pass it our toDate, this will be used as the fromDate on the next run
    writeCheckpointFile(toDate=toDate)

# Write an updated checkpointFile after a successful API call
def writeCheckpointFile(toDate):
            # Open the checkpoint file if it doesn't exist, if it does exist, overwrite it
            f = open(checkpointFile,"w+")
            # Write the future timestamp to the file
            f.write(toDate)
            # Close the file
            f.close

# Function to create toDate
def createToDate():
    # Create ToDate by getting the current date time, then passing it through the formatDate function to get the format we need for the API
    return formatDate(datetime.now())

# Function to perform the actual checkpoint logic
def checkpoint():

    # Determine if the checkpointFile exists and is a file
    try:
        # If the checkpointFile exists then open it
        if os.path.isfile(checkpointFile):
            # Read in the contents of the checkpointFile
            with open(checkpointFile, 'r') as f:
                # Assign the contents of checkpointFile to the fromDate variable
                fromDate = f.read()
                # Now that we have our fromDate, we can create our toDate using the current time, after formatting it by the formatDate function
                # toDate = formatDate(datetime.now())
                toDate = createToDate()
                # Now that we have both a fromDate and a toDate, pass them to the pullAPI function
                pullAPI(fromDate=fromDate, toDate=toDate)

        # If the checkpointFile is not a file or does not exist
        else:
            # Use the defaultFromDate as the fromDate
            fromDate = defaultFromDate
            # Call the createToDate function
            toDate = createToDate()
            # Call the pullAPI function
            pullAPI(fromDate=fromDate, toDate=toDate)

    # Catch IO errors and print them (e.g. checkpointFile is a directory)
    except IOError as e:
        print "Oh no! Looks like there was a problem with the checkpointFile. Here's the error:\n I/O error({0}): {1}".format(e.errno, e.strerror)

# Call the checkpoint function
checkpoint()
