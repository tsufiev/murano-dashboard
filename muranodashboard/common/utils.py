#    Copyright (c) 2014 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import string


def ensure_python_obj(obj):
    mappings = {'True': True, 'False': False, 'None': None}
    return mappings.get(obj, obj)


class Bunch(object):
    """Bunch is a container that provides both dictionary-like and
    object-like attribute access.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __contains__(self, item):
        return hasattr(self, item)

    def __iter__(self):
        return iter(self.__dict__.itervalues())


class BlankFormatter(string.Formatter):
    """Utility class aimed to provide empty string for non-existent keys."""
    def __init__(self, default=''):
        self.default = default

    def get_value(self, key, args, kwargs):
        if isinstance(key, str):
            return kwargs.get(key, self.default)
        else:
            return string.Formatter.get_value(self, key, args, kwargs)
