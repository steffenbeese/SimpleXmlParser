import lxml.etree as ET
import re


class SimpleXmlParser:
    '''
        Adds some features for easy usage for lxml etree.
    '''
    
    def __init__(self, xml_file: str, encoding: str='utf-8'):
        self.xml_file = xml_file
        self.encoding = encoding
        parser = ET.XMLParser(remove_blank_text=True, remove_comments=False)
        self.tree = ET.parse(self.xml_file,parser)
        self.root = self.tree.getroot()

    def addAttribute(self, node: ET.Element, attribute: str, value: str, path: str=""):
        '''
            Adds an attribute to a node.
        '''
        if node is None and path != "":
            node = self.getNodeByPath(path)
        node.set(attribute, value)

    def addNode(self, parent: ET.Element, node: ET.Element):
        '''
            Adds a node to a parent node.
        '''
        parent.append(node)

    def addNodeWithAttributes(self, parent: ET.Element, node: str, text: str, attributes: dict):
        '''
            Adds a node to a parent node with attributes.
        '''
        child = ET.SubElement(parent, node)
        child.text = text
        for key, value in attributes.items():
            child.set(key, value)

    def addNodeByString(self, parent: ET.Element, node: str):
        '''
            Adds a node to a parent node.
        '''
        parent.append(ET.fromstring(node))

    def getAttribute(self, node: ET.Element, attribute: str):
        '''
            Returns the value of an attribute.
        '''
        return node.get(attribute)  
    
    def getAttributes(self, node: ET.Element):
        '''
            Returns all attributes of a node.
        '''
        return node.attrib

    def getNodeByPath(self, path: str):
        '''
            Returns a node by a path.
        '''
        return self.root.find(path)
    
    def replaceNodeText(self, node: ET.Element=None, text: str="", path: str=""):
        '''
            Replaces the text of a node.
        '''
        if node is None and path != "":
            node = self.getNodeByPath(path)
        node.text = text

    def replaceNode(self, root: ET.Element,node: ET.Element, new_node: ET.Element):
        '''
            Replaces a node with a new node.
        '''
        try:
            root.remove(node)
        except Exception as e:
            print(e)
            return
        root.append(new_node)


    def replaceNodeByString(self, root: ET.Element,node: ET.Element, new_node: str):
        '''
            Replaces a node with a new node.
        '''
        try:
            root.remove(node)
        except Exception as e:
            print(e)
            return
        root.append(ET.fromstring(new_node))
    
    def getFormattedXml(self):
        '''
            Returns the formatted xml.
        '''
        parser = ET.XMLParser(remove_blank_text=True)
        treestring=ET.tostring(self.root, pretty_print=True, encoding=str)
        return ET.tostring(ET.fromstring(re.sub(r'(\n *)+', r'\n', treestring),parser), pretty_print=True, encoding=str)
    
    def writeFormattedXml(self, xml_file: str):
        '''
            Writes the formatted xml to a file.
        '''
        with open(xml_file, 'w', encoding=self.encoding) as f:
            f.write(self.getFormattedXml())