#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class Version(object):
    def __init__(self, version):
        self.version = list(map(int, re.findall("\d+", version)))

    def __str__(self):
        return ".".join(list(map(str, self.version)))

    def __repr__(self):
        return f"version: {self.version}"

    def __lt__(self, other):  # <
        return self.version < other.version

    def __le__(self, other):  # <=
        return self.version <= other.version

    def __eq__(self, other):  # ==
        return self.version == other.version

    def __ne__(self, other):  # !=
        return self.version != other.version

    def __gt__(self, other):  # >
        return self.version > other.version

    def __ge__(self, other):  # >=
        return self.version >= other.version


if __name__ == "__main__":
    import ipdb

    def compare(v1, v2):
        print(f"{v1} > {v2}", Version(v1) > Version(v2))
        print(f"{v1} >= {v2}", Version(v1) >= Version(v2))
        print(f"{v1} < {v2}", Version(v1) < Version(v2))
        print(f"{v1} <= {v2}", Version(v1) <= Version(v2))
        print(f"{v1} == {v2}", Version(v1) == Version(v2))
        print(f"{v1} != {v2}", Version(v1) != Version(v2))

    print("\n==============================")
    compare("1.1", "1.1.1")

    print("\n==============================")
    compare("1.1.1", "1.1.1")

    print("\n==============================")
    compare("1.2.1", "1.1.2")

    print("\n==============================")
    compare("1.2.1", "1.1.1.2")

    # ipdb.set_trace()
