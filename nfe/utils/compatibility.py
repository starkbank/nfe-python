from sys import version_info as version
from lxml import etree


if version.major == 3:

    def xmlFromString(string):
        return etree.fromstring(string.encode("utf-8"))

    def getXmlText(element):
        return element.text

if version.major == 2:

    def xmlFromString(string):
        return etree.fromstring(string)

    def getXmlText(element):
        return element.text.encode("utf-8") if element.text else None
