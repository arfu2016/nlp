"""
@Project   : aiball
@Module    : test_protocol_client.py
@Author    : Klose [klose@cubee.com]
@Created   : 2018/6/26 19:16
@Desc      : 
"""

import copy
import unittest
from aiball.protocol.msg import ClientMsg


class TestValue273:
    value_normal = {
        "user": "270875058652579840_ccb9bece-7796-44be-91f3-9b563e074094",
        "idfa": "gatwway",
        "data": {
            "code": 273,
            "uid": 115511,
            "idfa": "270875058652579840_ccb9bece-7796-44be-91f3-9b563e074094",
            "platform": "mi_brain",
            "version": "1.20",
            "param": {
                "msg": "冰岛和克罗地亚的比赛谁会赢"
            },
            "source": "",
            "ssid": 1181,
        }
    }

    def get_normal_value(self):
        des = copy.deepcopy(self.value_normal)
        return des

    def get_no_code_value(self):
        des = copy.deepcopy(self.value_normal)
        del des["data"]["code"]
        return des

    def get_error_code(self):
        des = copy.deepcopy(self.value_normal)
        des["data"]["code"] = 299
        return des

    def get_no_idfa(self):
        des = copy.deepcopy(self.value_normal)
        del des["data"]["idfa"]
        return des

    def get_no_matchid(self):
        des = copy.deepcopy(self.value_normal)
        del des["data"]["ssid"]
        return des

    def get_no_platform(self):
        des = copy.deepcopy(self.value_normal)
        del des["data"]["platform"]
        return des

    def get_no_version(self):
        des = copy.deepcopy(self.value_normal)
        del des["data"]["version"]
        return des

    def get_no_msg(self):
        des = copy.deepcopy(self.value_normal)
        del des["data"]["param"]["msg"]
        return des

    def get_no_param(self):
        des = copy.deepcopy(self.value_normal)
        del des["data"]["param"]
        return des

    def get_value_none(self):
        return {}

    def get_value_extra(self):
        des = copy.deepcopy(self.value_normal)
        des["data"]["param"]["button_type"] = 1
        des["data"]["param"]["content_pool_id"] = 1
        des["data"]["param"]["entity_id"] = 1
        des["data"]["param"]["entity_type"] = 1
        des["data"]["param"]["ack"] = "111111111111111111"
        return des

    def get_type_error(self):
        des = copy.deepcopy(self.value_normal)
        des["data"]["code"] = str(des["data"]["code"])
        des["data"]["uid"] = str(des["data"]["uid"])
        des["data"]["ssid"] = str(des["data"]["ssid"])
        des["data"]["version"] = float(des["data"]["version"])
        des["data"]["param"]["button_type"] = "1"
        des["data"]["param"]["content_pool_id"] = "1"
        des["data"]["param"]["entity_id"] = "1"
        des["data"]["param"]["entity_type"] = "1"
        return des


class TestClientMsg273(unittest.TestCase):
    def setUp(self):
        self.test_class = TestValue273()

    def tearDown(self):
        pass

    def test_pass(self):
        v1 = self.test_class.get_normal_value()
        c = ClientMsg()
        c.deserialize(str(v1))

        self.assertTrue(c.valid())
        self.assertEqual(c.code, 273)
        self.assertEqual(c.uid, 115511)
        self.assertEqual(c.platform, "mi_brain")
        self.assertEqual(c.version, "1.20")
        self.assertEqual(c.msg, "冰岛和克罗地亚的比赛谁会赢")
        self.assertEqual(c.ssid, 1181)

    def test_no_code_value(self):
        v1 = self.test_class.get_no_code_value()
        c = ClientMsg()
        c.deserialize(str(v1))

        self.assertFalse(c.valid())

    def test_error_code(self):
        v1 = self.test_class.get_error_code()
        c = ClientMsg()
        c.deserialize(str(v1))

        self.assertFalse(c.valid())

    def test_no_idfa(self):
        v1 = self.test_class.get_no_idfa()
        c = ClientMsg()
        c.deserialize(str(v1))
        self.assertFalse(c.valid())

    def test_no_matchid(self):
        v1 = self.test_class.get_no_matchid()
        c = ClientMsg()
        c.deserialize(str(v1))

        self.assertTrue(c.valid())
        self.assertEqual(c.ssid, 0)

    def test_no_platform(self):
        v1 = self.test_class.get_no_platform()
        c = ClientMsg()
        c.deserialize(str(v1))

        self.assertFalse(c.valid())

    def test_no_version(self):
        v1 = self.test_class.get_no_version()
        c = ClientMsg()
        c.deserialize(str(v1))

        self.assertFalse(c.valid())

    def test_no_msg(self):
        v1 = self.test_class.get_no_msg()
        c = ClientMsg()
        c.deserialize(str(v1))

        self.assertFalse(c.valid())

    def test_no_param(self):
        v1 = self.test_class.get_no_param()
        c = ClientMsg()
        c.deserialize(str(v1))

        self.assertFalse(c.valid())

    def test_value_none(self):
        v1 = self.test_class.get_value_none()
        c = ClientMsg()
        c.deserialize(str(v1))

        self.assertFalse(c.valid())

    def test_value_extra(self):
        v1 = self.test_class.get_value_extra()
        c = ClientMsg()
        c.deserialize(str(v1))

        self.assertTrue(c.valid())
        self.assertEqual(c.button_type, 1)
        self.assertEqual(c.content_pool_id(), 1)
        self.assertEqual(c.entity_id, 1)
        self.assertEqual(c.entity_type, 1)
        self.assertEqual(c.ack, "111111111111111111")
        self.assertEqual(c.button_type, 1)

    def test_type_error(self):
        v1 = self.test_class.get_type_error()
        c = ClientMsg()
        c.deserialize(str(v1))

        self.assertTrue(c.valid())
        self.assertEqual(c.button_type, 1)
        self.assertEqual(c.content_pool_id(), 1)
        self.assertEqual(c.entity_id, 1)
        self.assertEqual(c.entity_type, 1)
        self.assertEqual(c.button_type, 1)

        self.assertEqual(c.code, 273)
        self.assertEqual(c.uid, 115511)
        self.assertEqual(c.platform, "mi_brain")
        self.assertEqual(c.version, "1.20")
        self.assertEqual(c.msg, "冰岛和克罗地亚的比赛谁会赢")
        self.assertEqual(c.ssid, 1181)


if __name__ == "__main__":
    unittest.main()
