#!/usr/bin/env python

import sys
import os
import time
import subprocess
import json
from gi.repository import Notify

ss_file = "/tmp/screenshot.png"
taken_file = "/tmp/screentool-taken"
upload_file = "/tmp/screentool-uploaded"
link_file = "/tmp/screentool-link"
api_url = "http://status.novaember.com/image"
secret_file = os.path.expanduser("~") + "/.nvsecret"

use_shorturl = True

def should_upload():

    if not os.path.isfile(upload_file):
        return True

    taken = open(taken_file, "r")
    taken_time = float(taken.read())
    taken.close()

    upload = open(upload_file, "r")
    upload_time = float(upload.read())
    upload.close()

    return upload_time < taken_time

Notify.init("screentool.py")

if len(sys.argv) == 1:  # Capture
    os.system("maim -s -k -c 1,0.68,0 -b 1 " + ss_file)
    os.system("xclip -sel clipboard -t image/png < " + ss_file)
    f = open(taken_file, "w")  # fuck error handling
    f.write(str(time.time()))
    f.close()
    Notify.Notification.new("Screenshot copied!").show()

elif sys.argv[1] == "upload":
    if not os.path.isfile(ss_file):
        sys.exit(1)

    url = ""

    if should_upload():
        secret = open(secret_file, "r")
        secret_data = secret.read()
        print(secret_data)
        secret.close()
        print("file=@" + ss_file)
        print("-F secret=" + secret_data)

        Notify.Notification.new("Uploading image...").show()
        process = subprocess.Popen(["curl", "-s", api_url,
                                    "-F", "file=@" + ss_file,
                                    "-F", "secret=" + secret_data],
                                   stdout=subprocess.PIPE)
        out, err = process.communicate()
        print("Got output: ", out)
        print("stderr: ", err)
        output = json.loads(out)
        if output["status"] == "fail":
            Notify.Notification.new("Failed to upload image: ", out).show()
            sys.exit(1)
        else:
            if use_shorturl:
                url = output["shorturl"]
            else:
                url = output["url"]

            f = open(link_file, "w")
            f.write(url)
            f.close()
            f = open(upload_file, "w")
            f.write(str(time.time()))
            Notify.Notification.new("Image Uploaded!", url).show()
    else:
        f = open(link_file, "r")
        url = f.read()
        f.close()
        Notify.Notification.new("Image already uploaded!", url).show()

    os.system("echo " + url + " | xclip -sel clipboard")
