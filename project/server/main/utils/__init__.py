""" Utility Function Belong to Here """

import datetime

def current_datetime():
    return datetime.datetime.utcnow()


class Json2Obj:

    def __init__(self, name, dict_={}):
        self._name = name
        self._keys = list()
        for attr in dict_:
            if isinstance(dict_.get(attr), dict):
                dict_[attr] = self.__class__.from_dict(attr, dict_.get(attr, None))
            elif isinstance(dict_.get(attr), list):
                dict_[attr] = list(self.__class__(attr, dt) for dt in dict_.get(attr))
            self._keys.append(attr)
        self.__dict__.update(dict_)

    def __repr__(self):
        items = (f"{k}={self.__dict__.get(k) !r}" for k in self._keys)
        return f"{self._name}({', '.join(items)})"
    
    def __str__(self):
        items = (f"{k}={self.__dict__.get(k) !s}" for k in self._keys)
        return f"{self._name}({', '.join(items)})"
    
    def to_dict(self):
        todict = {}
        for key in self.__dict__:
            if key in self._keys:
                if isinstance(self.__dict__[key], self.__class__):
                    todict[key] = self.__dict__[key].to_dict()
                else:
                    todict[key] = self.__dict__[key]
        return todict

    @classmethod
    def from_dict(cls, name, dict_={}):
        if dict_ is None:
            return None

        doc = cls(name, dict_)
        return doc