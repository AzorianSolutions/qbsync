#!/usr/bin/env python
import argparse
import os
import src.qbsync.app
from loguru import logger
from src.qbsync.app import QBSyncApp
from src.qbsync.commands import QBSyncCommands


if __name__ == '__main__':
    # Setup CLI argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', help='QBSync YAML app config file to load', default='./config.yaml')
    parser.add_argument('-x', '--command', help='QBSync admin command to execute.', required=True)
    args = parser.parse_args()

    # Set up the application instance
    src.qbsync.app.app = QBSyncApp(os.path.dirname(os.path.realpath(__file__)), args)
    QBSyncCommands.app = src.qbsync.app.app

    # Validate the command argument against defined commands in the QBSyncCommands class
    if not hasattr(QBSyncCommands, args.command) or not hasattr(getattr(QBSyncCommands, args.command), '__call__'):
        logger.critical(f'The command {args.command} is not valid!')

    # Execute command
    logger.debug(f'Executing command {args.command}.')
    getattr(QBSyncCommands, args.command)()
