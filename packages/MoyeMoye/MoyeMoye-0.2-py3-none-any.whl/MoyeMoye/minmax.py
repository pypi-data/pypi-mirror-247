import math
 
def minimax (curDepth, nodeIndex,maxTurn, scores, targetDepth):
 
    
    if (curDepth == targetDepth): 
        return scores[nodeIndex]
     
    if (maxTurn):
        return max(minimax(curDepth + 1, nodeIndex * 2, 
                    False, scores, targetDepth), 
                   minimax(curDepth + 1, nodeIndex * 2 + 1, 
                    False, scores, targetDepth))
     
    else:
        return min(minimax(curDepth + 1, nodeIndex * 2, 
                     True, scores, targetDepth), 
                   minimax(curDepth + 1, nodeIndex * 2 + 1, 
                     True, scores, targetDepth))
     


 
 