class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

def alpha_beta_pruning(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or not node.children:
        return node.value

    if maximizing_player:
        max_val = float('-inf')
        for child in node.children:
            val = alpha_beta_pruning(child, depth - 1, alpha, beta, False)
            max_val = max(max_val, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break  # Beta cutoff
        return max_val
    else:
        min_val = float('inf')
        for child in node.children:
            val = alpha_beta_pruning(child, depth - 1, alpha, beta, True)
            min_val = min(min_val, val)
            beta = min(beta, val)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_val




