"""
@Project   : CubeGirl
@Module    : run_script.py
@Author    : Deco [deco@cubee.com]
@Created   : 3/26/18 5:03 PM
@Desc      : 运行python脚本，python run_script.py
"""

from Daka.chatbot.logic.knowledge_graph.one_hot_encoding import intent_MLP
from Daka.chatbot.logic.knowledge_graph.one_hot_encoding import syntac_MLP

if __name__ == '__main__':

    # intent_MLP.select_words()
    syntac_MLP.select_words()
