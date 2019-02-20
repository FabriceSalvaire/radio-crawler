####################################################################################################
#
# RadioCrawler - A Radio Playlist Crawler
# Copyright (C) 2019 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from pathlib import Path
import importlib.util as importlib_util
import logging

from . import DefaultConfig

####################################################################################################

class ConfigFile:

    _logger = logging.getLogger(__name__)

    ##############################################

    @classmethod
    def default_path(cls):
        return str(DefaultConfig.Path.join_config_directory('config.py'))

    ##############################################

    @classmethod
    def create(cls, args):

        template = '''
################################################################################
#
# Radio Crawler Configuration
#
################################################################################

import RadioCrawler.Config.DefaultConfig as DefaultConfig

################################################################################

# class Path(DefaultConfig.Path):
#    pass
'''

        path = args.config or cls.default_path()
        cls._logger.info('Create config file {}'.format(path))
        content = template.format(args).lstrip()
        DefaultConfig.Path.make_user_directory()
        with open(path, 'w') as fh:
            fh.write(content)

    ##############################################

    def __init__(self, config_path=None):

        path = config_path or self.default_path()
        self._logger.info('Load config from {}'.format(path))

        if not Path(path).exists():
            raise NameError("You must first create a configuration file using the init command")

        # This code as issue with code in class definition ???
        # with open(path) as fh:
        #     code = fh.read()
        # namespace = {'__file__': path}
        # # code_object = compile(code, path, 'exec')
        # exec(code, {}, namespace)
        # for key, value in namespace.items():
        #     setattr(self, key, value)

        # A factory function for creating a ModuleSpec instance based on the path to a file.
        spec = importlib_util.spec_from_file_location(name='Config', location=path)
        # Create a new module based on spec
        Config = importlib_util.module_from_spec(spec)
        # executes the module in its own namespace when a module is imported
        spec.loader.exec_module(Config)

        # Copy attributes from config or default
        for key in DefaultConfig.__all__:
            customised = hasattr(Config, key)
            if customised:
                src = Config
            else:
                src = DefaultConfig
            value = getattr(src, key)
            setattr(self, key, value)
            if customised:
                # Hack: reset ConfigFile_ClassName in DefaultConfig
                setattr(DefaultConfig, 'ConfigFile_' + key, value)
