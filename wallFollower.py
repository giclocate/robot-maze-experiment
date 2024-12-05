from pyamaze import maze, agent, COLOR

#rotacionar no sentido horário
def RCW():
    global direction
    k = list(direction.keys())
    v = list(direction.values())
    v_rotated = v[-1:] + v[:-1]  
    direction = dict(zip(k, v_rotated))

#rotacionar no sentido anti-horário
def RCCW():
    global direction
    k = list(direction.keys())
    v = list(direction.values())
    v_rotated = v[1:] + v[:1]  # Rotação correta
    direction = dict(zip(k, v_rotated))

#mover para frente de acordo com a direção atual
def moverFrente(cell):
    if direction['foward'] == 'E':
        return (cell[0], cell[1] + 1), 'E'
    if direction['foward'] == 'W':
        return (cell[0], cell[1] - 1), 'W'
    if direction['foward'] == 'N':
        return (cell[0] - 1, cell[1]), 'N'
    if direction['foward'] == 'S':
        return (cell[0] + 1, cell[1]), 'S'

# implementação do seguidor de paredes
def seguidorParedes(m):
    global direction
    direction = {'foward': 'N', 'left': 'W', 'back': 'S', 'right': 'E'}
    currCell = (m.rows, m.cols)
    caminho = ''

    while True:
        if currCell == (1, 1):  
            break
        if m.maze_map[currCell][direction['left']] == 0:  
            if m.maze_map[currCell][direction['foward']] == 0:  
                RCW() 
            else:
                currCell, d = moverFrente(currCell)  
                caminho += d
        else:
            RCCW()  
            currCell, d = moverFrente(currCell) 
            caminho += d
    caminho2=caminho
    #remove movimentos redundantes
    while 'EW' in caminho or 'WE' in caminho or 'NS' in caminho or 'SN' in caminho:
        caminho = caminho.replace('EW', '')
        caminho = caminho.replace('WE', '')
        caminho = caminho.replace('NS', '')
        caminho = caminho.replace('SN', '')

    return caminho, caminho2

#função principal
if __name__ == '__main__':
    labirinto = maze(10, 10) 
    labirinto.CreateMaze(loopPercent=20) 

    agente = agent(labirinto, shape='arrow', color='blue', footprints=True)
    agente2 = agent(labirinto, shape='arrow', footprints=True, color=COLOR.green)
    caminho, caminho2 = seguidorParedes(labirinto) 
    labirinto.tracePath({agente: caminho2})  
    labirinto.tracePath({agente2: caminho})  

    # Calcula os scores
    score_agente1 = len(caminho2)
    score_agente2 = len(caminho)
    
    # Exibe os scores
    print(f"Score do Agente 1 (caminho completo): {score_agente1} movimentos")
    print(f"Score do Agente 2 (caminho simplificado): {score_agente2} movimentos")
    

    labirinto.run()  
