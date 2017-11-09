#!/usr/bin/env python

import sys
import os
import time
import subprocess
import json

ss_file = "/tmp/screenshot.png"
taken_file = "/tmp/screentool-taken"
upload_file = "/tmp/screentool-uploaded"
link_file = "/tmp/screentool-link"
api_url = "http://status.novaember.com/image"
secret_file = os.environ["HOME"] + "/.nvsecret"

use_shorturl = True

from gi.repository import Notify

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

def upload_image(file_path):
        secret = open(secret_file, "r")
        secret_data = secret.read()
        secret.close()

        Notify.Notification.new("Uploading image...").show()
        process = subprocess.Popen(["curl", "-s", api_url,
                                    "-F", "file=@" + file_path,
                                    "-F", "secret=" + secret_data],
                                   stdout=subprocess.PIPE)

        out, err = process.communicate()
        output = json.loads(out)
        if output["status"] == "fail":
            Notify.Notification.new("Failed to upload image: ", out).show()
            sys.exit(1)
        else:
            if use_shorturl:
                url = output["shorturl"]
            else:
                url = output["url"]
            Notify.Notification.new("Image Uploaded!", url).show()
            return url


if __name__ == "__main__":
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
            url = upload_image(ss_file)

            f = open(link_file, "w")
            f.write(url)
            f.close()
            f = open(upload_file, "w")
            f.write(str(time.time()))
        else:
            f = open(link_file, "r")
            url = f.read()
            f.close()
            Notify.Notification.new("Image already uploaded!", url).show()

        os.system("echo " + url + " | xclip -sel clipboard")
