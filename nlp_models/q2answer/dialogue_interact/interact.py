"""
@Project   : CubeGirl
@Module    : interact.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/23/18 1:11 PM
@Desc      : 
"""
import copy
import sys
import datetime
import pickle as pkl

N = 1000
# uname = raw_input("Please Enter User Name: ").lower()
# uname = 'user0'
uname = input("Please Enter User Name: ").lower()
uid = hash(uname)
cdir = "sessions/" + str(uid) + '_' +\
       datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"/"

try:
    for i in range(N):
        print("------------------------------------------------------------")
        print("Dialog %d" % i)
        dia = []
        curr_agent = agent
        # 引出AgentSimpleRLAllActNoDB in agent_simple_nodb.py
        dia.append(curr_agent)
        dialog_manager = DialogManager(curr_agent, user_sim, db_full, db_inc,
                                       movie_kb, verbose=False)
        # 引出DialogManager in dialogue_manager.py
        utt = dialog_manager.initialize_episode()
        dia.append(copy.deepcopy(utt))
        total_reward = 0
        while True:
            episode_over, reward, utt, agact = dialog_manager.next_turn()
            dia.append(agact)
            dia.append(copy.deepcopy(utt))
            total_reward += reward
            if episode_over:
                break
        pkl.dump(dia, open(cdir+str(i)+".p", 'w'))
except KeyboardInterrupt:
    sys.exit()
