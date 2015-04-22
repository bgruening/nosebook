import json
import os
import unittest

from nose.plugins import PluginTester

from nosebook import Nosebook

OTHER_ARGS = ["--verbosity=3"]

NBFORMAT = ""

if os.environ.get("IP_VERSION", None) == 2:
    NBFORMAT = "nbformat3.*"


def match(pattern):
    return "--nosebook-match=.*%s%s.*" % (NBFORMAT, pattern)


def match_cell(pattern):
    return "--nosebook-match-cell=%s" % pattern


def scrub(patterns):
    return "--nosebook-scrub=%s" % json.dumps(patterns)


class TestNosebook(PluginTester, unittest.TestCase):
    activate = "--with-nosebook"
    plugins = [Nosebook()]
    args = [match("Test Simple")] + OTHER_ARGS
    env = {}

    def test_found(self):
        """
        Tests are found
        """
        assert "Ran 0 tests" not in self.output, ("got: %s" % self.output)

    def test_pass(self):
        """
        Tests pass
        """
        assert "FAIL" not in self.output, ("got: %s" % self.output)

    def makeSuite(self):
        """
        will find the notebooks
        """
        pass


class TestScrubDict(TestNosebook):
    args = [
        match("Scrubbing"),
        scrub({
            "a random number <0x0\.\d*>": "scrub1",
            "some other random number <0x0\.\d*>": "scrub2",
            "<(.*) at 0x[0-9a-f]+>": "<\1>"
        })
    ] + OTHER_ARGS


class TestScrubList(TestNosebook):
    args = [
        match("Scrubbing"),
        scrub([
            "a random number <0x0\.\d*>",
            "some other random number <0x0\.\d*>",
            "<(.*) at 0x[0-9a-f]+>"
        ])
    ] + OTHER_ARGS


class TestScrubStr(TestNosebook):
    args = [
        match("Scrubbing"),
        scrub("((a|some other) random number <0x0\.\d*>)|"
              "<(.*) at 0x[0-9a-f]+>")
    ] + OTHER_ARGS


class TestMatchCell(TestNosebook):
    args = [
        match("Test"),
        match_cell("^\s*(class|def) .*[tT]est.*")
    ] + OTHER_ARGS


if __name__ == '__main__':
    unittest.main()
