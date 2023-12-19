# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-19 11:33:45
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Log methods.
"""


from os.path import abspath as os_abspath
from reytool.rlog import RLog as RRLog

from .rreceive import RMessage
from .rwechat import RWeChat


__all__ = (
    "RLog",
)


class RLog(object):
    """
    Rey's `log` type.
    """


    # Logger.
    rrlog = RRLog("WeChat")


    def __init__(
        self,
        rwechat: RWeChat
    ) -> None:
        """
        Build `log` instance.

        Parameters
        ----------
        rwechat : `RClient` instance.
        """

        # Set attribute.
        self.rwechat = rwechat

        # Add handler.
        self.add_print()
        self.add_file()


    def add_print(self) -> None:
        """
        Add print handler.
        """

        # Add.
        self.rrlog.add_print()


    def add_file(self) -> None:
        """
        Add file handler.
        """

        # Set parameter.
        file_path = os_abspath("log\\WeChat")

        # Add.
        self.rrlog.add_file(file_path, time="m")


    def log_receive(self) -> None:
        """
        Add handler, log receive message.
        """


        # Define.
        def handler_log_receive(self, message: RMessage) -> None:
            """
            Log receive message.

            Parameters
            ----------
            message : `RMessage` instance.
            """

            # Generate text.
            text = "%19s | %20s | %-19s | %5s" % (
                message.id,
                message.room,
                message.sender,
                message.type
            )

            # Log.
            self(text)


        # Add handler.
        self.rwechat.rreceiver.add_handler(handler_log_receive)


    def log_all(self) -> None:
        """
        Log all.
        """

        # Log.
        self.log_receive()


    log = rrlog.log


    debug = rrlog.debug


    info = rrlog.info


    warning = rrlog.warning


    error = rrlog.error


    critical = rrlog.critical


    __call__ = log