from pyats import aetest
import logging
from unicon.core.errors import ConnectionError
from distutils.version import LooseVersion

logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):

    # Checking testbed info
    @aetest.subsection
    def check_testbed(self, testbed):

        if len(testbed.devices) == 0:
            self.failed('{testbed} is empty'.format(testbed=str(testbed)))

        else:
            # Listing the devices
            logger.info('List of Devices:')
            for device in testbed.devices:
                logger.info(f'  - {device}')

    @aetest.subsection
    def connect_to_devices(self, testbed):

        logger.info("Verifying that I can connect to each device.")

        for device in testbed:

            # Tracking each device.test_result
            device.test_results = {}

            # Try if I can connect to the device.
            try:
                device.connect(init_exec_commands=[],
                               init_config_commands=[],
                               log_stdout=False)
            except ConnectionError as e:
                self.failed(f"Could not connect to device {device.name}.")


class PingTestcase(aetest.Testcase):

    @aetest.test.loop(destination=('10.58.244.63', '10.58.244.23'))
    def ping(self, testbed, destination):
        for device in testbed:
            result = device.parse(f"ping {destination}")
            ping = result.get("ping", {})
            statistics = ping.get("statistics", {})
            success_rate = statistics.get("success_rate_percent", 0)
        if success_rate < 95:
            self.failed(f"device {device.name} ping {destination} rate : {success_rate}.")


class CheckVersionTestCase(aetest.Testcase):
    @aetest.test
    def check_version(self, testbed, check_os_version):
        target_version = LooseVersion(check_os_version)
        logger.info(f'Check os version, target version : {target_version}')
        has_errors = False
        errors_txt = ""
        for device in testbed:
            result = device.parse(f"show version")
            software_version = result.get("software_version", None)

            if software_version:
                current_version = LooseVersion(software_version)
                if current_version != target_version:
                    has_errors = True
                    errors_txt += f"{device.name} current version {current_version} does not match {target_version}.\n"
            else:
                self.failed(f"failed to get version from show version on  {device.name}.")
        if has_errors:
            errors_txt = errors_txt.strip()
            self.failed(errors_txt)



class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        for device in testbed:

            # Only disconnect if we are connected to the device
            if device.is_connected():
                device.disconnect()



if __name__ == '__main__':
    # local imports
    from genie.testbed import load
    import argparse
    import sys
    import time

    # set debug level DEBUG, INFO, WARNING
    logger.setLevel(logging.INFO)

    # Getting the current_time before the test
    t = time.localtime()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

    # Parsing the args
    parser = argparse.ArgumentParser(description='Process the testbed.')
    parser.add_argument('--testbed', dest='testbed', help='/link/to/testbed.yaml', required=True)
    parser.add_argument("--check_os_version", dest='check_os_version', help='os version to check', required=True)
    args, sys.argv[1:] = parser.parse_known_args(sys.argv[1:])

    testbed = load(args.testbed)

    # List of tests_run
    testbed.tests_run = []

    aetest.main(testbed=testbed, current_time=current_time, check_os_version=args.check_os_version)

    # Adding two blank lines for formatting
    logger.info("")
    logger.info("")
