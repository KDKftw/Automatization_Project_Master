from starter_master_browserstack import runner_tests_generalized
from ET_Automation_Local_Deploy_PyCharm.starter_local import suite_ET_full

brand_name = "ETRAVEL"

desired_cap = {
"os" : "Windows",
"os_version" : "11",
"browser" : "Edge",
"browser_version" : "latest",
"resolution" : "1680x1050",
"project" : brand_name,
"build" : "buid",
"name" : "name",
"browserstack.local" : "false",
"browserstack.debug" : "true",
"browserstack.networkLogs" : "true",
"browserstack.selenium_version" : "3.5.2"
}
def setUp(self):
  self.driver = webdriver.Remote(
      command_executor=comandExecutor,
      desired_capabilities=desired_cap)
#while True:
runner_tests_generalized(suite_ET_full, brand_name)