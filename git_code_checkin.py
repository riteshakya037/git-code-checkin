#!/usr/bin/python3
__author__ = 'Ashish Kayastha'
# Python script for automating Git code check-in emails.
# Usage: git-code-checkin -c <commit-hash>

import argparse
import subprocess
import collections
import sys
import os

changed_files_dict = collections.OrderedDict()

changed_files_dict["New"] = list()
changed_files_dict["Modified"] = list()
changed_files_dict["Renamed"] = list()
changed_files_dict["Deleted"] = list()
# Console colorse
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Code Checkin Script")
    parser.add_argument("-c", "--commit", required=True, dest="Hash", help="Commit Hash")
    args = parser.parse_args()

    hash = args.Hash

    # Git commands to get all the required information
    list_changed_files_cmd = "git diff-tree --no-commit-id --name-status -r -M {}".format(hash)

    # Get list of all files
    pipe = subprocess.Popen(list_changed_files_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pipe.communicate()

    files_list = str(out, encoding="utf_8").splitlines()

    # Maintain separate changed file lists for easier looping
    for file in files_list:
        if file.startswith('A'):
            changed_files_dict["New"].append(file)
        elif file.startswith('M'):
            changed_files_dict["Modified"].append(file)
        elif file.startswith('R'):
            changed_files_dict["Renamed"].append(file)
        elif file.startswith('D'):
            changed_files_dict["Deleted"].append(file)
        else:
            pass

    # get name of branch
    commit_in_branch_cmd = "git branch -r --contains {}".format(hash)
    pipe = subprocess.Popen(commit_in_branch_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pipe.communicate()

    # Create a new string that consists of all the branches a commit is in
    branch_list = str(out, encoding="utf_8").splitlines()
    branch_list = [branch.strip() for branch in branch_list]
    branches = ', '.join(branch_list)

    # Get full commit hash and commit message
    commit_hash_and_message_cmd = "git log {}".format(branch_list[0]) + " --pretty=oneline | grep {}".format(hash)

    # Get additional inputs
    try:
        while True:
            account = input(C + "Account: " + W)
            if account == "":
                print(R + "Cannot leave blank Mandatory Value" + W)
                continue
            else:
                break
        while True:
            client = input(C + "Client: " + W)
            if client == "":
                print(R + "Cannot leave blank Mandatory Value" + W)
                continue
            else:
                break
        while True:
            reviewed_by = input(C + "Code/Unit Test Reviewed By: " + W)
            if reviewed_by == "":
                print(R + "Cannot leave blank Mandatory Value" + W)
                continue
            else:
                break
    except KeyboardInterrupt:
        print(R + "Exiting." + W)
        sys.exit(0)

    # Write an HTML file in user's 'Desktop'
    with open("{}/checkin.html".format(os.getenv("HOME")), 'w') as out_file:
        pipe = subprocess.Popen(commit_hash_and_message_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = pipe.communicate()

        commit = str(out, encoding="utf_8").split(' ', 1)
        try:
            commit_hash, commit_message = tuple(commit)
        except ValueError:
            print(R + "Cannot find Commit" + W)
            sys.exit(0)
        commit_messages = commit_message.split(" -")
        i = 0;
        # Commit Hash
        out_file.write(
            "<div>DasScrub Code CheckIn (" + account.title() + " " + client.title() + ")</div>")
        out_file.write("<div><br></div>")
        # Deermine
        if "#" in commit_messages[0]:
            i = 1
            deermine_list = commit_messages[0].split(",")
            out_file.write(
                "<div><strong>Deermines:</strong>&nbsp;</div><ul>")
            for dm in deermine_list:
                out_file.write(
                    "<li><a href=\"https://svn.deerwalk.com/issues/" + dm.replace("#", "") + "\" target=\"_blank\">" +
                    dm.replace("#", "") + "</a></li>")
            out_file.write("</ul><br/>")

        # Description
        if len(commit_messages) > 1:
            out_file.write(
                "<div><strong>Description:</strong>&nbsp;</div><ol>")
            while i < len(commit_messages):
                out_file.write(
                    "<li>" + commit_messages[i] + "</li>")
                i += 1
            out_file.write("</ol></br>")
        # Code/Unit Test Reviewed By
        out_file.write(
            "<div><b>Code/Unit Test Reviewed By:</b>&nbsp;{}</div>".format(
                reviewed_by))
        out_file.write("<div><br></div>")

        # Git Branch
        out_file.write(
            "<div><b>Git Branch:</b>&nbsp;{}</div>".format(branches))
        out_file.write("<div><br></div>")

        # Commit Hash
        out_file.write("<div><b>Commit Hash:</b>&nbsp;{}</div>".format(
            commit_hash))
        out_file.write("<div><br></div>")

        for header, file_list in changed_files_dict.items():
            if len(file_list) != 0:
                out_file.write(
                    "<div><b>{} Files:</b></div><ul>".format(
                        header))
                for file in file_list:
                    i = 0
                    out_file.write("<li>")
                    for token in file.split('\t'):
                        if i == 0:
                            out_file.write("")
                        elif i == 2:
                            out_file.write(" -> " + token)
                        else:
                            out_file.write(token)

                        i += 1
                    out_file.write("</li>")

                out_file.write("</ul><div><br></div>")

        out_file.write("<div>Regards,</div>")

    # Copy the generated HTML to clipboard
    os.system("xclip -selection clipboard -t text/html {}/checkin.html".format(os.getenv("HOME")))


if __name__ == "__main__": main()
