# Example
# -------
#
#   a simple, sequential job file

import os

from pyats.easypy import run


# main() function must be defined in each job file
#   - it should have a runtime argument
#   - and contains one or more tasks
def main(runtime):
    # provide custom job name for reporting purposes (optional)
    runtime.job.name = 'pyats presentation'

    # using run() api to run a task
    #
    # syntax
    # ------
    #   run(testscript = <testscript path/file>,
    #       runtime = <runtime object>,
    #       max_runtime = None,
    #       taskid = None,
    #       **kwargs)
    #
    #   any additional arguments (**kwargs) to run() api are propagated
    # *  to AEtest as input arguments.
    run(testscript='demo/pre_check.py', runtime=runtime, check_os_version="7.4.1")

