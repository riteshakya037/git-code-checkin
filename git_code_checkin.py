#!/usr/bin/python3
__author__ = 'Ashish Kayastha', 'Ritesh Shakya'
# Python script for automating Git code check-in emails.
# Usage: git-code-checkin -c <commit-hash> <commit-hash> ...

import argparse
import collections
import os
import subprocess
import sys
import re

# regex to match deermine pattern e.g. : #12356
deermine_pattern = re.compile(r"#\d{5}")

# Hash-Map of commit:branches
branch_branches = dict()
log_list = dict()
# Hash-Map of deermines and descriptions ({'Deermines':{values}},{'Description':{values}})
commit_message_array = collections.OrderedDict()
commit_message_array["Deermines"] = list()
commit_message_array["Descriptions"] = list()

# Hash-Map of files ({'New':{files}},{'Modified':{files}},...)
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
    parser.add_argument("-c", "--commits", dest="Hashs", nargs='+', help="Commit Hash")
    args = parser.parse_args()

    global hashs
    hashs = args.Hashs
    if not hashs:
        commit_hash_and_message_cmd = "git log --pretty=oneline | head -20"
        pipe = subprocess.Popen(commit_hash_and_message_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = pipe.communicate()
        logs = str(out, encoding="utf_8").splitlines()
        i = 1
        for log in logs:
            print(C + "{}".format(i) + W + " - " + G + log + W)
            try:
                commit_hash, commit_message = tuple(log.split(' ', 1))
            except ValueError:
                print(R + "Cannot find Commit " + W)
            log_list[i] = commit_hash
            i += 1
        print("\nPlease specify a number(s) to run. (eg. 2 or 2,3,4 or 3-9 etc.) ?")
        try:
            if sys.version_info >= (3, 0):
                jobs = input()
            else:
                jobs = raw_input()
        except KeyboardInterrupt:
            print(R + "USER CANCELED" + W)
            sys.exit(1)
        pattern = re.compile("(^([0-9]+?-[0-9]+?)|^[0-9]+?)((,[0-9]+?-[0-9]+?)|(,[0-9]+?))*$")

        if not pattern.match(jobs):
            print("The specified no(s) {0} are not in valid format. Valid format is 1-5,6,7,8-11.\n".format(jobs))
            sys.exit(100)
        jobsToRun = jobs.split(',')
        hashs = []
        for job in jobsToRun:
            if job.find('-') != -1:
                i, j = job.split('-')
                i = int(i)
                j = int(j)
                while i <= j:
                    hashs.append(log_list.get(i))
                    i += 1
            else:
                hashs.append(log_list.get(int(job)))
    else:
        hashs = list(set(hashs))
    print(G + "Fetching details...." + W)
    # For each commit hash
    hashCount = 1
    for hash in hashs:
        print(G + "{}".format(hashCount) + " " + "{}".format(hash) + W)
        hashCount += 1
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

        # Get full commit hash and commit message, used branch name to get log from any branch
        # regardless of whether current branch has the commit or not
        commit_hash_and_message_cmd = "git log {}".format(branch_list[0]) + " --pretty=oneline | grep {}".format(hash)
        pipe = subprocess.Popen(commit_hash_and_message_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = pipe.communicate()

        commit = str(out, encoding="utf_8").split(' ', 1)
        try:
            commit_hash, commit_message = tuple(commit)
        except ValueError:
            print(R + "Cannot find Commit ".format(hash) + W)
            continue
        commit_messages = commit_message.split(" -")
        once = True
        for msg in commit_messages:
            if msg.startswith("#") and once:
                once = False
            else:
                commit_message_array["Descriptions"].append(msg)
            deermine_list = deermine_pattern.findall(msg)
            for dm in deermine_list:
                commit_message_array["Deermines"].append(dm)
        # add commit_hash:branches
        branch_branches[commit_hash] = branches
    # Removing duplicates from Deermines
    commit_message_array["Deermines"] = list(set(commit_message_array["Deermines"]))
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

        # Commit Hash
        out_file.write(
            "<div>DasScrub Code CheckIn (" + account.title() + " " + client.title() + ")</div>")
        out_file.write("<div><br></div>")
        # Deermine
        if commit_message_array["Deermines"]:
            out_file.write(
                "<div><strong>Deermines:</strong>&nbsp;</div><ul>")
            for dm in commit_message_array["Deermines"]:
                out_file.write(
                    "<li><a href=\"https://svn.deerwalk.com/issues/" + dm.replace("#", "") + "\" target=\"_blank\">" +
                    dm + "</a></li>")
            out_file.write("</ul><br/>")

        # Description
        if commit_message_array["Descriptions"]:
            out_file.write(
                "<div><strong>Description:</strong>&nbsp;</div><ol>")
            for dm in commit_message_array["Descriptions"]:
                out_file.write(
                    "<li>" + dm + "</li>")
            out_file.write("</ol></br>")
        # Code/Unit Test Reviewed By
        out_file.write(
            "<div><b>Code/Unit Test Reviewed By:</b>&nbsp;{}</div>".format(
                reviewed_by))
        out_file.write("<div><br></div>")

        # Git Branch and Commits
        out_file.write(
            "<div><b>Git Hash & Commit:</b></div><ul>")
        for key, value in branch_branches.items():
            out_file.write("<li><b>{}</b>".format(key) + " - " + "{}</li>".format(value))
        out_file.write("</ul><div><br></div>")

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
