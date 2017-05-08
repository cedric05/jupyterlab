# coding: utf-8
"""A tornado based Jupyter lab server."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os

from jupyterlab_launcher import add_handlers, LabConfig

from .commands import APP_DIR, list_extensions
from ._version import __version__

#-----------------------------------------------------------------------------
# Module globals
#-----------------------------------------------------------------------------

DEV_NOTE_NPM = """You're running JupyterLab from source.
If you're working on the TypeScript sources of JupyterLab, try running

    npm run watch

from the JupyterLab repo directory in another terminal window to have the
system incrementally watch and build JupyterLab's TypeScript for you, as you
make changes.
"""


CORE_NOTE = """
Running the core application with no additional extensions or settings
"""


def load_jupyter_server_extension(nbapp):
    """Load the JupyterLab server extension.
    """
    # Print messages.
    here = os.path.dirname(__file__)
    nbapp.log.info('JupyterLab alpha preview extension loaded from %s' % here)

    app_dir = APP_DIR
    if hasattr(nbapp, 'app_dir'):
        app_dir = nbapp.app_dir or APP_DIR

    web_app = nbapp.web_app
    config = LabConfig()

    config.assets_dir = os.path.join(app_dir, 'static')
    config.settings_dir = os.path.join(app_dir, 'settings')
    config.page_title = 'JupyterLab Alpha Preview'
    config.name = 'JupyterLab'
    config.page_url = '/lab'
    config.version = __version__

    # Check for dev mode.
    dev_mode = ''
    if hasattr(nbapp, 'dev_mode'):
        dev_mode = nbapp.dev_mode

    if dev_mode:
        nbapp.log.info(DEV_NOTE_NPM)
        config.assets_dir = os.path.join(here, 'build')
        config.settings_dir = ''
        config.dev_mode = True

        add_handlers(web_app, config)
        return

    # Check for explicit core mode.
    core_mode = False
    if hasattr(nbapp, 'core_mode'):
        core_mode = nbapp.core_mode

    # Run core mode if explicit or there is no static dir and no
    # installed extensions.
    installed = list_extensions(app_dir)
    fallback = not installed and not os.path.exists(config.assets_dir)
    if core_mode or fallback:
        config.assets_dir = os.path.join(here, 'static', 'build')
        if not os.path.exists(config.assets_dir):
            msg = 'Static assets not built, please see CONTRIBUTING.md'
            nbapp.log.error(msg)
        else:
            nbapp.log.info(CORE_NOTE.strip())

    add_handlers(web_app, config)
