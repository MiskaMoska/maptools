class DeadlockKiller(object):

    def __init__(self,w,h,cloops):
        self.w = w
        self.h = h
        self.cloops = cloops

    @staticmethod
    def greedy_SCP(U:set,S:list,accum_U:set,ret:list):
        '''
        Greedy algorithm to solve set cover problem
        '''
        assert len(S) > 0, "fatal error when greedy_SCP"
        if accum_U == U:
            return 

        remain_U = U - accum_U
        cnt_list = []
        for Si in S:
            cnt = 0
            for ele in Si:
                if ele in remain_U:
                    cnt += 1
            cnt_list.append(cnt)
        idx = cnt_list.index(max(cnt_list))
        ret.append(S[idx])
        accum_U |= S.pop(idx)
        DeadlockKiller.greedy_SCP(U,S,accum_U,ret)




    def __get_UBMs(self)->set:
        '''
        Get the UBM channels through greedy SCP
        Remove an arbitary dependency in each cloop
        '''
        dep_union = set()
        for cloop in self.cloops:
            for dep in cloop:
                if dep

if __name__ == "__main__":
    dlk = DeadlockKiller(1,1,[1])
    U = set([1,2,3,4,5])
    S = [set([1,4,5]),set([1,2]),set([5]),set([2,3]),set([2,3,5])]
    ret = []
    dlk.greedy_SCP(U,S,set([]),ret)
    print(ret)

