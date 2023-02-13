'''
A test script to test the optimization of cast communication plan
The object is to reduce contentions of cast communication as much as possible
'''
from mapper import Mapper
from deadlock_analyzer import DeadlockAnalyzer
from mapplot import *

if __name__ == "__main__":
    W = 7
    H = 8
    maper = Mapper(W,H,[1,1,1,1,1,2,2,2,4,4,4,4,4],[1,1,1,1,1,1,1,2,2,2,2,2,2])
    con_accu = 10000
    cnt = 0
    while True:
        cnt += 1
        maper.Run_Mapping()
        # con = maper.Get_Contention_Level()
        dla = DeadlockAnalyzer(W,H,maper.cast_paths,maper.merge_paths)
        dla.Run_Analyzing()
        if len(dla.sloops) == 0:
            print("Finished!!\n\n")
            print(f"find {len(dla.cloops)} complex loop(s)")
            print("accumulated_contention_level:",maper.Get_Contention_Level())
            dla.Plot_Loops()
            break

        # if con < con_accu:
        #     con_accu = con
        #     print("\n\nstarting iteration:",cnt)
        #     print("accumulated_contention_level:",con)
        #     plt.figure(figsize=(maper.w,maper.h))
        #     plot_routers(maper.w,maper.h)
        #     G,pos,el = construct_cdg(maper.w,maper.h,maper.cast_paths,maper.merge_paths)
        #     ec = get_edge_colors(G)
        #     nx.draw(G, pos, node_size = 20,width=1, arrowsize=10,node_color='black',edge_color='blue',arrowstyle='-|>')
        #     plt.savefig(f'/mnt/c/git/nvcim-comm/behavior_model/scripts/opt_cast/contention_level_'+str(con_accu),
        #                     dpi=400,bbox_inches='tight')
        #     print(f"Finished saving the image")

        #     dla = DeadlockAnalyzer(W,H,maper.cast_paths,maper.merge_paths,log=file_name)
        #     dla.Run_Analyzing()
            
        #     print(f"find {len(dla.cloops)} complex loop(s)")
        #     print(f"find {len(dla.sloops)} simple loop(s)")     

        # if con_accu <= 0:
        #     print("cast_paths = dict()")
        #     for k,v in maper.cast_paths.items():
        #         print(f"cast_paths[{k}]={v}")
        #     print("merge_paths = [")
        #     for i in maper.merge_paths:
        #         print(i,",")
        #     print("]")
        #     break
    
