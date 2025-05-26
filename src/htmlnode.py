class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def props_to_html(self):
        if not self.props:
            return ""
        return ''.join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        child_repr = ', '.join(repr(child) for child in self.children)
        return (
            f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
            f"children=[{child_repr}], props={self.props})"        )

    
        
#leaf node class, a HTML node that doesn't accept a child
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, children=None, props=props)

    
    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value        
        
        if self.tag == "a":
            # props'un dict olduğunu varsayıyorum, örn: {'href': 'url'}
            # Burada tek bir prop bekleniyor gibi
            if not self.props or 'href' not in self.props:
                raise ValueError("Missing href in props for <a> tag")
            href = self.props['href']
            res = f'<{self.tag} href="{href}">{self.value}</{self.tag}>'
        elif self.tag == "img":        
            res = f'<{self.tag} src="{self.props["src"]}" alt="{self.value}" />'

        else:
            res = f"<{self.tag}>{self.value}</{self.tag}>"
        return res


#parent node any HTML node that isn't a leaf node
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag parameter cannot be empty")
        if not self.children:
            raise ValueError("children parameter cannot be empty")
        
        html_parts = []
        for item in self.children:
            html = item.to_html()
            if not isinstance(html, str):
                raise TypeError("child.to_html() must return a string")
            html_parts.append(html)

        return f"<{self.tag}>{''.join(html_parts)}</{self.tag}>"
    

        
        

