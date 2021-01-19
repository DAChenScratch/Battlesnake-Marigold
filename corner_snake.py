from utilities import getBodies, trapped
from try_other_snakes import other_can_trap
def tryCorner(data, myhead, snakes):
  #moves[a]
  for thishead in snakes:
    if thishead != myhead:
      if other_can_trap(data, thishead['head'], data['you']['head'], thishead['body']):
        return True
  return False
#trapped(bodies, target, width, height, shouldPrint

def can_trap(data, heads, target):
  #my target
  for head in heads:
    bodies = getBodies(data)
    bodies.append(target)
    if trapped(bodies, head, data, False):
      return True
    else:
      return False
