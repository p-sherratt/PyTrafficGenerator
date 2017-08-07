"""
Tests for basic TGN object operations.

@author yoram@ignissoft.com
"""

import unittest
from mock import MagicMock

from trafficgenerator.tgn_utils import is_false, is_true, is_local_host, is_ip
from trafficgenerator.tgn_object import TgnObject


class TgnObjectTest(unittest.TestCase):

    def setUp(self):
        self.root = TgnObject(objRef='root1', objType='root')
        self.leaf1 = TgnObject(objRef='leaf1', objType='leaf', parent=self.root)
        self.node1 = TgnObject(objRef='node1', objType='node', parent=self.root, name='name1')
        self.node2 = TgnObject(objRef='node2', objType='node', parent=self.root, name='name2')
        self.node11 = TgnObject(objRef='node11', objType='node', parent=self.node1, name='name11')
        self.leaf11 = TgnObject(objRef='leaf11', objType='leaf', parent=self.node1)
        for o in self.__dict__.values():
            if type(o) == TgnObject:
                self._mock_object(o)

    def tearDown(self):
        pass

    def testHelloWorld(self):
        pass

    def testObjectsTree(self):
        """ Test object search operations. """

        assert(self.root.obj_ref() == 'root1')
        assert(self.root.obj_type() == 'root')
        assert(self.root.obj_name() == 'root1')
        assert(self.node1.obj_ref() == 'node1')
        assert(self.node1.obj_type() == 'node')
        assert(self.node1.obj_name() == 'name1')
        assert(self.node1.obj_parent() == self.root)

        assert(self.root.get_object_by_name('name2') == self.node2)
        assert(len(self.root.get_objects_by_type('node')) == 2)
        assert(len(self.root.get_objects_by_type('no_such_object')) == 0)
        assert(self.root.get_object_by_ref('leaf1') == self.leaf1)

        assert(len(self.root.get_objects_by_type_in_subtree('node')) == 3)
        assert(len(self.root.get_objects_by_type_in_subtree('leaf')) == 2)
        assert(len(self.node11.get_objects_by_type_in_subtree('node')) == 0)

        assert(str(self.root) == self.root.obj_name())

        assert(len(self.root.get_objects_with_attribute('node', 'attr_name', 'node1')) == 1)

    def _mock_object(self, o):
        o.get_attribute = MagicMock(name='get_attribute')
        o.get_attribute('attr_name')
        o.get_attribute.return_value = o.obj_ref()


class TgnUtilsTest(unittest.TestCase):

    def testTrueFalse(self):
        """ Test TGN true and false values. """

        for false_stc in ('False', 'false', '0', 'null', 'NONE', 'none', '::ixnet::obj-null'):
            assert(is_false(false_stc))
            assert(not is_true(false_stc))

        for true_str in ('True', 'TRUE', '1'):
            assert(is_true(true_str))
            assert(not is_false(true_str))

    def testLocalhost(self):
        """ Test TGN localhost values. """

        for location in ('127.0.0.1', 'localhost', 'Localhost/1/1', '//(Offline)/1/1', 'null'):
            assert(is_local_host(location))

        for location in ('1.2.3.4', 'hostname', '192.168.1.1/1/2'):
            assert(not is_local_host(location))

    def testIps(self):
        """ Test TGN IP values. """

        for ip in ('IPV4', 'ipv6', 'ipv4if', 'IPV6IF'):
            assert(is_ip(ip))

        for ip in ('mac', 'bla'):
            assert(not is_ip(ip))