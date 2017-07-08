import time
import speedtest
import random
from twitter import *


# converts bits per second (Bps) to kilobits per second (KBps)
# Only used by KBps_to_Mbps.
def to_Kbps(speed):
    return (speed / 1024)

# converts kbps to mbps
def to_Mbps(speed):
    megabits = to_Kbps(speed) / 1024
    return round(megabits, 2)

# Speed test to test download and upload speeds.
def speed_test():
    results = []
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
    token = ""
    token_secret = ""
    consumer_key = ""
    consumer_secret = ""
    # Array of possible messages to post.
    status = [
        t.statuses.update(
            status="@NBN_Australia speeds with @MyRepublicAU: " + download + " down, " + 
                upload + " up, at " + time + ". What happened to 'superfast'"),
        t.statuses.update(
            status="Paying for 100/40 yet getting " + download + "/" + upload + 
                " with FTTN, don't we deserve 1st world speeds?"),
        t.statuses.update(
            status="Hey @MyRepublic, I'm on @NBN_Australia am currently getting " + 
                download + "down/" + upload + "up. I'm paying for 100/40. #NBN #MyRepublic #speedtest")
    ]
    # Opens communication with Twitter API.
    t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    # Update your status, chooses random tweet from above
    random.choice(status)

def speed_test_log(download, upload, time):
    log_path = "speedtest.log"
    log_file = open(log_path, 'a')
    log_file.write(str(download) + ",")
    log_file.write(str(upload) + ",")
    log_file.write(time)
    log_file.write('\n')
    log_file.close()

if __name__ == "__main__":
    print("Let's get started...")
    while True:
        # current time
        now_time = formatted_time()
        # speedtest results
        results = speed_test()
        download = to_Mbps(results[0])
        upload = to_Mbps(results[1])

        speed_test_log(download, upload, now_time)

        # posts status update to twitter when download 
        # is less than 30Mbps (30 MegaBits per second)
        if download < 30:
            # tweet the speed results and time.
            tweet(download, upload, now_time)
            # print("Tweeted!")
        # sleep for 30 minutes
        time.sleep(1800)
