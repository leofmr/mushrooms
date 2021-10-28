class TreeNode:
    def __init__(self, text):
        self.text = text
        
        self.depth = self._identify_depth()
        self.node = self._parse_node()
        
        self.is_leaf = self._check_node_type()
        
        self._parse_node_text()
        
    
    def _identify_depth(self):
        return len(self.text.split("   "))
    
    def _parse_node(self):
        times = self.depth - 1
        prefix = "|   " * times + "|--- "
        return self.text.replace(prefix, "")
    
    def _check_node_type(self):
        return self.node.startswith("class: ")
    
    
    def _parse_node_text(self):
        
        if self.is_leaf:
            
            self.variable = None
            self.category = None
            self.is_equal = None
            self.prediction = self.node[-1]
            
        else:
            feature = self.node.split(" ")[0]
            self.variable, self.category = feature.split("_")
            self.variable = self.variable.replace("-", " ")
            self.is_equal = ">" in self.node
            self.prediction = None