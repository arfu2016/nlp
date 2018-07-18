"""
@Project   : aiball
@Module    : person.specific_information.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/12/18 5:14 PM
@Desc      : 
"""
from chatbot import Response
from aiball.core.en_topic import EnTopic


class TopicPersonSpecificInformation(EnTopic):
    """人员具体信息"""

    # def __init__(self):
    #     super().__init__()
    #     self.create_attr()

    def create_attr(self):
        self._extract_words()
        self._generate_subcode_maps()
        self._generate_response_functions()

    @classmethod
    def topic_name(cls):
        return "person.specific_information"

    def _extract_words(self):
        self.keywords = []
        question = self.parameters["text"]
        cases = ('height weight nationality age constellation '
                 'birthday club').split()
        cases.append('shirt number')
        self.subcodes = list(range(120101, 120109))
        self.case_code = {case: code for case, code
                          in zip(cases, self.subcodes)}
        for case in cases:
            if case in question:
                self.keywords.append(case)

    def _calc_subcode(self):
        if len(self.keywords) > 1:
            return 120100
        elif len(self.keywords) == 1:
            return self.case_code[self.keywords[0]]
        return 100000

    def _generate_subcode_maps(self):
        self.cases = ('multiple height weight shirt_number nationality age '
                      'constellation birthday club').split()
        response_methods = ['response_' + case for case in self.cases]
        descs = ["球员多个具体信息", "球员身高", "球员体重", "球员号码",
                 "球员国籍", "球员年龄", "球员星座", "球员生日", "球员所属俱乐部"]
        subcodes = [120100] + self.subcodes
        self._subcode_maps = dict()
        for idx, desc in enumerate(descs):
            temp = {subcodes[idx]: {
                "desc": desc,
                "method": response_methods[idx],
                "params": {"person": "player"},
                "protocol": 2049
            }}
            self._subcode_maps.update(temp)

    @property
    def subcode_maps(self):
        return self._subcode_maps

    @property
    def subcode_maps(self):
        return {
            120100: {
                "desc": "球员多个具体信息",
                "method": "response_multiple",
                "params": {"person": "player"},
                "protocol": 2049
            },
            120101: {
                "desc": "球员身高",
                "method": "response_height",
                "params": {"person": "player"},
                "protocol": 2049
            },
            120102: {
                "desc": "球员体重",
                "method": "response_weight",
                "params": {"person": "player"},
                "protocol": 2049
            },
            120103: {
                "desc": "球员号码",
                "method": "response_shirt_number",
                "params": {"person": "player"},
                "protocol": 2049
            },
            120104: {
                "desc": "球员国籍",
                "method": "response_nationality",
                "params": {"person": "player"},
                "protocol": 2049
            },
            120105: {
                "desc": "球员年龄",
                "method": "response_age",
                "params": {"person": "player"},
                "protocol": 2049
            },
            120106: {
                "desc": "球员星座",
                "method": "response_constellation",
                "params": {"person": "player"},
                "protocol": 2049
            },
            120107: {
                "desc": "球员生日",
                "method": "response_birthday",
                "params": {"person": "player"},
                "protocol": 2049
            },
            120108: {
                "desc": "球员所属俱乐部",
                "method": "response_club",
                "params": {"person": "player"},
                "protocol": 2049
            },

        }

    def _generate_response_function(self, attr):

        def response():
            person = self.parameters["person"]
            person_id = self.parameters["person_id"]
            question = self.parameters["text"]
            user = self.parameters["user"]
            subcode = self.parameters["subcode"]
            # short_answer = get_person_attr(person_id, attr)
            # reply_success = get_reply_method(subcode, case='success')
            # reply_fail = get_reply_method(subcode, case='fail')

            short_answer = '180'
            if short_answer:
                answer = 'The height of ' + person + ' is ' + short_answer
            else:
                answer = 'No relevant information'

            res = self.create_response(self.subcode)
            raw_data = {"msg": question}
            output = {"protocol": 2049, "msg": answer}
            res.put(raw_data, 2049, output)

            return res

        return response

    def _generate_response_functions(self):

        for attr in self.cases:

            method = 'response_' + attr
            self.__dict__[method] = self._generate_response_function(attr)


if __name__ == '__main__':

    def get_person_attr(person_id: int, attr: str):
        """
        获取人员的具体信息，比如身高、体重、号码、国籍、年龄、星座、生日、所属俱乐部
        :param person_id:
        :param attr: height, weight, shirt_number, nationality, age,
                     birthday, constellation, birthday, club
        :return: 相关信息，int or str
        """
        pass


    # topic = TopicPersonSpecificInformation()

    def t_test180713():

        from aiball.protocol.client.client_msg import ClientMsgData
        from aiball.protocol.client.parameter import ParameterNormalTextMsg
        from aiball.protocol.msg import ClientMsg
        from aiball.core.en_bot import EnBot

        questions = ["Could you tell me Cristiano Ronaldo's weight?",
                     # "What's Cristiano Ronaldo's height?",
                     "Could you tell me what is Cristiano Ronaldo's height?", ]

        for question in questions:
            msg = {
                "user": "for_test",
                "msg": question
            }

            param = ParameterNormalTextMsg()
            param.load(msg)

            cmd = ClientMsgData()
            cmd.param = param
            cmd.idfa = msg["user"]

            cm = ClientMsg()
            cm.user = msg["user"]
            cm.data = cmd

            msg = EnBot._extract_msg(cm)

            en_client = EnBot._create_client(cm)
            # print('en_client parse result', en_client._parse(msg['text'], {}))

            print('question:', question)

            en_client._dialog.parse_data['intent'] = 'person.specific_information'
            print('en_client._dialog.intent:', en_client._dialog.intent)

            # print('en_clinet dialog', en_client._dialog.parse_data)

            topic = TopicPersonSpecificInformation()
            topic.parameters.deserialize(en_client._dialog.parse_data)
            topic.create_attr()

            print('topic.parameters', topic.parameters.serialized_data())
            print('response:',
                  topic.response(en_client._dialog).serialized_data)

            print()

    t_test180713()
