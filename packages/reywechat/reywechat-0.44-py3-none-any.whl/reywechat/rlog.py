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


    @property
    def print_colour(self) -> bool:
        """
        Whether print colour.

        Returns
        -------
        Result.
        """

        # Get parameter.
        result = self.rrlog.print_colour

        return result


    @print_colour.setter
    def print_colour(self, value: bool) -> None:
        """
        Set whether print colour.

        Parameters
        ----------
        value : Set value.
        """

        # Set.
        self.rrlog.print_colour = value


    def add_print(self) -> None:
        """
        Add print handler.
        """

        # Set parameter.
        format_ = (
            "%(format_time)s | "
            "%(format_levelname)s | "
            "%(format_message)s"
        )

        # Add.
        self.rrlog.add_print(format_=format_)


    def add_file(self) -> None:
        """
        Add file handler.
        """

        # Set parameter.
        file_path = os_abspath("log\\WeChat")
        format_ = (
            "%(format_time)s | "
            "%(format_levelname)s | "
            "%(content_file)s"
        )

        # Add.
        self.rrlog.add_file(
            file_path,
            time="m",
            format_=format_
        )


    def log_receive(
        self,
        message: RMessage
    ) -> None:
        """
        Log receive message.

        Parameters
        ----------
        message : `RMessage` instance.
        """

        # Get parameter.
        if message.room is None:
            message_object = message.sender
        else:
            message_object = message.room
        content_print = "RECEIVE | %19s | %-20s | %5s" % (
            message.id,
            message_object,
            message.type
        )
        content_file = "RECEIVE | %s" % message.params

        # Log.
        self.log(
            content_print,
            content_file=content_file
        )


    log = rrlog.log


    debug = rrlog.debug


    info = rrlog.info


    warning = rrlog.warning


    error = rrlog.error


    critical = rrlog.critical


    __call__ = log