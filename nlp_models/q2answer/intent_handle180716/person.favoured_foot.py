"""
@Project   : aiball
@Module    : person.favoured_foot.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/11/18 3:39 PM
@Desc      : 
"""
from chatbot import Response
from aiball.core.en_topic import EnTopic


class TopicPersonFavouredFoot(EnTopic):
    """球员惯用脚"""

    @classmethod
    def topic_name(cls):
        return "person.favoured_foot"

    def _calc_subcode(self):
        return 130401

    @property
    def subcode_maps(self):
        return {
            130401: {
                "desc": "球员惯用脚",
                "method": "response_favoured_foot",
                "params": {"person": "player"},
                "protocol": 2049
            }
        }

    def response_favoured_foot(self) -> Response:
        person = self.parameters["person"]
        person_id = self.parameters["person_id"]
        question = self.parameters["text"]
        user = self.parameters["user"]
        subcode = self.parameters["subcode"]
        # short_answer = get_person_favoured_foot(person_id)
        # reply_success = get_reply_method(subcode, 'success')
        # reply_fail = get_reply_method(subcode, 'fail')

        short_answer = 'left foot'
        if short_answer:
            answer = 'The favoured foot of ' + person + ' is ' + short_answer
        else:
            answer = 'No relevant information'

        res = self.create_response(self.subcode)
        raw_data = {"msg": question}
        output = {"protocol": 2049, "msg": answer}
        res.put(raw_data, 2049, output)

        return res


if __name__ == '__main__':

    # import os
    # os.environ["AIBALL_SETTINGS_ENV"] = 'dev'

    def get_person_favoured_foot(person_id: int) -> str:
        """
        查询人员惯用脚
        :param person_id:
        :return: left foot, right foot, or both feet
        """
        pass


    def get_reply_method(subcode: int, case: str) -> [str]:
        """
        获取话术
        :param subcode: topic的subcode
        :param case: 相关信息查询成功还是失败, 'success' or 'fail'
        :return: a list of strings, 比如['The favoured foot of ', 'is']
        """
        pass


    def t_test180712():

        from aiball.protocol.client.client_msg import ClientMsgData
        from aiball.protocol.client.parameter import ParameterNormalTextMsg
        from aiball.protocol.msg import ClientMsg
        from aiball.core.en_bot import EnBot

        questions = ["Could you tell me who Cristiano Ronaldo is?",
                     # "What's Cristiano Ronaldo's height?",
                     "Could you tell me what is Cristiano Ronaldo's height?", ]

        for question in questions:
            msg = {
                "user": "for_test",
                "msg": question
            }

            param = ParameterNormalTextMsg()
            param.load(msg)
            print('param', param.dump())

            cmd = ClientMsgData()
            cmd.param = param
            cmd.idfa = msg["user"]

            cm = ClientMsg()
            cm.user = msg["user"]
            cm.data = cmd
            print('cm.data', cm.data.dump())
            print('cm', cm.serialize())

            msg = EnBot._extract_msg(cm)
            print('msg', msg)

            en_client = EnBot._create_client(cm)
            print('en_client parse result', en_client._parse(msg['text'], {}))

            en_client._dialog.parse_data['intent'] = 'person.favoured_foot'
            print('en_client._dialog.intent', en_client._dialog.intent)

            print('en_clinet dialog', en_client._dialog.parse_data)

            topic = TopicPersonFavouredFoot()
            topic.parameters.deserialize(en_client._dialog.parse_data)

            parameters = topic.parameters
            print('parameters._data', parameters.serialized_data())

            print('topic.parameters', topic.parameters.serialized_data())
            print('response:',
                  topic.response(en_client._dialog).serialized_data)

            en_response = en_client.response()
            print('en_response:', en_response)

            res = EnBot.get_response(cm)
            print('res:', res)

    t_test180712()
