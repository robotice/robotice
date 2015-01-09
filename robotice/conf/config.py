#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Routines for configuring Robotice
"""
import logging
import os

from oslo.config import cfg

robotice_group = cfg.OptGroup('robotice')
robotice_opts = [
    cfg.StrOpt('flavor',
               help=("The flavor to use.")),
    cfg.StrOpt('robotice_config', default="/srv/robotice/conf/robotice.ini",
               help=("The Robotice paste config file to use."))]

monitor_group = cfg.OptGroup('monitor')
monitor_opts = [
    cfg.StrOpt('flavor',
               help=("The flavor to use.")),
    cfg.StrOpt('api_paste_config', default="api-paste.ini",
               help=("The API paste config file to use."))]

def list_opts():
    yield monitor_group.name, monitor_opts
    yield robotice_group.name, robotice_opts

cfg.CONF.register_group(robotice_group)
cfg.CONF.register_group(monitor_group)

for group, opts in list_opts():
    cfg.CONF.register_opts(opts, group=group)


def _get_deployment_config_file():
    """
    Retrieve the deployment_config_file config item, formatted as an
    absolute pathname.
    """
    config_path = cfg.CONF.find_file(
        cfg.CONF.robotice['robotice_config'])
    if config_path is None:
        return None

    return os.path.abspath(config_path)


def load_paste_app(app_name=None):
    """

    :raises RuntimeError when config file cannot be located or application
            cannot be loaded from config file
    """
    if app_name is None:
        app_name = cfg.CONF.prog

    conf_file = _get_deployment_config_file()
    if conf_file is None:
        raise RuntimeError(("Unable to locate config file"))

    try:
        app = None #deploy_app(conf_file, app_name, cfg.CONF)

        # Log the options used when starting if we're in debug mode...
        if cfg.CONF.debug:
            cfg.CONF.log_opt_values(logging.getLogger(app_name),
                                    sys_logging.DEBUG)

        return app
    except (LookupError, ImportError) as e:
        raise RuntimeError(("Unable to load %(app_name)s from "
                             "configuration file %(conf_file)s."
                             "\nGot: %(e)r") % {'app_name': app_name,
                                                'conf_file': conf_file,
                                                'e': e})
