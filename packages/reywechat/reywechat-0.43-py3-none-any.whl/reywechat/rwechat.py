# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-17 20:27:16
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : WeChat methods.
"""


from typing import Optional, Final
from os.path import abspath as os_abspath
from reytool.rdatabase import RDatabase as RRDatabase
from reytool.ros import create_folder as reytool_create_folder
from reytool.rtime import sleep


__all__ = (
    "RWeChat",
)


class RWeChat(object):
    """
    Rey's `WeChat` type.
    Only applicable to WeChat clients with version `3.9.5.81`.
    Will start client API service with port `19088` and message callback service with port '19089'.
    """

    # Environment.
    client_version: Final[str] = "3.9.5.81"
    client_api_port: Final[int] = 19088
    message_callback_port: Final[int] = 19089


    def __init__(
        self,
        rrdatabase: Optional[RRDatabase] = None,
        max_receiver: int = 2
    ) -> None:
        """
        Build `WeChat` instance.

        Parameters
        ----------
        max_receiver : Maximum number of receivers.
        """

        # Import.
        from .rclient import RClient
        from .rdatabase import RDatabase
        from .rlog import RLog
        from .rreceive import RReceiver

        # Create folder.
        self._create_folder()

        # Set attribute.

        ## Instance.
        self.rclient = RClient(self)
        self.rlog = RLog(self)
        self.rreceiver = RReceiver(self, max_receiver)
        if rrdatabase is not None:
            self.rdatabase = RDatabase(self, rrdatabase)

        ## Log.
        self.log_all = self.rlog.log_all
        self.log_receive = self.rlog.log_receive

        ## Receive.
        self.receive_add_handler = self.rreceiver.add_handler
        self.receive_start = self.rreceiver.start
        self.receive_stop = self.rreceiver.stop

        ## Database.
        if rrdatabase is not None:
            self.database_all = self.rdatabase.use_all
            self.database_use_message_receive = self.rdatabase.use_message_receive


    def _create_folder(self) -> None:
        """
        Create project standard folders.
        """

        # Set parameter.
        paths = [
            "log",
            "file"
        ]

        # Create.
        reytool_create_folder(*paths)

        # Set attribute.
        self.log_dir = os_abspath("log")
        self.file_dir = os_abspath("file")


    def all(self) -> None:
        """
        Start all function.
        """

        # Start.
        self.log_all()
        self.database_all()
        self.receive_start()


    def keep(self) -> None:
        """
        Blocking the main thread to keep running.
        """

        # Report.
        print("Keep runing.")

        # Blocking.
        while True:
            sleep(1)