import unittest
from xml.etree.ElementTree import Element, SubElement
from unittest.mock import mock_open
import xml.etree.ElementTree as ET
from xml.dom import minidom



from SimpleXmlParser import SimpleXmlParser
import os


class TestSimpleXmlParser(unittest.TestCase):

    def setUp(self):
        self.xml_file = os.path.join('./test','SampleXml_orig.xml')
        self.encoding = 'utf-8'
        self.xml_parser = SimpleXmlParser(self.xml_file, self.encoding)
        self.root = self.xml_parser.root

    def test_addAttribute(self):
        test_node = self.xml_parser.getNodeByPath('./media/medium[2]/phases/phase[2]/properties/property[4]/minimal_porosity')
        self.xml_parser.addAttribute(test_node, 'test_attribute', 'test_value')
        self.assertEqual(test_node.get('test_attribute'), 'test_value')

    def test_addNode(self):
        test_parent = self.xml_parser.getNodeByPath('./media/medium[2]/phases/phase[2]/properties')
        self.xml_parser.addNode(test_parent, 'test_Property', 'test_value')
        test_node = test_parent.find('test_Property')
        self.assertIsNotNone(test_node)
        self.assertEqual(test_node.text, 'test_value')

    def test_addNodeWithAttributes(self):
        test_parent = self.xml_parser.getNodeByPath('./time_loop/processes/process/convergence_criterion')
        attributes = {'attrib_1': 'value_1', 'attrib_2': 'value_2'}
        self.xml_parser.addNodeWithAttributes(test_parent, 'test_node', 'test_text', attributes)
        test_node = test_parent.find('test_node')
        self.assertIsNotNone(test_node)
        self.assertEqual(test_node.text, 'test_text')
        self.assertEqual(test_node.get('attrib_1'), 'value_1')
        self.assertEqual(test_node.get('attrib_2'), 'value_2')

    def test_addNodeByString(self):
        test_parent = self.xml_parser.getNodeByPath('./media/medium[2]/phases/phase[2]/properties')
        self.xml_parser.addNodeByString(test_parent, ''' <Newproperty>
                            <name>micro_porosity</name>
                            <type>FromMassBalance</type>
                            <initial_porosity>phi_m0</initial_porosity>
                            <minimal_mporosity>0</minimal_mporosity>
                            <maximal_mporosity>1</maximal_mporosity>
                        </Newproperty> ''')
        test_node = test_parent.find('Newproperty')
        self.assertIsNotNone(test_node)

    def test_getAttribute(self):
        test_node = Element('test_node', {'test_attribute': 'test_value'})
        attribute_value = self.xml_parser.getAttribute(test_node, 'test_attribute')
        self.assertEqual(attribute_value, 'test_value')

    def test_getAttributes(self):
        test_node = Element('test_node', {'test_attribute_1': 'test_value_1', 'test_attribute_2': 'test_value_2'})
        attributes_dict = self.xml_parser.getAttributes(test_node)
        self.assertIsInstance(attributes_dict, dict)
        self.assertEqual(len(attributes_dict), 2)
        self.assertEqual(attributes_dict['test_attribute_1'], 'test_value_1')
        self.assertEqual(attributes_dict['test_attribute_2'], 'test_value_2')

    def test_replaceNodeText(self):
        test_node = Element('test_node')
        test_node.text = 'old_text'
        self.xml_parser.replaceNodeText(test_node, 'new_text')
        self.assertEqual(test_node.text, 'new_text')

    def test_replaceNode(self):
        test_parent = self.xml_parser.getNodeByPath('./media/medium[2]/phases/phase[2]/properties')
        old_node = self.xml_parser.getNodeByPath('./media/medium[2]/phases/phase[2]/properties/property[2]')
        new_node = ET.fromstring('''<Newproperty>
                            <Newname>ReplacedBiot</Newname>
                            <type>Constant</type>
                            <value>999</value>
                        </Newproperty>
        ''')
        self.xml_parser.replaceNode(test_parent,old_node, new_node)
        self.assertIsNotNone(test_parent.find('Newproperty'))

    def test_replaceNodeByString(self):
        test_parent = Element('test_parent')
        old_node = SubElement(test_parent, 'old_node')
        self.xml_parser.replaceNodeByString(test_parent,old_node, '<new_node>new_text</new_node>')
        self.assertIsNone(test_parent.find('old_node'))
        test_node = test_parent.find('new_node')
        self.assertIsNotNone(test_node)
        self.assertEqual(test_node.text, 'new_text')


    def test_getFormattedXml(self):
        return self.xml_parser.getFormattedXml()
    
    def test_writeXml(self):
        xml_file_path = 'SampleXml.xml'
        self.xml_parser.writeFormattedXml(os.path.join('test','SampleXml.xml'))