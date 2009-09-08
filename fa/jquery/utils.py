# -*- coding: utf-8 -*-
import os
from mako.lookup import TemplateLookup

dirname = os.path.join(os.path.dirname(__file__), 'templates')
templates = TemplateLookup([dirname], input_encoding='utf-8', output_encoding='utf-8')


