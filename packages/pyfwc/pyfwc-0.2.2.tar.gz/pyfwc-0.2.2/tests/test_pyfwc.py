from pyfwc import fwc
import pytest
import pandas as pd
# from pandas.testing import assert_frame_equal

@pytest.mark.parametrize("award_name,expected", [('mining','MA000001')])
class TestClass:
    # def __init__(self):
    #     self.fwc = fwc.FWCAPI('5d37f1a91012490089e4a5ac698fd512')

    def test_getaward(self, award_name, expected):
        assert fwc.FWCAPI('c483613ac4874570a2b847c0c068b20a').get_awards(award_name)['code'][0] == expected
