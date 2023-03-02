'''
Merge network routing path configuration
'''
W = 5 #merge network width
H = 11 #merge network height

# test merge
# Paths = [
#     ((0,0),(0,1)),
#     ((0,1),(0,2)),
#     ((1,0),(1,1)),
#     ((1,1),(0,1)),
#     ((2,0),(2,1)),
#     ((2,1),(1,1)),
#     ((2,2),(1,2)),
#     ((1,2),(1,1))
# ]

# test virtual vgg16
# Paths = [
#     ((5,0),(6,0)),
#     ((6,1),(5,1)),
#     ((4,1),(3,1)),
#     ((2,1),(1,1)),
#     ((0,1),(0,2)),
#     ((0,2),(1,2)),
#     ((2,2),(1,2)),
#     ((3,2),(4,2)),
#     ((5,2),(4,2)),
#     ((6,2),(5,2)),
#     ((6,3),(5,3)),
#     ((5,3),(4,3)),
#     ((4,3),(3,3)),
#     ((2,3),(1,3)),
#     ((1,3),(0,3)),
#     ((0,3),(0,4)),
#     ((1,4),(2,4)),
#     ((3,4),(2,4)),
#     ((4,4),(3,4)),
#     ((5,4),(5,5)),
#     ((6,4),(6,5)),
#     ((6,5),(5,5)),
#     ((4,5),(3,5)),
#     ((3,5),(2,5)),
#     ((2,5),(2,6)),
#     ((1,5),(1,6)),
#     ((0,5),(0,6)),
#     ((1,6),(0,6)),
#     ((3,6),(3,7)),
#     ((4,6),(4,7)),
#     ((4,7),(3,7)),
#     ((5,6),(5,7)),
#     ((6,6),(6,7)),
#     ((6,7),(5,7))
# ]

# # test virtual vgg16 v2
# Paths = [
#     ((5,0),(6,0)),
#     ((6,1),(5,1)),
#     ((4,1),(3,1)),
#     ((2,1),(1,1)),
#     ((0,1),(0,2)),
#     ((0,2),(1,2)),
#     ((2,2),(1,2)),
#     ((3,2),(4,2)),
#     ((5,2),(4,2)),
#     ((6,2),(5,2)),
#     ((6,3),(5,3)),
#     ((5,3),(4,3)),
#     ((4,3),(3,3)),
#     ((2,3),(1,3)),
#     ((1,3),(0,3)),
#     ((0,3),(0,4)),
#     ((1,4),(2,4)),
#     ((2,4),(3,4)),
#     ((3,4),(4,4)),
#     ((5,4),(5,5)),
#     ((6,4),(6,5)),
#     ((6,5),(5,5)),
#     ((4,5),(3,5)),
#     ((3,5),(2,5)),
#     ((2,5),(2,6)),
#     ((1,5),(1,6)),
#     ((0,5),(0,6)),
#     ((1,6),(0,6)),
#     ((3,6),(3,7)),
#     ((4,6),(4,7)),
#     ((4,7),(3,7)),
#     ((5,6),(5,7)),
#     ((6,6),(6,7)),
#     ((6,7),(5,7))
# ]

# test no contention
Paths = [
((4, 1), (3, 1)),
((2, 1), (1, 1)),
((0, 1), (0, 2)),
((1, 2), (2, 2)),
((4, 2), (3, 2)),
((3, 2), (3, 3)),
((4, 3), (3, 3)),
((0, 3), (0, 4)),
((1, 3), (0, 3)),
((2, 3), (1, 3)),
((2, 4), (3, 4)),
((3, 4), (4, 4)),
((1, 4), (2, 4)),
((3, 5), (2, 5)),
((4, 5), (3, 5)),
((2, 5), (1, 5)),
((1, 6), (2, 6)),
((0, 5), (0, 6)),
((0, 6), (1, 6)),
((3, 6), (3, 7)),
((4, 6), (4, 7)),
((4, 7), (3, 7)),
((0, 7), (0, 8)),
((1, 7), (0, 7)),
((2, 7), (1, 7)),
((2, 8), (3, 8)),
((3, 8), (4, 8)),
((1, 8), (2, 8)),
((2, 9), (1, 9)),
((3, 9), (2, 9)),
((4, 9), (3, 9)),
((1, 10), (2, 10)),
((0, 9), (0, 10)),
((0, 10), (1, 10))
]
