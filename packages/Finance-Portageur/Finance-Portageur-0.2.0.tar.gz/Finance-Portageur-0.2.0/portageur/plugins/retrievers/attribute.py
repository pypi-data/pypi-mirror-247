from langchain.chains.query_constructor.schema import AttributeInfo
from collections import namedtuple

class AttributeTuple(
    namedtuple(
        'AttributeTuple',(
            'name','description','type'
        ))
    ):
    __slots__ = ()

    def __repr__(self):
        return "\nname:{}\ndescription:{}\ntype:{}".format(
            self.name, self.description, self.type
        )
    
    def to_atrribute(self):
        return AttributeInfo(
            name=self.name,description=self.description,
            type=self.type)
    
    @classmethod
    def from_dictionary(cls, dict):
        return cls(**dict)
    

## 多格式加载
def create_attribute(info_array):
    res = [] 
    for array in info_array:
        if isinstance(array, dict):
            res.append(AttributeTuple.from_dictionary(array))
    return res