from collections import namedtuple
from operator import itemgetter
from pprint import pformat

class Node(namedtuple('Node', 'location left_child right_child')):
    def __repr__(self):
        return pformat(tuple(self))

def kdtree(point_list, depth=0):
    try:
        k = len(point_list[0]) # assumes all points have the same dimension
    except IndexError as e: # if not point_list:
        return None
    # Select axis based on depth so that axis cycles through all valid values
    axis = depth % k
 
    # Sort point list and choose median as pivot element
    point_list.sort(key=itemgetter(axis))
    median = len(point_list) // 2 # choose median
 
    # Create node and construct subtrees
    return Node(
        location=point_list[median],
        left_child=kdtree(point_list[:median], depth + 1),
        right_child=kdtree(point_list[median + 1:], depth + 1)
    )

def main():
    """Example usage"""
    point_list = [(2,3), (5,4), (9,6), (4,7), (8,1), (7,2)]
    tree = kdtree(point_list)
    print(tree)

if __name__ == '__main__':
    main()

ed2k://|file|Frozen.2013.冰雪奇缘.双语字幕.HR-HDTV.AC3.1024X576.x264.mkv|1675792217|160c22039ef7a0c77d312a776f5b31e2|h=a5pftwl5ovnbxrje6s4yekoja5kdkkl3|/
ed2k://|file|[剃刀边缘].The.Razors.Edge.1946.DVDRip.XviD-PROMiSE.cd2.avi|734380032|d5c4f74aaa5af4a07b1167ee09e3d182|/

http://rapidgator.net/file/12ec642dd329e9ac04921254767d21b6/The.Razors.Edge.1946.DVDRip.XviD-Wolfman.avi.html
