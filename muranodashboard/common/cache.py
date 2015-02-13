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

try:
    import cPickle as pickle
except ImportError:
    import pickle
import functools
import logging
import os

from muranodashboard.environments import consts


LOG = logging.getLogger(__name__)
OBJS_PATH = os.path.join(consts.CACHE_DIR, 'apps')

if not os.path.exists(OBJS_PATH):
    os.makedirs(OBJS_PATH)
    LOG.info('Creating apps cache directory located at {dir}'.
             format(dir=OBJS_PATH))

LOG.info('Using apps cache directory located at {dir}'.
         format(dir=OBJS_PATH))


def _get_entry_path(app_id):
    head, tail = app_id[:2], app_id[2:]
    head = os.path.join(OBJS_PATH, head)
    if not os.path.exists(head):
        os.mkdir(head)
    tail = os.path.join(head, tail)
    if not os.path.exists(tail):
        os.mkdir(tail)
    return tail


def _load_from_file(file_name):
    if os.path.isfile(file_name):
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    else:
        return None


def _save_to_file(file_name, content):
    dir_path = os.path.dirname(file_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(file_name, 'wb') as f:
        pickle.dump(content, f)


def with_cache(*dst_parts):
    def _decorator(func):
        @functools.wraps(func)
        def __inner(request, app_id, *args):
            parts = tuple([str(part) for part in (dst_parts + args)])
            path = os.path.join(_get_entry_path(app_id), *parts)
            content = _load_from_file(path)
            if content is None:
                content = func(request, app_id, *args)
                if content:
                    LOG.debug('Caching value at {0}.'.format(path))
                    _save_to_file(path, content)
            else:
                LOG.debug('Using cached value from {0}.'.format(path))

            return content

        return __inner

    return _decorator
