def hungary(edges):
    result = set()
    lenA = max(edge[0] for edge in edges) + 1
    lenB = max(edge[1] for edge in edges) + 1

    def allVectorsGen():
        for x in xrange(lenA):
            yield x, None
        for x in xrange(lenB):
            yield None, x


    def getPath(inResult, startVector, path=(), pathUsedVectors=None):
        pathUsedVectors = pathUsedVectors or set()
        # No need to enumerate edge already in path.
        for edge in edges - set(path):
            if (edge in result) != inResult:
                continue
            vectors = set(((edge[0], None), (None, edge[1])))
            if not startVector in vectors:
                continue
            vectors.remove(startVector)
            endVector = vectors.pop()
            if endVector in pathUsedVectors:
                continue
            pathUsedVectors.add(endVector)
            path = path + (edge,)
            # Invert inResult, know & don't know of a & b
            subPath = getPath(not inResult, endVector, path, pathUsedVectors)
            if not subPath is None:
                return subPath
            elif len(path) % 2 == 1 and not endVector in usedVectors:
                return path
        return None
    
    usedVectors = set()
    while len(result) < min(lenA, lenB):
        for vector in allVectorsGen():
            if vector in usedVectors:
                continue
            path = getPath(False, vector)
            if not path is None:
                result ^= set(path)
                # Every path found, both start vector & end vector will be
                # removed from free vectors.
                usedVectors.add(vector)  # Start vector
                usedVectors.add(((path[-1][0] if vector[0] is None else None),
                                 (path[-1][1] if vector[1] is None else None)))
                # End vector
                break
        else:
            break

    return result

if __name__ == '__main__':
    print hungary(set([(0, 1), (0, 4),
                       (1, 1), (1, 2), (1, 3),
                       (2, 0), (2, 4),
                       (3, 0), (3, 1), (3, 4),
                       (4, 1)]))
