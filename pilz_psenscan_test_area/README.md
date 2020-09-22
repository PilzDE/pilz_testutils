# PSENscan test area scripts
This folder contains all scripts handling the automatic test execution at the PSENscan test area.

## Installation
1. Set the global environment variable TEST_AREA_SCRIPTS_PATH.

    ```
    export TEST_AREA_SCRIPTS_PATH="/usr/local/bin/laser_scan_test_scripts"
    ```

    to add it permanently create a file in `/etc/profile.d/`

    > The PSENscan test area pc has a test_environment.sh file for this purpose.

2. Create the TEST_AREA_SCRIPTS_PATH folder and copy the scripts in it.
3. Create a .desktop file in `/etc/xdg/autostart/` with following content:
    ```
    [Desktop Entry]
    Type=Application
    Name=AutomaticAcceptanceTestPSENscan
    Terminal=true
    Exec=bash -c "sleep 1; $TEST_AREA_SCRIPTS_PATH/automatic_acceptance_test_psen_scan.sh 'feature/acceptance_test_publish_test'; echo 'Press ENTER to exit ...'; read"

    ```
4. Create the folder `/var/log/automatic_acceptance_test`
5. Change the folder group to test
    ```
        addgroup test
        chgrp test `/var/log/automatic_acceptance_test`
    ```
    > All users have to be add to this group. \
    > `usermod -a -G test USER`

## Options
The main script (`automatic_acceptance_test_psen_scan.sh`) can be launched with one optional parameter. This parameter changes the target checkout 
> default: `melodic-devel`