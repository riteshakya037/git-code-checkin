git-code-checkin
================

git-code-checkin is a Python script for automating Git code check-in e-mails. Currently, it works only with Python 3 on Linux. Soon, it will be cross-platform and support Python 2.

**Author:** Ashish Kayastha <kayastha.ashish@ymail.com>
**Modified:** Ritesh Shakya <riteshakya037@gmail.com>

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
1
-------------
    # Change to the Git repository directory.

    $ git log --oneline			        # Find out your commit hash
    $ git-code-checkin -c {<commit-hash>}	# Use the -c or --commit option and paste the commit hashs

    # Paste the HTML text in clipboard to your e-mail's 'Compose' window.

2
-------------
    # Change to the Git repository directory.
    
    $ git-code-checkin 

    # Paste the HTML text in clipboard to your e-mail's 'Compose' window.
    
Commit Syntax for best usage
-------------
1 Header Deermine
-------------
    {deermines}
    -description
    -description
    
    e.g.
    #84468,#84469,#84425
    -Fix multiple case of "Unknown" and "UNKNOWN" due to crosswalk
    -Duplication in record due removed by use of firstBy.
    -Hardcoded "Orphan_" in mbr_id, dw_member_id for Coventry Claims
    
2 Embedded Deermine
-------------
    -description #deermine description
    -description
    
    e.g.
    -Fix multiple case of "Unknown" and "UNKNOWN" due to crosswalk #84468
    -Duplication in record due removed by use of firstBy.

