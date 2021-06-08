# Github Hardware Tests

## [Step 1.1] Local industrial_ci with real hardware (IN PROGRESS)
Got so far to ping the sensor in `AFTER_INIT` and only continue if there is something. If the sensor is bootet shortly before running industrial_ci maybe a later hook makes more sense since this would give the sensor more time to boot. The specification of `ADDITIONAL_DEBS` is needed to have `ping` available.

The mount in `DOCKER_RUN_OPTS` is needed for the custom ssl certificate that is needed. A PR on industrial_ci is opened [here](https://github.com/ros-industrial/industrial_ci/pull/671/files).

```
rosrun industrial_ci run_ci ROS_DISTRO=noetic ROS_REPO=main DOCKER_RUN_OPTS="-v /usr/local/share/ca-certificates:/usr/local/share/ca-certificates:ro" ADDITIONAL_DEBS="iputils-ping" AFTER_INIT="ping -c 1 192.168.0.100"
```

Next steps:
- Mount the relevant port (via `DOCKER_RUN_OPTS`?)
- Pass the `HARDWARE_TESTING_ENABLED` flag cmake
- Maybe split the publish test and start by trying to get this to work before continuing with the `hardware_compare` test

### [Step 1.2] Python execute CI without real hardware
see `run_ci.py`