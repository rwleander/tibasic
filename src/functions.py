#  evaluate functions

#  get function results

def evaluate(parts):
  if len(parts) == 0:
    return [0, 'Bad function']
    
  func = parts[0]
  if func == 'SQR':
    return doSqr(parts)
  
  return [0, 'Unknown function']


#  SQR - square root

def doSqr (parts):
  if len(parts) < 2:
    return [0, 'Bad argument']
      
  n = parts[1]
  if type(n) != float or n < 0:
    return [0, 'Bad argument']
  
  sqr = n ** 0.5
  return [sqr, 'OK']
    
  