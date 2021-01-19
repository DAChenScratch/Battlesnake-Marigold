from utilities import assign, getBodies, getHeads, getPossibleMoves, indvBodies, areas_near_heads, smaller_snakes_get_heads, get_dangerous_heads, onlyOneWayToGo
#from get_closest import closest
from corner_snake import tryCorner, can_trap
from maths import distance_between
from try_other_snakes import other_can_trap
from get_closest import closest
def best(data, scores):
  moves = ['up', 'down', 'left', 'right']
  dict_moves = assign(data['you']['head'])
  points_moves = [150, 150, 150, 150]
  #print('DICT MOVES:', dict_moves)
  bodies = getBodies(data)
  heads = getHeads(data)
  myhead = data['you']['head']
  mybody = data['you']['body']
  #mytail = data['you']['body'][len(data['you']['body']) - 1]
  food = data['board']['food']
  health = data['you']['health']
  height = data['board']['height']
  width = data['board']['width']
  snakes = data['board']['snakes']
  center = {
    'x':round(width/2),
    'y':round(height/2)
  }
  small_heads = smaller_snakes_get_heads(data)
  indv_bodies = indvBodies(data)
  head_areas = areas_near_heads(small_heads, indv_bodies, mybody, myhead)
  danger_heads = get_dangerous_heads(data)
  me_smallest = 0
  for snake in snakes:
    if len(snake['body']) >= len(mybody):
      me_smallest +=1
  if me_smallest == len(snakes):
    me_smallest = 2
  else:
    me_smallest = 1/3
  #print('AM I THE SMALLEST?', me_smallest)
  best_move_for_space = None
  num_best_move_space = 0
  for trymoves in dict_moves:
    thismoves = getPossibleMoves(bodies, trymoves, data, mybody, True)
    if thismoves > num_best_move_space:
      num_best_move_space = thismoves
      best_move_for_space = trymoves
  #print(num_best_move_space)
  for a in range(4):
    if dict_moves[a] in bodies or not -1<dict_moves[a]['x']<width or not -1<dict_moves[a]['y']<height:
      points_moves[a] = -999999999999 #350
    else:
      first_time = getPossibleMoves(bodies, dict_moves[a], data, mybody, True)-len(mybody)
      #points_moves[a] += (first_time - len(mybody))*1.5 #1.5
      if first_time < 1:
        print('OOF:', moves[a], '\n', first_time)
        points_moves[a] -=600
      else:
        if me_smallest == 2 or health <36:
          points_moves[a] -= closest(dict_moves[a], food, heads) * 20 *me_smallest

      if me_smallest !=2 and health>30:
        points_moves[a] -= closest(dict_moves[a], small_heads, heads) * 15
          #print('FOR MOVE:', moves[a] + ", THE DISTANCE TO THIS HEAD IS", distance_between(dict_moves[a], myhead))
      i_can_corner = False
      if tryCorner(data, myhead, snakes):
        print('Cornering!')
        points_moves[a] +=200
      if dict_moves[a] in head_areas:
        #60
        points_moves[a] +=60
      for snakehead in snakes:
        if can_trap(data, heads, dict_moves[a]):
          points_moves[a] +=140 #55
        if other_can_trap(data, dict_moves[a], snakehead['head'], data['you']['body']) < len(mybody) and snakehead['body'] != mybody:
          points_moves[a] -=250
        bc = bodies.copy()
        bc.append(dict_moves[a])
        if getPossibleMoves(bc, snakehead['head'], data, snakehead['body'], True) < getPossibleMoves(bodies, snakehead['head'], data, snakehead['body'], True) and not snakehead['body'] == mybody:
          print('I love constricting')
          points_moves[a] +=100
        if onlyOneWayToGo(data, snakehead['head'], bc, False) and not snakehead['body'] == mybody:
          points_moves[a] +=90
        
        #getPossibleMoves(bodies, startCoord, data, mybody, trapped = False, shouldprint = False)
      
      for danger in danger_heads:
        #points_moves[a] +=round(distance_between(danger, dict_moves[a])) * 15
        
        #if distance_between(danger, dict_moves[a]) <4:
        #swcores[9] = 2.5
          #points_moves[a] -= 60
        if distance_between(danger, dict_moves[a]) <=3.5:
        #swcores[9] = 2.5
          points_moves[a] -= 150
        if distance_between(danger, dict_moves[a]) <2:
        #swcores[9] = 2.5
          points_moves[a] -= 300
      
      
      if num_best_move_space < len(mybody):
        if dict_moves[a] == best_move_for_space:
          points_moves[a] +=150 #60
      
      #if not other_head_on_head(dict_moves[a], heads):
        #points_moves[a] -=70
      if dict_moves[a] in data['board']['hazards']:
        points_moves[a] -= 100
      #if onlyOneWayToGo(data, dict_moves[a], bodies, False):
        #points_moves[a] -=30
  return moves[points_moves.index(max(points_moves))]
  
