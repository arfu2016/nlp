"""
@Project   : CubeGirl
@Module    : module_test.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/19/17 11:31 AM
@Desc      : 测试脚本
"""
if __name__ == '__main__':
    from Daka.chatbot.logic.knowledge_graph.q2answer.sentence_parse_tree \
        import test
    test()

    from Daka.chatbot.logic.knowledge_graph.q2answer.question_test \
        import KnownQuestions

    KnownQuestions().test_process_single_question()

    # KnownQuestions().test_process_question_answer()

    # from Daka.chatbot.logic.knowledge_graph.q2answer.question_answer \
    #     import test
    # test()
