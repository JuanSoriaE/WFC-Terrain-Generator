from PIL import Image
import queue
import heapq
import random

# 0: land | 1: sand | 2: water
COLORS = {0: '#1b9908', 1: '#c2b280', 2: '#1c4894'}
OFFS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
# OFFS = [(0, -1), (-1, 0), (1, 0), (0, 1)]
N, M = 50, 50
W, H = 500, 500
ADJ_DIC = {0: [0, 1], 1: [0, 1, 2], 2: [1, 2]}
TOTAL = {0, 1, 2}
INI_STATE = [0, 1, 2]

def buildImg(grid):
    main_img = Image.new('RGB', size=(W, H), color=(0, 0, 0))
    sub_img_w, sub_img_h = int(W / M), int(H / N)
    
    for r in range(N):
        for c in range(M):
            x, y = int(c * (W / M)), int(r * (H / N))
            color = COLORS[grid[r][c][0]]
            sub_img = Image.new('RGB', size=(sub_img_w, sub_img_h), color=color)
            main_img.paste(sub_img, box=(x, y))
    
    main_img.save('sample.jpg')
    main_img.show()

def BFS(grid, r, c, collapsed):
    # POSSIBLE =   {0: [0, 1], 1: [0, 1, 2], 2: [1, 2]}
    q = queue.Queue()
    q.put((r, c))

    while not q.empty():
        cur_r, cur_c = q.get()
        poss = []

        # Get NO possible states
        for state in grid[cur_r][cur_c]:
            for poss_state in ADJ_DIC[state]:
                poss.append(poss_state)
        no_poss = list(TOTAL - set(poss))

        for x, y in OFFS:
            new_r, new_c = r + y, c + x
            if min(new_r, new_c) < 0 or new_r >= N or new_c >= M or collapsed[new_r][new_c]:
                continue

            og_len = len(grid[new_r][new_c])
            for no_poss_state in no_poss:
                if no_poss_state in grid[new_r][new_c]:
                    grid[new_r][new_c].remove(no_poss_state) # Dont consider any more impossible states

                if len(grid[new_r][new_c]) == 1:
                    collapsed[new_r][new_c] = True
                    break
            
            if len(grid[new_r][new_c]) != og_len:
                q.put((new_r, new_c))

def getRandomState(grid, r, c, collapsed):
    # Get random choice but with priority based on the neighbors
    cnt = {}
    for i in range(len(TOTAL)):
        cnt[i] = 0

    for x, y in OFFS:
        new_r, new_c = r + y, c + x
        if min(new_r, new_c) >= 0 and new_r < N and new_c < M and collapsed[new_r][new_c]:
            cnt[grid[new_r][new_c][0]] += 1
    
    choice_list = []
    for i in range(len(TOTAL)):
        if i not in grid[r][c]:
            continue
        choice_list += [i for j in range(cnt[i])]
    
    return [random.choice(grid[r][c] + choice_list)]

def WFC(grid):
    collapsed = [[False for j in range(M)] for i in range(N)]
    heap = [] # (entropy, row, col)

    for r in range(N):
        for c in range(M):
            heap.append([len(TOTAL), r, c]) # Initially all the cells can be in the 3 states
    
    heapq.heapify(heap)

    while len(heap) > 0:
        e, r, c = heapq.heappop(heap) # Get the cell with least entropy and collapse it
        if (collapsed[r][c] == True):
            continue

        collapsed[r][c] = True
        grid[r][c] = getRandomState(grid, r, c, collapsed)
        BFS(grid, r, c, collapsed) # Propagate constraints

def main():
    grid = [[INI_STATE.copy() for j in range(M)] for i in range(N)]
    
    WFC(grid)
    buildImg(grid)

if __name__ == "__main__":
    main()