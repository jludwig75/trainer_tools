# MIT License

# Copyright (c) 2020 Jonathan Ludwig, Michal Kozma

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

RANGE_MIN=0
RANGE_MAX=1
RANGE_VALUE=2


class RangedValueMapper:
    def __init__(self, ranges, swing):
        self._ranges = ranges
        self._range_swing = swing
        self._MIN_RANGE = 0
        self._MAX_RANGE=len(self._ranges) - 1
        self._current_index = 0

    def map_value(self, input_value):
        if input_value > self._ranges[-1][RANGE_MAX]:
            self._current_index = self._MAX_RANGE
        elif input_value < self._ranges[0][RANGE_MIN]:
            self._current_index = self._MIN_RANGE
        else:
            while True:
                if input_value < self._ranges[self._current_index][RANGE_MIN] - self._range_swing:
                    self._current_index -= 1
                elif input_value > self._ranges[self._current_index][RANGE_MAX] + self._range_swing:
                    self._current_index += 1
                else:
                    break
            assert self._current_index >= self._MIN_RANGE and self._current_index <= self._MAX_RANGE
        return self._ranges[self._current_index][RANGE_VALUE]
