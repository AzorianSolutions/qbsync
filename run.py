#!/usr/bin/env python
import argparse
import os
import src.qbsync.app
from src.qbsync.app import QBSyncApp
from src.qbsync.commands import QBSyncCommands


if __name__ == '__main__':
    # Set up CLI argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', help='QBSync YAML app config file to load', default='./config.yaml')
    args = parser.parse_args()

    # Set up the application instance
    src.qbsync.app.app = QBSyncApp(os.path.dirname(os.path.realpath(__file__)), args)
    QBSyncCommands.app = src.qbsync.app.app

    # Start the application
    src.qbsync.app.app.run()
