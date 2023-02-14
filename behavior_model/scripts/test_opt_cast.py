'''
A test script to test the optimization of cast communication plan
The object is to reduce contentions of cast communication as much as possible
'''
from noc_mapper import NoC_Mapper
from deadlock_analyzer import DeadlockAnalyzer

if __name__ == "__main__":
    W = 7
    H = 8
    maper = NoC_Mapper(W,H,[1,1,1,1,1,2,2,2,4,4,4,4,4],[1,1,1,1,1,1,1,2,2,2,2,2,2])
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
