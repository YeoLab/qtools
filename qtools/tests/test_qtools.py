#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_qtools
----------------------------------

Tests for `qtools` module.
"""

import pytest


@pytest.fixture
def command():
    return 'bedtools intersect exons.bed placental_conserved_elements.bed'


@pytest.fixture(params=['string', 'list'])
def commands(request, command):
    if request.param == 'string':
        return command
    elif request.param == 'list':
        return [command]


class TestSubmitter(object):

    def test_init(self):
        pass
