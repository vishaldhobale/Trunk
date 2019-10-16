# /var/lib/env python
import os
import sys
import logging

sys.path.append(os.getcwd())


class SampleLogger:
    def __init__(self, logging_level=None, logging_file=None):
        self.logger = None
        self.ch = None
        self.formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(module)s] [%(lineno)s] '
                                           '[%(message)s]')
        self.log_file = logging_file if logging_file else os.path.join(os.getcwd(), "logs\\testcaserun.log")
        self.logging_level = logging_level if logging_level else logging.DEBUG
        self.create_logger()

    def create_logger(self):
        """
        # create logger
        :return:
        """
        self.logger = logging.getLogger()
        self.logger.setLevel(self.logging_level)
        self.set_streamhandler()
        self.set_filehandler()

    def set_streamhandler(self):
        """
        # create console handler and set level to debug
        :return:
        """
        ch = logging.StreamHandler()
        ch.setLevel(self.logging_level)
        # add formatter to ch
        ch.setFormatter(self.formatter)
        # add ch to logger
        self.logger.addHandler(ch)

    def set_filehandler(self):
        """
        :return:
        """
        fh = logging.FileHandler(self.log_file, mode='a', encoding=None, delay=False)
        fh.setLevel(self.logging_level)
        # add formatter to ch
        fh.setFormatter(self.formatter)
        # add fh to logger
        self.logger.addHandler(fh)


if __name__ == "__main__":
    l = SampleLogger()
    l.logger.info("hi")
