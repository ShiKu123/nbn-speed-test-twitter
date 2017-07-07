import time
import speedtest
from random import randint
from twitter import *


# converts bits per second (Bps) to kilobits per second (KBps)
# Only used by KBps_to_Mbps.
def to_kilobits_per_second(speed):
    return (speed / 1024)

# converts kbps to mbps
def Kbps_to_Mbps(speed):
    megabits = to_kilobits_per_second(speed) / 1024
    return megabits

# Speed test to test download and upload speeds.
def speed_test():
    results = []
    servers = []
    s = speedtest.Speedtest()
    # Opens the closest/best server for the speed test
    s.get_best_server()
    # Allocates download/upload results to results array.
    results.append(s.download())
    results.append(s.upload())

    return results

# Formats localtime.
def formatted_time():
    local_time = time.asctime( time.localtime(time.time()) )
    return local_time

def tweet(download, upload, time):
    # API tokens
    token = "API_TOKEN_TEAM"
    token_secret = "API_TOKEN_SECRET"
    consumer_key = "API_CONSUMER_KEY"
    consumer_secret = "API_CONSUMER_SECRET"
    # Array of possible messages to post.
    status = [
        t.statuses.update(
            status="@NBN_Australia speeds with @MyRepublicAU: " + download + " down, " + 
                upload + " up, at " + time + ". What happened to 'superfast'"),
        t.statuses.update(
            status="Paying for 100/40 yet getting " + download + "/" + upload + 
                " with FTTN, don't we deserve 1st world speeds?")
    ]
    # Opens communication with Twitter API.
    t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    # Update your status, chooses between 
    # one of two possible status updates
    status[random.randing(0,1)]

if __name__ == "__main__":
    # speedtest results
    results = speed_test()
    download = results[0]
    upload = results[1]

    # current time
    now_time = formatted_time()

    while True:
        # posts status update to twitter when download 
        # is less than 30Mbps (30 MegaBits per second)
        if download < 50 or upload < 10:
            # tweet the speed results and time.
            tweet(download, upload, now_time)
        # sleep for 30 minutes
        sleep(1800)
