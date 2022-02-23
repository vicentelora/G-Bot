def find_all(a_str, sub):
  start = 0
  while True:
    start = a_str.find(sub, start)
    if start == -1: 
      return
    yield start
    start += len(sub)

def add_line_at(i, string):
  string = string[:i] + "\n" + string[i:]
  return string

def add_lines_at(i, string, num_lines):
  string = string[:i] + "\n"*num_lines + string[i:]
  return string

def remove_excess_lines(string):

  while string[-1] == "\n":
    string = string[:(len(string) - 1)]
  while string[0] == "\n":
    string = string[1:]

  return string