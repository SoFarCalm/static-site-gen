from textnode import TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    if len(old_nodes) == 0:
        return new_nodes
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_node = old_node.text.split(delimiter)

        if len(split_node) % 2 == 0:
            raise Exception("Text is not valid markdown")
        else:
            created_nodes = []
            i = 0
            while i < len(split_node):
                if split_node[i].strip() == "":
                    i += 1
                    continue

                if (i == 0 or i % 2 == 0):
                    created_nodes.append(TextNode(split_node[i], TextType.TEXT))
                else:
                    created_nodes.append(TextNode(split_node[i], text_type))
                i += 1
            
            new_nodes.extend(created_nodes)
    
    return new_nodes