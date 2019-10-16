import os
import sys
import json
import pkgutil
import inspect
import unittest
import HtmlTestRunner
import threading
from threading import Thread, active_count
from concurrencytest import ConcurrentTestSuite, fork_for_tests

sys.path.append(os.getcwd())
import testcases
from db.database import SqLiteDB


class TestRunner(SqLiteDB):
    def __init__(self):
        super().__init__()
        self.server_dict = {}

    def read_server_details_config(self):
        """
        :return:
        """
        fpath = os.path.join(os.getcwd(), "config", "server_details.json")
        if not fpath:
            self.logger.critical(f"Server details path not present: {fpath}")
            raise Exception(f"Server details path not presents: {fpath}")
        with open(fpath, "rb") as f_read:
            self.server_dict = json.loads(f_read.read())
        self.logger.info(f"Server details: {self.server_dict.items()}")
        for k, v in self.server_dict.items():
            return self.server_dict[k]
        return None

    def get_testcase_paths(self):
        """
        :return:
        """
        tpathlist = []
        tpath = os.path.join(os.getcwd(), "testcases")
        if not os.path.exists(tpath):
            self.logger.critical(f"Test case path not exists: {tpath}")
            raise Exception(f"Missing path: {tpath}")
        for root, dir, files in os.walk(tpath):
            for f in files:
                fpath = os.path.join(root, f)
                if os.path.isfile(fpath) and fpath.lower().endswith(".py"):
                    if fpath not in tpathlist:
                        tpathlist.append(fpath)
                    else:
                        self.logger.warning(f"Duplicate testcase found: {fpath}")
        return tpathlist

    def update_db_for_testcases(self):
        """
        :return:
        """
        tcfilepath = self.get_testcase_paths()
        for fpath in tcfilepath:
            with open(fpath) as f_read:
                lines = f_read.readlines()
                for line in lines:
                    if "test_id" in line:
                        tid = line.split("=")[-1].strip().strip('"')
                    if "test_name" in line:
                        tname = line.split("=")[-1].strip().strip('"')
                    if "server_type" in line:
                        stype = line.split("=")[-1].strip().strip('"')
                    if "test_flg" in line:
                        flg = line.split("=")[-1].strip().strip('"')
                if tid and tname and stype and flg:
                    self.insert_into_table(str(tid), str(tname), str(stype), int(flg))
                else:
                    self.logger.warning(f"Unable to add/update record for test case: {fpath}")

    def runner(self):
        """
        :return:
        """
        import subprocess
        testcasepath = self.get_testcase_paths()
        threads = []
        for filepath in testcasepath:
            t = Thread(target=subprocess.call(f"python {filepath}"))
            t.setName(filepath)
            t.start
            threads.append(t)
            print(threading.enumerate())
        for index, thread in enumerate(threads):
            print(index, thread.getName(), thread.join())

    def test_runner(self, testlist):
        """
        :param testlist:
        :return:
        """
        security_checks_packages = [testcases]
        packages = list(security_checks_packages)
        self.logger.info(f"Packages: {packages}")
        objSuite = unittest.TestSuite()
        for package in packages:
            self.logger.info(f"Packages name: {package.__name__}")
            self.logger.info(f"Package path: {package.__path__}")
            prefix = package.__name__ + "."
            for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
                module = __import__(modname, fromlist="dummy")
                for name, obj in inspect.getmembers(module):
                    self.logger.info(f"name:{name}, obj:{obj}")
                    if inspect.isclass(obj):
                        objSuite.addTest(obj("runTest"))
                        # objSuite.addTest(obj("runTest"))
                        # for testcase in testlist:
                        #     if obj.__name__.find(testcase) != -1:
                        #         objSuite.addTest(obj("runTest"))
        return objSuite

    def run(self, ):
        """
        :return:
        """
        # Create test runner.
        objTestRunner = self.test_runner(testlist=[])
        runner = HtmlTestRunner.HTMLTestRunner(output="report", report_name="automation_run",
                                               report_title="Test_automation_report",
                                               combine_reports=True, open_in_browser="Chrome", verbosity=2)
        # concurrent_suite = ConcurrentTestSuite(objTestRunner, fork_for_tests(10))
        # runner.run(concurrent_suite)
        runner.run(objTestRunner)


if __name__ == "__main__":
    obj = TestRunner()
    obj.update_db_for_testcases()
    # obj.runner()
