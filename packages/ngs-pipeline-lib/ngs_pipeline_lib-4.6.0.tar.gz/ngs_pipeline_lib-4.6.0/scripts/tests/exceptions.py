class TestError(Exception):
    # This is needed to prevent pytest from discovering testcase within this class
    __test__ = False
