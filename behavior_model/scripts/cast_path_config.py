'''
Cast network routing path configuration
'''
W = 3 #cast network width
H = 3 #cast network height
RT_DEPTH = 16 #routing table depth
SID_WIDTH = 10 #data width of stream ID

PATH_DICT = dict()

# ----------------------------------------------------------------------------------------------------- example begin
# PATH_DICT['0,0'] = [(       2       ,       0       ,       0       ),(...),(...),...]
#             ^               ^               ^               ^                 ^
#       router position  input port      output port      stream ID        other paths
# ----------------------------------------------------------------------------------------------------- example end
# Note: A stream is a multicast tree, every multicast tree in the cast network has a unique stream ID.
# Port specification: 0-local, 1-west, 2-east, 3-vert0, 4-vert1.

PATH_DICT[(0,0)] = [(2,0,1)]
PATH_DICT[(1,0)] = [(2,3,1),(2,1,1),(2,0,1)]
PATH_DICT[(2,0)] = [(0,1,1),(0,3,1)]
PATH_DICT[(0,1)] = [(2,0,1)]
PATH_DICT[(1,1)] = [(3,1,1),(3,3,1)]
PATH_DICT[(2,1)] = [(3,0,1)]
PATH_DICT[(0,2)] = [(2,0,1)]
PATH_DICT[(1,2)] = [(3,1,1),(3,0,1)]
PATH_DICT[(2,2)] = []


