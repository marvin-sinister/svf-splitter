#!/usr/bin/env python3
INFILE = 'led.svf'

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

def format_file():
  # read all lines from file
  with open(INFILE, 'r') as f:
    lines = f.readlines()
  # remove comments
  lines = [x.split('!')[0] for x in lines]
  lines = [x.split('//')[0] for x in lines]
  # remove leading and trailing spaces, and newlines
  lines = [x.strip() for x in lines]
  # convert whole file into single line
  file_in_line = ''
  for line in lines:
    # ignore empty lines
    if len(line) >  0:
      # because some commands are broken into multiple lines, we need to add space after closing brackets
      append_space = False
      if line.endswith(')'):
        append_space = True
      # append the line and convert all the arbitrary whitespaces to single space
      file_in_line = ''.join([file_in_line, ' '.join(line.split())])
      if append_space:
       file_in_line = file_in_line + ' '

  # split the line at semicolon, ignore whatever remains after last semicolon
  lines = file_in_line.split(';')[:-1]

  # return formated file
  return lines

def main():
  # read file
  lines = format_file()

  payload_length = 0
  payload = ''
  suffix = ''

  # iterate over lines
  for line in lines:
    # find command
    if line.startswith('SDR'):
      # get payload length
      payload_length = int(line.split()[1])
      # do we need to split the command
      if payload_length > segment_size:
        # get payload without brackets
        payload = line.split()[3].strip().lstrip('(').rstrip(')').strip()
        convert_payload(payload)
      else:
        print(line + ';')
    else:
      print(line + ';')
main()
