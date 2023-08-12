# Copyright © Enzo Busseti 2019.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Greedy grid search for hyper-parameter optimization.
"""

import math
import logging

logger = logging.getLogger(__name__)

__version__ = '0.1'


def min_key(d):
    return min(d, key=d.get)


def greedy_grid_search(function,
                       parameter_indexables,
                       num_steps=1):
    """Evaluates function on combinations from
    the parameter_indexables dictionary. Returns lowest
    value obtained from greedy grid search, starting
    from the first parameters in the indexables."""

    results = {}

    current_counter = [0 for param in parameter_indexables]

    def evaluate_function():

        if not tuple(current_counter) in results:
            params = {param: parameter_indexables[param][current_counter[i]]
                      for i, param in enumerate(parameter_indexables)}

            logger.info('evaluating function at %s' % params)
            value = function(**params)
            if math.isnan(value):
                raise ValueError('Function must return real value or +inf.')
            logger.info('function value = %f' % value)
            results[tuple(current_counter)] = value

    evaluate_function()

    def search_n_step(n):
        for i, param in enumerate(parameter_indexables):
            if current_counter[i] < len(parameter_indexables[param]) - 1:
                current_counter[i] += 1
                evaluate_function()
                if n > 1:
                    search_n_step(n - 1)
                current_counter[i] -= 1

            if current_counter[i] > 0:
                current_counter[i] -= 1
                evaluate_function()
                if n > 1:
                    search_n_step(n - 1)
                current_counter[i] += 1

    while True:

        search_n_step(num_steps)

        old_current_counter = current_counter
        current_counter = list(min_key(results))

        if tuple(old_current_counter) == tuple(current_counter):
            logger.debug('optimal function value = %f' %
                         results[tuple(current_counter)])
            logger.debug('optimal function parameters = %s' %
                         str(tuple(current_counter)))
            return results[tuple(current_counter)], \
                {param:  parameter_indexables[param][current_counter[i]]
                 for i, param in
                 enumerate(parameter_indexables)}, results
