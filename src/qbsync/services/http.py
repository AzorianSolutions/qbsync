from flask import Flask, render_template, render_template_string
from flask_spyne.flask_spyne import Spyne
from spnexus.utils.paths import PathsUtil
from src.qbsync.app import app as qbsync_app

tpl_path = qbsync_app.config['defaults']['templates']['path']
tpl_path = PathsUtil.remove_leading_slash(PathsUtil.remove_trailing_slash(tpl_path))
app: Flask = Flask(__name__, static_url_path='', template_folder=f'{qbsync_app.path}/{tpl_path}')
spyne: Spyne = Spyne(app)


def make_server() -> Flask:
    return app


def get_app_conf() -> dict:
    return qbsync_app.config['defaults']['app']


def get_users() -> list or None:
    from src.qbsync.app import app
    if not isinstance(app.users, dict):
        return []
    return list(app.users.keys())


@app.route('/')
def main():
    return render_template(f'gui.html', app=get_app_conf(), users=get_users())


@app.route('/static/<path:path>')
def send_static(path):
    from flask import send_from_directory
    return send_from_directory('static', path)


@app.route('/qbwc/download-customers')
def download_customers():
    qbsync_app.requests.put({'job': 'download_customers'})
    return render_template(f'gui.html', app=get_app_conf(), users=get_users(),
                           data="Queued customers download request.")


@app.route('/qbwc/download-invoices')
def download_invoices():
    qbsync_app.requests.put({'job': 'download_invoices'})
    return render_template(f'gui.html', app=get_app_conf(), users=get_users(),
                           data="Queued invoices download request.")


@app.route('/qbwc/download-all')
def download_all():
    qbsync_app.requests.put({'job': 'download_all'})
    return render_template(f'gui.html', app=get_app_conf(), users=get_users(),
                           data="Queued full download request.")


@app.route('/qbwc/download-qwc/<string:user>')
def download_qwc(user: str):
    import os
    import uuid
    from flask import send_file
    from io import BytesIO
    from src.qbsync.app import app

    conf = app.config['defaults']
    error_tpl_path = conf['templates']['error']
    qwc_path = f"{app.path}/{tpl_path}/{conf['templates']['qbwc']}"
    error: str or None = None

    if not os.path.exists(qwc_path):
        error = f'The configured QBWC template path does not exist at {qwc_path}.'

    if error is None and not os.access(qwc_path, os.R_OK):
        error = f'The configured QBWC template path is not readable at {qwc_path}.'

    if error is None and not isinstance(user, str) or not len(user.strip()):
        error = f'The given value for the user parameter is not valid: {user}'

    if error is None and user not in app.users:
        error = f'The given user {user} does not exist in the users YAML file.'

    if isinstance(error, str):
        return render_template(error_tpl_path, data=error)

    tpl_data: dict = {**{
        'user': user,
        'owner_id': uuid.uuid4(),
        'file_id': uuid.uuid4(),
    }, **conf['app']}

    with open(qwc_path, 'r') as f:
        tpl = f.read()
        f.close()

    tpl = render_template_string(tpl, data=tpl_data)

    return send_file(BytesIO(bytes(tpl.encode())), mimetype='application/xml', as_attachment=True,
                     download_name=f"{conf['app']['name']}.qwc", max_age=0)


if __name__ == '__main__':
    conf = qbsync_app.config['defaults']['servers']['http']
    app.run(host=conf['host'], port=conf['port'], debug=conf['debug'])
