from enum import Enum
from htmlnode import HTMLNode, LeafNode

class TextType(Enum):
	TEXT = None
	BOLD = "b" #"**Bold text**"
	ITALIC = "i" #"_Italic text_"
	CODE = "code" #"`Code text`"
	LINK = "a" #"[anchor text](url)"
	IMAGE = "img" #![alt text](url)"


class TextNode:

	def __init__(self, text: str, text_type, url: str=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, node):
		return self.text == node.text and self.text_type == node.text_type and self.url == node.url

	def __repr__(self):
		if self.url:
			return f"TextNode({self.text}, {self.text_type}, {self.url})"
		else:
			return f"TextNode({self.text}, {self.text_type})"
	
	def text_node_to_html_node(self):
		if self.text_type not in TextType:
			raise Exception("Not a valid text type")

		if self.text_type == TextType.LINK:
			return LeafNode('a', self.text, {"href": self.url})
		elif self.text_type == TextType.IMAGE:
			return LeafNode('img', '', {"src": self.url, "alt": self.text})
		else:
			return LeafNode(self.text_type.value, self.text)