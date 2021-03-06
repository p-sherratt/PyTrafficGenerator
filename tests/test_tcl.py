"""
Tests for TGN Tcl wrapper - the default wrapper.

@author yoram@ignissoft.com
"""

import sys
from os import path
import logging
from configparser import ConfigParser

from trafficgenerator.tgn_tcl import TgnTclWrapper, tcl_list_2_py_list, py_list_to_tcl_list, tcl_file_name

config_file = path.join(path.dirname(__file__), 'TrafficGenerator.ini')


class TestTcl():

    def setup(self):
        config = ConfigParser(allow_no_value=True)
        config.read_file(open(config_file))

        logger = logging.getLogger('log')
        logger.setLevel(config.get('Logging', 'level'))
        logger.addHandler(logging.FileHandler(config.get('Logging', 'file_name')))
        logger.addHandler(logging.StreamHandler(sys.stdout))

        self.tcl = TgnTclWrapper(logger)

    def teardown(self):
        pass

    def test_list(self):
        """ Test Python->Tcl and Tcl->Python list conversion. """

        py_list = ['a', 'b b']
        tcl_list_length = self.tcl.eval('llength ' + py_list_to_tcl_list(py_list))
        assert int(tcl_list_length) == 2

        tcl_list = '{a} {b b}'
        python_list = tcl_list_2_py_list(tcl_list)
        assert len(python_list) == 2
        assert type(python_list[0]) is str
        assert type(python_list[1]) is str

        tcl_list = '{{a} {b b}}'
        python_list = tcl_list_2_py_list(tcl_list)
        assert len(python_list) == 2
        assert type(python_list[0]) is list
        assert type(python_list[1]) is list
        assert len(python_list[1]) == 2

        tcl_list = ''
        assert len(tcl_list_2_py_list(tcl_list)) == 0

        tcl_list = '{}'
        assert len(tcl_list_2_py_list(tcl_list)) == 0

        tcl_list = '[["a"], ["b", "b"]]'
        assert len(tcl_list_2_py_list(tcl_list)) == 2

    def test_file_name(self):
        """ Test Tcl file names normalization. """

        assert(tcl_file_name('a\\b/c').strip() == '{a/b/c}')
