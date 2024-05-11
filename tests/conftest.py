import os
from time import sleep
from unittest import mock

import pytest
import roslaunch as rl
from roslaunch import parent as rlparent, rlutil


@pytest.fixture
def roslaunch(request: pytest.FixtureRequest):
    args = request.param

    uuid = rlutil.get_or_generate_uuid(options_runid=None, options_wait_for_master=False)
    rl.configure_logging(uuid)
    roslaunch_files = rlutil.resolve_launch_arguments(args)
    launch = rlparent.ROSLaunchParent(uuid, roslaunch_files, is_core=True)
    launch.start()

    sleep(0.5)

    with mock.patch.dict(os.environ, {"ROS_VERSION": "3"}):
        yield

    launch.shutdown()
