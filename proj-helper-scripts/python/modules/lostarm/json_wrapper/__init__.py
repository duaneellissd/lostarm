import json
import os
from lostarm.utils import VerbosePrint


class JsonWrapper(VerbosePrint):
    def __init__(self):
        VerbosePrint.__init__(self)
        self.filename : str = ""
        self.data : dict = dict()



