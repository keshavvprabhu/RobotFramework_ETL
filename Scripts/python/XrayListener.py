# import section
from robot.libraries.BuiltIn import  BuiltIn
import os
import codecs
import logging
import requests
import requests.packages.urllib3
import datetime
from configparser import ConfigParser, ExtendedInterpolation
requests.packages.urllib3.disable_warnings()

# Author Section
# Program Name: XrayListener.py                                     
# Created by Keshav at 20/05/22 11:05 p.m.                       


# Write your code here
def create_logger():
    """
    Creates a logger for internal use
    Returns:

    """
    currdate = datetime.datetime.now().strftime("%Y%m%d")
    log_name = "{}_{}.log".format(os.path.basename(__file__).rsplit(".")[0], currdate)
    global logger
    logger = logging.getLogger(__name__)
    current_working_dir = os.getcwd()
    logger.setLevel(logging.INFO)
    logger_folder_path = os.path.join(current_working_dir, "Scripts/log")
    logger_folder_path = os.path.abspath(logger_folder_path)
    if not os.path.exists(logger_folder_path):
        os.makedirs(logger_folder_path)
    log_file_path = os.path.join(logger_folder_path, log_name)
    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class XRayListener:
    ROBOT_LISTENER_API_VERSION = 3
    create_logger()

    def __init__(self):
        pass

    def get_all_variables(self):
        """
        Gets all the RobotFramework CommandLine variables as a dictionary
        Returns: dictionary of commandline variables

        """
        self._variables = dict(BuiltIn().get_variables())
        logger.info("Commandlind Variables: {}".format(self._variables))
        return self._variables

    @staticmethod
    def read_config_values():
        """
        Reads XrayListener.ini configuration file and gets teh mandatory variables required to
        synchronize RobotFramework Test Execution with XRay JIRA Server instance
        Returns: dict_config_variables

        """
        my_name = "read_config_values()"
        logger.info("Entered: {}".format(my_name))
        current_working_directory = os.getcwd()
        config_file_path = r"{}/Scripts/python/XrayListener.ini".format(current_working_directory)
        config_file_path = os.path.abspath(config_file_path)
        if not os.path.exists(config_file_path):
            logger.error("File Not Found: {}".format(config_file_path))
            raise SystemExit("Mandatory values not provided to the Listener")

        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(config_file_path, encoding='utf-8')
        logger.info("Reading configutation values from file: {}".format(config_file_path))
        logger.info("Xray Host: {}".format(config["XRAY"].get("XRAY_HOST")))
        logger.info("Project Key: {}".format(config["XRAY"].get("PROJECT_KEY")))
        logger.info("XRay Auth Key: {}".format(config["XRAY"].get("XRAY_AUTH_KEY")))
        logger.info("Component: {}".format(config["XRAY"].get("COMPONENT", None)))
        logger.info("FixVersion: {}".format(config["XRAY"].get("FIX_VERSION", None)))
        logger.info("Sprint: {}".format(config["XRAY"].get("SPRINT")))
        dict_config_variables = dict()
        dict_config_variables["${PROJECT_KEY}"] = config["XRAY"].get("PROJECT_KEY")
        dict_config_variables["${XRAY_HOST}"] = config["XRAY"].get("XRAY_HOST")
        dict_config_variables["${XRAY_AUTH_KEY}"] = config["XRAY"].get("XRAY_AUTH_KEY")
        dict_config_variables["${COMPONENT}"] = config["XRAY"].get("COMPONENT", None)
        dict_config_variables["${FIX_VERSION}"] = config["XRAY"].get("FIX_VERSION", None)
        dict_config_variables["${SPRINT}"] = config["XRAY"].get("SPRINT", None)
        logger.info("Completed: {}".format(my_name))
        return dict_config_variables

    def start_suite(self, name, attrs):
        """
        This event will be fired when RobotFramework Test Suite Commences
        Args:
            name:
            attrs:

        Returns:

        """
        logger.info("Entered: start_suite()")
        logger.info("Retrieve all Robotframework command line variable")
        self.get_all_variables()
        logger.info("Completed: start_suite()")

    def start_test(self, name, attrs):
        """
        This event will be fired when the Robot Framework Test Starts
        Args:
            name:
            attrs:

        Returns:

        """
        logger.info("Entered: start_test()")
        # do something here
        logger.info("Completed: start_test()")

    def end_test(self, name, attrs):
        """
        This event will be fired when the RobotFramework Test Finishes
        Args:
            name:
            attrs:

        Returns:

        """
        logger.info("Entered: end_test()")
        # do something here
        logger.info("Completed: end_test()")

    def end_suite(self, name, attrs):
        """
        This event will be fired when the RobotFramework Test Suite ends
        Args:
            name:
            attrs:

        Returns:

        """
        logger.info("Entered: end_suite()")
        # do something here
        logger.info("Completed: end_suite()")

    def close(self):
        """
        This event will run after the RobotFramework Execution has completed
        Returns:

        """
        dict_config_values = self.read_config_values()
        logger.info("Entered: close()")
        # Mandatory values - CHeck if it is provided as Runtime arguments, if not provided as Runtime arguments then
        # get it from XrayListener.ini. If the value cannot be found in both Runtime Arguments or XRayListener.ini
        # then exit with an error.
        logger.info("self._variables = {}".format(self._variables))
        try:
            self.project_key = self._variables.get("${PROJECT_KEY}", dict_config_values["${PROJECT_KEY}"])
            self.xray_host = self._variables.get("${XRAY_HOST}", dict_config_values["${XRAY_HOST}"])
            self.xray_auth_key = self._variables.get("${XRAY_AUTH_KEY}", dict_config_values["${XRAY_AUTH_KEY}"])
            self.test_plan_key = self._variables["${TEST_PLAN_KEY}"]

            self.fix_version = self._variables.get("${FIX_VERSION}", dict_config_values["${FIX_VERSION}"])
            self.component = self._variables.get("${COMPONENT}", dict_config_values["${COMPONENT}"])

            # Get the RobotFramework output.xml file
            self.output_xml_file_path = self._variables["${OUTPUT_FILE}"]
            os.path.abspath(self.output_xml_file_path)
            with codecs.open(self.output_xml_file_path, 'rb', encoding='utf-8') as fin:
                self.content = fin.read()

            self.files = {'file': ('output.xml', self.content)}

        except Exception as e:
            logger.error("XRAY_HOST, XRAY_AUTH_KEY, PROJECT_KEY, TEST_PLAN_KEY need to be provided")
            raise SystemExit("Mandatory Values are not provided to the XrayListener. Check log file for error")

        # Get the Robotframework log.html file
        self.log_file_path = self._variables.get("${LOG_FILE}", None)
        os.path.abspath(self.log_file_path)
        logger.info("Here is the log file path: {}".format(self.log_file_path))
        with codecs.open(self.log_file_path, encoding='utf-8') as flog:
            self.log_content = flog.read()

        self.log_file = {'file': ('log.html', self.log_content)}

        # Get the RobotFramework report.html file
        self.report_file_path = self._variables.get("${REPORT_FILE}", None)
        os.path.abspath(self.report_file_path)
        logger.info("Here is the log file path: {}".format(self.report_file_path))
        with codecs.open(self.report_file_path, encoding='utf-8') as frep:
            self.report_content = frep.read()

        self.report_file = {'file': ('report.html', self.report_content)}

        # Get the RobotFramework Environment variables
        self.set_test_environment = set()
        self.list_test_environment = list()
        self.test_environment = self._variables.get("${ENV}", None)
        self.set_test_environment.add(self.test_environment)

        # This is useful when we do a cross-environment comparison
        self.test_source_environment = self._variables.get("${SOURCE_ENV}", None)
        logger.info("SOURCE_ENV: {}".format(self.test_source_environment))
        self.test_target_environment = self._variables.get("${TARGET_ENV}", None)
        logger.info("TARGET_ENV: {}".format(self.test_target_environment))

        if self.test_source_environment and self.test_target_environment:
            self.test_cross_environment = f"{self.test_source_environment}_vs_{self.test_target_environment}"
            self.set_test_environment.add(self.test_cross_environment)
            self.list_test_environment = list(self.set_test_environment)

        self.list_test_environment = list(self.set_test_environment)

        if self.test_plan_key in ('', None, False):
            self.parameters = {'projectKey': self.project_key,
                               'testEnvironments': self.list_test_environment}
        else:
            self.parameters = {'projectKey': self.project_key,
                               'testPlanKey': self.test_plan_key,
                               'testEnvironments': self.list_test_environment}

        self.api_header = {'Authorization': 'Basic {}'.format(self.xray_auth_key)}

        self.xray_api_endpoint = "{}/rest/raven/1.0/import/execution/robot".format(self.xray_host)
        try:
            self.response = requests.post(self.xray_api_endpoint, params=self.parameters,
                                          headers=self.api_header, files=self.files, verify=False)

            if self.response.status_code == 200:
                logger.info("RobotFramework Test Excution Completed Successfully")
                self.response_json = self.response.json()

                # Test Execution JIRA
                self.test_execution_endpoint = self.response_json.get("testExecIssue", None).get("self")
                logger.info("Test Execution Issue: {}".format(self.test_execution_endpoint))

                # Test Issues List
                self.list_test_urls = list()

                try:
                    for item in self.response_json.get("testIssues").get('success'):
                        test_url = item.get('self')
                        self.list_test_urls.append(test_url)

                    logger.info("Test URL List: {}".format(self.list_test_urls))

                except Exception as e:
                    logger.error("Error: {}".format(e))

                for item in self.list_test_urls:
                    logger.info("Modifying the custom fields in the Test: {}".format(item))

                    self.data = { "fields": {"description": "The automated test was executed using RobotFramework."
                                                            "Please refer to the RobotFramework log.html and"
                                                            "report.html attached to the Test Execution JIRA",
                                             "customfield_10201": {"id": "11306"},
                                             "customfield_10304": [{"id": "11206"}, {"id": "11205"}],
                                             "customfield_10309": [{"id": "11217"}, {"id": "11218"}, {"id": "11219"}, {"id": "11226"}],
                                             "fixVersions": [{"name": self.fix_version}],
                                             "components": [{"name": self.component}],
                                             }}
                    try:
                        self.response = requests.put(item, headers=self.api_header, verify=False, json=self.data)
                        if self.response.status_code not in (200, 204):
                            logger.error("Modifying custom fields in Test JIRA Failed. "
                                         "Status Code: {}".format(self.response.status_code))
                            logger.error("Failure Response Content: {}".format(self.response.content))
                        else:
                            logger.info("Custom Field Update for Test: {} completed successfully".format(item))
                    except Exception as e:
                        logger.info("{} - {} -  {}".format(item, self.response.status_code, self.response.content))

                    # Transitioning the status to 'Ready for Use'
                    self.data = {'transition': {'id': '91'}}
                    try:
                        self.response = requests.post("{}/transitions".format(item),
                                                  headers=self.api_header,
                                                  verify=False,
                                                  json=self.data)
                        if self.response.status_code not in (200, 204):
                            logger.error("Status could not be set to - Ready for Use")
                        else:
                            logger.info("Status changed to - Ready for Use")
                    except Exception as e:
                        logger.error("Error while Changing Transition")
                        logger.error("{} - {} -  {}".format(item, self.response.status_code, self.response.content))

                # Now let us update the Test Execution JIRA issues
                logger.info("Attaching report.html to Test Execution JIRA")
                self.jira_attachments_endpoint = "{}/attachments".format(self.test_execution_endpoint)
                self.attachment_header = {'X-Atlassian-Token': 'no-check',
                                          'Authorization': 'Basic {}'.format(self.xray_auth_key)}
                try:
                    self.response = requests.post(self.jira_attachments_endpoint,
                                                  files=self.report_file,
                                                  verify=False,
                                                  headers=self.attachment_header)
                    if self.response.status_code in (200, 204):
                        logger.info("RobotFramework report.html successfully attached to Test Execution JIRA")
                    else:
                        logger.error("Failed to attach RobotFramework report.html to Test Execution JIRA")

                except Exception as e:
                    logger.error("Error while attaching report.html")
                    logger.error("{} - {} -  {}".format(item, self.response.status_code, self.response.content))

                logger.info("Attaching log.html to Test Execution JIRA")
                try:
                    self.response = requests.post(self.jira_attachments_endpoint,
                                                  files=self.log_file,
                                                  verify=False,
                                                  headers=self.attachment_header)
                    if self.response.status_code in (200, 204):
                        logger.info("RobotFramework log.html successfully attached to Test Execution JIRA")
                    else:
                        logger.error("Failed to attach RobotFramework log.html to Test Execution JIRA")
                except Exception as e:
                    logger.error("Error while attaching log.html")
                    logger.error("{} - {} -  {}".format(item, self.response.status_code, self.response.content))

                # Transitioning the Test Execution JIRA to DONE
                self.data = {'transition': {'id': '11'}}
                try:
                    self.response = requests.post("{}/transitions".format(self.test_execution_endpoint),
                                                  verify=False,
                                                  json=self.data,
                                                  headers=self.api_header,
                                                  )
                except Exception as e:
                    logger.error("Error while transitioning Test Execution JIRA")
                    logger.error("{} - {} -  {}".format(item, self.response.status_code, self.response.content))

                # Changing Custom fields for the Test Execution JIRA
                self.data = {'fields': { 'customfield_10228': {'id': '11401'},
                                         'fixVersions': [{'name': self.fix_version}],
                                         'components':[{'name':self.component}],
                                         }
                             }
                try:
                    self.response = requests.put(self.test_execution_endpoint,
                                                 headers=self.api_header,
                                                 json=self.data,
                                                 verify=False)
                    if self.response.code not in (200, 204):
                        logger.error("Error while updating customfields of Test Execution JIRA")
                    else:
                        logger.info("Custom Fields updated successfully for the TestExecution JIRA")
                except Exception as e:
                    logger.error("Error while updating Custom Fields of Test Execution JIRA")
                    logger.error("{} - {} -  {}".format(item, self.response.status_code, self.response.content))

                #Adding a comment to the Test Execution JIRA

                self.comment_message = "Changed Automated='Yes' and attached RobotFramework log.html and report.html." \
                                       "Changed the Status to DONE and aldo some additional custom fields " \
                                       "as deemed important."

                try:
                    self.response = requests.post("{}/comment".format(self.test_execution_endpoint),
                                                  headers=self.api_header,
                                                  verify=False,
                                                  json=self.data)

                    if self.response.status_code not in (200, 204):
                        logger.error("Adding Comment to the Test Execution Failed")
                    else:
                        logger.info("Comment added to the Test Execution JIRA")
                except Exception as e:
                    logger.error("Error while adding Comment to Test Execution JIRA")
                    logger.error("{} - {} -  {}".format(item, self.response.status_code, self.response.content))

            else:
                logger.error("RobotFramework Test Execution Import Failed")

        except Exception as e:
            logger.error("Something went wrong while importing RobotFramework Test Import into Xray")
            logger.info("{} - {} - {}".format(self.xray_api_endpoint, self.response.status_code, self.response.content))


if __name__ == '__main__':
    pass
