class HTMLNode:
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __eq__(self, node):
        return self.tag == node.tag and self.value == node.value and self.children == node.children and self.props == node.props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError("child classes will override")
    
    def props_to_html(self):
        props_string = ''
        for key,value in self.props.items():
            props_string = props_string + f'{key}="{value}" '

        return props_string

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict=None):
        super().__init__(tag, value, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("all lead nodes must have a value")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}>{self.value}</{self.tag}>"
        

