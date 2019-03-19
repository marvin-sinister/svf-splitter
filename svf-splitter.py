#!/usr/bin/env python3
INFILE = 'input.svf'

segment_size = int(16000/4)
line_length = 100

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def convert_payload(payload):
  command = 'SDR %d TDI (' % (segment_size * 4)
  remaining_payload = len(payload)
  i = 1;
  while remaining_payload > segment_size:
    print(command, end = '')
    print_payload(payload[((-i)*segment_size):remaining_payload])
    i = i + 1;
    remaining_payload = remaining_payload - segment_size
  if remaining_payload:
    command = 'SDR %d TDI (' % (remaining_payload * 4)
    print(command, end = '')
    print_payload(payload[:remaining_payload])

def print_payload(payload):
  lines = list(chunkstring(payload, line_length))
  print(''.join(lines[0:1]))
  for line in lines[1:-1]:
    print('        ', end='')
    print(line)
  print('        ', end='')
  print(''.join(lines[-1:]), end='')
  print(');')
  print('')

def main():
  with open(INFILE, 'r') as f:
    lines = f.readlines()
  # you may also want to remove whitespace characters like `\n` at the end of each line
  lines = [x.strip() for x in lines]

  in_payload = False
  payload_length = 0
  payload = ''

  for line in lines:
    if 'TDI' in line:
      if line.endswith(';'):
        print(line)
        continue
      in_payload = True
      payload_length = int(line.split()[1])
      if line.split()[3].endswith(')'):
        in_payload = False
        print(line)
      else:
        payload = line.split()[3][1:]
    elif in_payload:
      if line.endswith(';'):
        payload = ''.join([payload, line.strip()[:-2]])
        convert_payload(payload)
        payload = ''
        in_payload = False
      else:
        payload = ''.join([payload, line.strip()])

    else:
      print(line)

main()
