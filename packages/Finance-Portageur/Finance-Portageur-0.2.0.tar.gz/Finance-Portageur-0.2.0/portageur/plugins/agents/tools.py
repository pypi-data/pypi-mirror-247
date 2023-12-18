from langchain.tools import Tool
from collections import namedtuple

class ToolTuple(
    namedtuple(
        'ToolTuple',(
            'name','func','description'
        ))):
    __slots__ = ()


    def __repr__(self):
        return "\nname:{}\ndescription:{}\func:{}".format(
            self.name, self.description, self.func)

    def to_tool(self):
        return Tool(
            name=self.name,description=self.description,
            func=self.func)
    
    @classmethod
    def from_dictionary(cls, dict):
        return cls(**dict)

## 多格式加载
def create_tools(tool_array):
    res = [] 
    for array in tool_array:
        if isinstance(array, dict):
            res.append(ToolTuple.from_dictionary(array))
    return res