# QBSync by [Azorian Solutions](https://azorian.solutions)

## Admin CLI

I have provided a very basic interactive CLI tool to list, add, and remove users from the QBSync users YAML file. This
is currently the best way to manager users as passwords are **not** stored in plaintext so there is an involved
process to salt and hash the password before storing it in the users YAML file.

To get started with the admin tool, execute the following command;

    cd {PROJECT_ROOT}

### List Users

    ./admin.py -x list_users

### Add User

    ./admin.py -x add_user

### Remove User

    ./admin.py -x remove_user
