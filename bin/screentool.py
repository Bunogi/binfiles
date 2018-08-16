#!/usr/bin/env python

import sys
import os
import time
import subprocess
import gi
import base64
import hashlib

ss_file = "/tmp/screenshot.png"
taken_file = "/tmp/screentool-taken"
upload_file = "/tmp/screentool-uploaded"
link_file = "/tmp/screentool-link"
upload_target = "bunogi@bunogi.xyz:~/shots/"
base_url = "https://shots.bunogi.xyz/"

gi.require_version('Notify', '0.7')
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
        Notify.Notification.new("Uploading image...").show()

        f = open(ss_file, "rb")
        buf = f.read()
        hasher = hashlib.sha3_224()
        hasher.update(buf)

        target_name = str(base64.urlsafe_b64encode(hasher.digest()).hex()[0:4]) + ".png"
        p = subprocess.run(["scp", ss_file, upload_target + target_name])
        print(p.args)
        if p.returncode != 0:
            Notify.Notification.new("Failed to upload image", "got " + str(status)).show()
            sys.exit(1)
        else:
            full_url = base_url + target_name
            Notify.Notification.new("Image uploaded!", full_url).show()
            return full_url

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

        os.system("echo -n " + url + " | xclip -sel clipboard")
