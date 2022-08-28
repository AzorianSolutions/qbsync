from loguru import logger
from src.qbsync.app import QBSyncApp


class QBSyncCommands:
    app: QBSyncApp
    line_width: int = 80
    min_line_width: int = 40
    tables: dict = {
        'users': {
            '_order': ['user', 'pass_hash'],
            '_column_separator': '|',
            'user': {
                'label': 'Username',
                'min_width': 30,
                'padding': 1,
            },
            'pass_hash': {
                'label': 'Password Hash',
                'min_width': 4,
                'padding': 1,
            }
        }
    }

    @staticmethod
    def _get_width() -> int:
        import os
        return max(QBSyncCommands.min_line_width, os.get_terminal_size().columns)

    @staticmethod
    def _print_separator(length: int or None = None, character: str = '-'):
        if not isinstance(length, int) or not length:
            length = QBSyncCommands._get_width()
        print(character * length)

    @staticmethod
    def _print_header(title: str or None):
        QBSyncCommands._print_separator()
        if isinstance(title, str) and len(title.strip()):
            print(f' {title}')
            QBSyncCommands._print_separator()

    @staticmethod
    def _print_table_header(table: str):
        if table not in QBSyncCommands.tables:
            return

        line: str = ''

        for col in QBSyncCommands.tables[table]['_order']:
            if col[0] == '_':
                continue

            if len(line.strip()):
                line += QBSyncCommands.tables[table]['_column_separator']

            conf = QBSyncCommands.tables[table][col]

            # Insert the proper left side padding into the line if any
            if 'left_padding' in conf and isinstance(conf['left_padding'], int) and conf['left_padding']:
                line += ' ' * conf['left_padding']
            elif 'padding' in conf and isinstance(conf['padding'], int) and conf['padding']:
                line += ' ' * conf['padding']

            # Determine the minimum width for this column
            min_width: int = 0
            if 'min_width' in conf and isinstance(conf['min_width'], int) and conf['min_width']:
                min_width = conf['min_width']

            # Insert the column label into the line if provided and not empty or whitespace
            if 'label' in conf and isinstance(conf['label'], str) and len(conf['label'].strip()):
                line += conf['label'].ljust(min_width)
            else:
                line += ''.ljust(min_width)

            # Insert the proper right side padding into the line if any
            if 'right_padding' in conf and isinstance(conf['right_padding'], int) and conf['right_padding']:
                line += ' ' * conf['right_padding']
            elif 'padding' in conf and isinstance(conf['padding'], int) and conf['padding']:
                line += ' ' * conf['padding']

        print(line)

        QBSyncCommands._print_separator()

    @staticmethod
    def _print_table_row(table: str, row: dict, line_number: int or None = None):
        if table not in QBSyncCommands.tables:
            return

        line: str = ''
        first: bool = True

        for col in QBSyncCommands.tables[table]['_order']:
            if col[0] == '_':
                continue

            conf = QBSyncCommands.tables[table][col]

            if first and isinstance(line_number, int):
                # Insert the proper left side padding into the line if any
                if 'left_padding' in conf and isinstance(conf['left_padding'], int) and conf['left_padding']:
                    line += ' ' * conf['left_padding']
                elif 'padding' in conf and isinstance(conf['padding'], int) and conf['padding']:
                    line += ' ' * conf['padding']

                # Insert the given line number if any
                line += f'{str(line_number)}.'

            if not first:
                line += QBSyncCommands.tables[table]['_column_separator']

            # Insert the proper left side padding into the line if any
            if 'left_padding' in conf and isinstance(conf['left_padding'], int) and conf['left_padding']:
                line += ' ' * conf['left_padding']
            elif 'padding' in conf and isinstance(conf['padding'], int) and conf['padding']:
                line += ' ' * conf['padding']

            # Determine the minimum width for this column
            min_width: int = 0
            if 'min_width' in conf and isinstance(conf['min_width'], int) and conf['min_width']:
                min_width = conf['min_width']

            # Insert the column row value into the line if provided and not empty or whitespace
            if col in row and isinstance(row[col], str) and len(row[col].strip()):
                line += row[col].ljust(min_width)
            else:
                line += ''.ljust(min_width)

            # Insert the proper right side padding into the line if any
            if 'right_padding' in conf and isinstance(conf['right_padding'], int) and conf['right_padding']:
                line += ' ' * conf['right_padding']
            elif 'padding' in conf and isinstance(conf['padding'], int) and conf['padding']:
                line += ' ' * conf['padding']

            first = False

        print(line)

    @staticmethod
    def _clear_screen(print_header: bool = False, title: str = None):
        import os
        logger.info(f'Clearing terminal.')
        os.system('cls' if os.name == 'nt' else 'clear')
        if print_header:
            QBSyncCommands._print_header(title=title)

    @staticmethod
    def list_users():
        logger.info(f'Executing list_users command.')
        QBSyncCommands._clear_screen(print_header=True, title='QBSync Users')
        QBSyncCommands._print_table_header(table='users')

        if not isinstance(QBSyncCommands.app.users, dict) or not len(QBSyncCommands.app.users.items()):
            print(' There are currently no users in the users YAML file.')

        if isinstance(QBSyncCommands.app.users, dict):
            for user, pass_hash in QBSyncCommands.app.users.items():
                QBSyncCommands._print_table_row(table='users', row={'user': user, 'pass_hash': pass_hash})

        QBSyncCommands._print_separator()

    @staticmethod
    def add_user(error: str or None = None, username: str or None = None):
        import hashlib
        from getpass import getpass
        logger.info(f'Executing add_user command.')
        QBSyncCommands._clear_screen(print_header=True, title='QBSync Add User')
        print()

        if isinstance(error, str) and len(error.strip()):
            print(f' {error}')
            print()

        if isinstance(username, str) and len(username.strip()):
            print(f' Please enter the desired username: {username.strip()}')
        else:
            print(' Please enter the desired username: ', end='')
            username = input()
            username = str(username).strip()

        if isinstance(QBSyncCommands.app.users, dict) and len(username) and username in QBSyncCommands.app.users:
            return QBSyncCommands.add_user(f'The username {username} is already in use. Please choose something '
                                           + 'different.')

        print()
        password = getpass(' Please enter the desired password: ')
        print()

        password_confirm = getpass(' Please re-enter the desired password again: ')

        if password != password_confirm:
            return QBSyncCommands.add_user(f'The passwords entered did not match. Please try again.', username=username)

        print()

        print(f'Adding user {username} to QBSync users YAML file.')

        if not isinstance(QBSyncCommands.app.users, dict):
            QBSyncCommands.app.users = {}

        # Store the new user credentials to the users dictionary
        salt = QBSyncCommands.app.config['defaults']['auth']['salt']
        iterations = QBSyncCommands.app.config['defaults']['auth']['iterations']
        digest = hashlib.pbkdf2_hmac('sha256', password.encode(), str(salt).encode(), iterations)
        QBSyncCommands.app.users[username] = digest.hex()
        QBSyncCommands.app.save_yaml(prop_name='users')

    @staticmethod
    def remove_user(error: str or None = None):
        logger.info(f'Executing remove_user command.')
        QBSyncCommands._clear_screen(print_header=True, title='QBSync Users')

        left_padding: int = 0
        left_padding_default: int or None = None

        if isinstance(QBSyncCommands.app.users, dict):
            left_padding = len(str(len(QBSyncCommands.app.users.items()))) + 2

        if isinstance(left_padding, int) and left_padding:
            if 'left_padding' in QBSyncCommands.tables['users']['user']:
                left_padding_default = QBSyncCommands.tables['users']['user']['left_padding']

            elif 'padding' in QBSyncCommands.tables['users']['user']:
                left_padding_default = QBSyncCommands.tables['users']['user']['padding']

            if isinstance(left_padding_default, int) and left_padding_default:
                left_padding += left_padding_default

            QBSyncCommands.tables['users']['user']['left_padding'] = left_padding

        QBSyncCommands._print_table_header(table='users')

        if isinstance(left_padding_default, int):
            QBSyncCommands.tables['users']['user']['left_padding'] = left_padding_default
        else:
            del QBSyncCommands.tables['users']['user']['left_padding']

        if not isinstance(QBSyncCommands.app.users, dict) or not len(QBSyncCommands.app.users.items()):
            print(' There are currently no users in the users YAML file.')

        index: int = 0
        user_map: dict = {}
        if isinstance(QBSyncCommands.app.users, dict):
            for user, pass_hash in QBSyncCommands.app.users.items():
                index += 1
                user_map[index] = user
                QBSyncCommands._print_table_row(table='users', row={'user': user, 'pass_hash': pass_hash},
                                                line_number=index)

        QBSyncCommands._print_separator()

        if isinstance(error, str) and len(error.strip()):
            print()
            print(f' {error}')

        print()
        print(' Please enter the corresponding user number you would like to remove: ', end='')

        user_index = input()

        if not user_index.isnumeric() or int(user_index) > index or not int(user_index):
            return QBSyncCommands.remove_user(f'The given user number {user_index} is not valid. Please try again.')

        user = user_map[int(user_index)]

        print()
        print(f' Are you sure you want to remove the user {user} from the users YAML file? Enter "yes" to confirm. ', end='')

        confirm = input()

        if confirm.strip().lower() == 'yes':
            del QBSyncCommands.app.users[user]
            QBSyncCommands.app.save_yaml(prop_name='users')
            print()
            print(f' Removed the user {user} from users YAML file.')
            print()
        else:
            print()
            print(f' You failed to properly confirm the removal of the user {user}. Please try again.')
            print()
