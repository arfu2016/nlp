"""
@Project   : CubeGirl
@Module    : question_test.py
@Author    : Deco [deco@cubee.com]
@Created   : 3/2/18 10:20 AM
@Desc      : process() in question_answer.py的测试
"""
from .question_answer import process
from . import single_question


class KnownQuestions:

    questions = ('鲁尼俱乐部队友入选英格兰国家队有哪些?!',
                 '',
                 ' ',
                 'aaaa',
                 '123',
                 '谁?',
                 '?',
                 '你好',
                 'hello',
                 # '哪名球员顶级联赛冠军最多',
                 '哪些球员球队如今不在顶级联赛',
                 '哪些球员的俱乐部是死敌',
                 '梅西效力于哪家俱乐部',
                 '哪些球员是俱乐部队友',
                 '哪些球员的儿子也是球员',
                 '谁儿子是守门员',
                 '谁的儿子是前锋',
                 '哪名球员当过美国国家队主教练呢',
                 '哪些西德球员是俱乐部队友',
                 '哪些德国球员是俱乐部队友',
                 '哪些英格兰球员是俱乐部队友',
                 '哪些球员效力于同一个俱乐部啊',
                 '两队球员效力于哪些俱乐部',
                 '西德球员效力于哪些俱乐部',
                 '英格兰球员效力于哪些俱乐部',
                 '哪些球员效力于科隆',
                 '哪些英格兰球员效力于曼联',
                 '哪些西德球员效力于拜仁',
                 '克林斯曼的儿子是踢什么位置的',
                 '里德尔的儿子是踢什么位置的',
                 '科普克的儿子是踢什么位置的',
                 '沃克的儿子是踢什么位置的',
                 '霍吉的儿子是踢什么位置的',
                 '贝克汉姆的儿子是踢什么位置的',
                 '场上哪些球员是俱乐部队友',
                 '场上哪些西德球员是俱乐部队友',
                 '场上哪些英格兰球员是俱乐部队友',
                 '场上球员效力于哪些俱乐部',
                 '场上两队球员效力于哪些俱乐部',
                 '场上西德球员效力于哪些俱乐部',
                 '场上英格兰球员效力于哪些俱乐部',
                 '场上哪些球员效力于国米',
                 '场上哪些德国球员效力于云达不来梅',
                 '场上哪些英格兰球员效力于利物浦',
                 '场上哪些球员俱乐部是死敌',
                 '哪些英格兰球员俱乐部是死敌',
                 '哪些西德球员俱乐部是死敌',
                 '马特乌斯的妻子是谁',
                 '马特乌斯现在的妻子是谁',
                 '贝克汉姆现在的妻子是谁',
                 '莱因克尔离过几次婚',
                 '哪个球员离婚次数最多',
                 '场上哪个球员离婚次数最多',
                 '哪个球员老婆最漂亮',
                 '哪些球员的球队现在不在顶级联赛',
                 '场上哪些球员球队如今不在顶级联赛',
                 '场上哪些英格兰球员球队如今不在顶级联赛',
                 '哪些德国球员球队如今不在顶级联赛',
                 '德甲有哪些参赛球队',
                 '英超现在有哪些参赛球队',
                 '德甲有哪些俱乐部',
                 '英甲有哪些俱乐部',
                 '德甲现在有哪些俱乐部',
                 '英超现在有哪些俱乐部',
                 '哪些球员的俱乐部',
                 '克林斯曼的俱乐部',
                 '场上哪些球员效力的球队是死敌',
                 '哪些球员效力的球队是死敌',
                 '场上哪些球员当时所在球队是死敌',
                 '哪些球员效力的球队是死敌',
                 '哪些西德球员效力的球队是死敌',
                 '哪些英格兰球员效力球队是死敌',
                 '哪些英格兰球员当时效力球队是死敌',
                 '哪些球员当时所在的球队已经不在顶级联赛了',
                 '哪些西德球员当时所在球队已经不在顶级联赛',
                 '场上哪些球员当时所在的球队已经不在顶级联赛了',
                 '场上哪些西德球员当时所在球队已经不在顶级联赛',
                 '哪些球员效力于云达不莱梅',
                 '哪些球员效力于多特蒙德',
                 '哪些球员效力于女王公园巡游者',
                 '梅西的身高',
                 '克林斯曼的儿子',

                 )

    def test_process_question_answer(self):
        question_answer = process(self.questions)
        print('test() in question_test.py')
        print('Question and answer after answer generation:')
        for question, question_in in question_answer.items():
            print(question, ":", question_in.answer)
        print()

    def test_process_single_question(self):
        question_answer = single_question.process(self.questions)
        print('test() in question_test.py')
        print('Question and answer after answer generation:')
        for question, question_in in question_answer.items():
            print(question, ":")
            print(question_in.answer)
            print('\n')
