# weiqi.gs
# Copyright (C) 2016 Michael Bitzi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import io
from collections import defaultdict


class Node:
    def __init__(self):
        self.parent = None
        self.children = []
        self.props = defaultdict(list)
        self.head_subtree = False
        self.first_child = False

    def prop_one(self, key, default=''):
        return self.props.get(key.upper(), [default])[0]


class Reader(io.StringIO):
    def unread(self, size):
        self.seek(self.tell()-size)


class ParserError(Exception):
    pass


def parse_sgf(sgf):
    node = Node()
    node.first_child = True

    parse_node(node, Reader(sgf))

    return node


def parse_node(node, reader):
    while True:
        ch = reader.read(1)
        if not ch:
            break

        if ch.isspace():
            continue

        if ch.isalpha():
            reader.unread(1)
            parse_property(node, reader)
        elif ch == '(':
            node.head_subtree = True
        elif ch == ')':
            break
        elif ch == ';':
            if node.first_child:
                child = node
                node.first_child = False
            else:
                child = Node()
                child.parent = node
                node.children.append(child)

            parse_node(child, reader)

            if not node.head_subtree:
                break


def parse_property(node, reader):
    name = parse_property_name(reader)

    while True:
        value = parse_property_value(reader)
        node.props[name.upper()].append(value)

        ch = reader.read(1)
        if not ch:
            raise ParserError('unexpected EOF')

        reader.unread(1)

        if ch != '[':
            break


def parse_property_name(reader):
    prop = ''

    while True:
        ch = reader.read(1)
        if not ch:
            break

        if not ch.isalpha():
            reader.unread(1)
            break

        prop += ch

    return prop


def parse_property_value(reader):
    ch = reader.read(1)

    if ch != '[':
        reader.unread(1)
        return ''

    value = ''

    while True:
        ch = reader.read(1)
        if not ch:
            raise ParserError('unexpected EOF')

        if ch == ']':
            break

        if ch == '\\':
            next_ch = reader.read(1)
            if not next_ch:
                raise ParserError('unexpected EOF')

            if next_ch == ']':
                ch = next_ch
            else:
                reader.unread(1)

        value += ch

    return value
