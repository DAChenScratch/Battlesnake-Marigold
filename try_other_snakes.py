from utilities import assign, getBodies, getPossibleMoves
from maths import distance_between

#safe(target, oh, ob, myh, mb)
      
def other_head_on_head(target, others):
  for head in others:
    theirSpots = assign(head)
    for spot in theirSpots:
      if round(distance_between(spot, target)) < 2:
        return False

  return True



def other_can_trap(data, myhead, thisHead, mybody):
  moves = assign(thisHead)
  worst_scenario = 999999999
  for a in range(4):
    bodies = getBodies(data).copy()
    bodies.append(moves[a])
    #first_time = getPossibleMoves(bodies, dict_moves[a], data, mybody)
    thismove = getPossibleMoves(bodies, myhead, data, mybody, True)
    if thismove < worst_scenario and thismove >0:
      worst_scenario = thismove
  if worst_scenario <len(mybody):
    return True
  else:
    return False