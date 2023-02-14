'''
Verify that only E2E-FC can eliminate all loops,
and there is no need to apply UBM any more.
FAILED!!!
'''
if __name__ == "__main__":
    from noc_mapper import NoC_Mapper
    from deadlock_analyzer import DeadlockAnalyzer
    from deadlock_killer import DeadlockKiller
    while True:
        maper = NoC_Mapper(5,11,[1,1,1,1,1,2,2,2,4,4,4,4,4],[1,1,1,1,1,1,1,2,2,2,2,2,2])
        maper.Run_Mapping()
        dla = DeadlockAnalyzer(5,11,maper.cast_paths,maper.merge_paths,log=None)
        dla.Run_Analyzing()
        dlk = DeadlockKiller(5,11,maper.merge_nodes,maper.cast_targets,maper.cast_paths,dla.sloops,dla.cloops)
        dlk.Run_Killing()
        print("remain_loops:",len(dlk.remain_loops))
        if len(dlk.remain_loops) > 0:
            print("Exception!!!remain_loops")
            dla.Plot_Loops()
            dlk.Plot_Remain_Loops()
            break