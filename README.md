git-code-checkin
================

git-code-checkin is a Python script for automating Git code check-in e-mails. Currently, it works only with Python 3 on Linux. Soon, it will be cross-platform and support Python 2.

**Author:** Ashish Kayastha <kayastha.ashish@ymail.com>
**Forked:** Ritesh Shakya <riteshakya037@gmail.com>

Dependencies
------------
* Linux >= 2.6
* Python >= 3.0

Install
-------
    # Change to the extracted directory.

    $ sh install_git_code_checkin.sh

Example Usage
-------------
    # Change to the Git repository directory.

    $ git log --oneline			        # Find out your commit hash
    $ git-code-checkin -c {<commit-hash>}	# Use the -c or --commit option and paste the commit hashs

    # Paste the HTML text in clipboard to your e-mail's 'Compose' window.
