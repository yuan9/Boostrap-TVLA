
import numpy as np
import os
import re
import struct

_fname = None
_fhandle = None
_data_width = None

def reset_reader():
  global _fname, _fhandle, _data_width
  if _fhandle:
    _fhandle.close()
  _fname = None
  _fhandle = None
  _data_width = None

def read_trace(filename, offset=0, samples=-1, start=0, stop=0):
  global _fname, _fhandle, _data_width
  data_type = {
      8  : np.uint8,
      16 : np.uint16,
      32 : np.uint32,
      64 : np.float64,
      }

  if _fname != filename:
    reset_reader()
    _fname = filename
    _fhandle = open(_fname, 'rb')
    magic_number = struct.unpack('h', _fhandle.read(2))[0]
    sample_rate  = struct.unpack('f', _fhandle.read(4))[0]
    range_mv     = struct.unpack('i', _fhandle.read(4))[0]
    offset_mv    = struct.unpack('f', _fhandle.read(4))[0]
    data_width   = struct.unpack('B', _fhandle.read(1))[0]
    offset_file  = struct.unpack('i', _fhandle.read(4))[0]
    sub_version  = struct.unpack('B', _fhandle.read(1))[0]
    status_flag  = struct.unpack('B', _fhandle.read(1))[0]
    pad          = _fhandle.read(3)
    _data_width  = data_width

  start_pos = max(0, offset * _data_width // 8)
  _fhandle.seek(start_pos + 24, 0) # from the beginning

  output = np.fromfile(_fhandle, data_type[_data_width], samples)

  if (start == 0) and (stop == 0):
    return output
  else:
    return output[start:stop]

def parse_metadata_line(line):
  line = line.strip()
  offset_re = re.compile(r'^(?P<offset>[+-]?\d+)(,\s+)?(?P<qvalue>[+-]?(\d+(\.*\d*)?|\.\d+)([eE][+-]?\d+)?\)?)?')
  classifiers_re = re.compile(r'(?P<classifiers>\{(0x)?[\da-fA-F]+\})')
  
  #qvalue_re = re.compile(r'(\(\Q|qval)=\s*(?P<qvalue>[+-]?(\d+(\.*\d*)?|\.\d+)([eE][+-]?\d+)?)')
  #qvaluefield_re = re.compile(r'(?P<qvaluefield>(\(\Q|qval)=\s*[+-]?(\d+(\.*\d*)?|\.\d+)([eE][+-]?\d+)?\)?)')
  #qvaluefield_re = re.compile(r'(?P<qvalueheader>(qval=)\s*(?P<qvalue>[+-]?(\d+(\.*\d*)?|\.\d+)([eE][+-]?\d+)?)')

  ret_dict = {}
  columns = line.split()
  first_three = ' '.join(columns[0:3]) # offset must be within first three columns
  offset_m = offset_re.search(first_three)
  qvalue_str = None

  if offset_m:
    offset = offset_m.group('offset')

    filename_idx = 2 if qvalue_str else 1
    ret_dict['filename'] = columns[filename_idx].strip()

    line = offset_re.sub('', line).strip()
    line = line.replace(ret_dict['filename'], '').strip()

    if qvalue_str: ret_dict['qvalue'] = qvalue_str
    ret_dict['offset'] = offset
  else:
    ret_dict['filename'] = columns[0].strip()
    line = line.replace(ret_dict['filename'], '').strip()

  classifiers_m = classifiers_re.search(line)
  if classifiers_m:
    ret_dict['classifiers'] = classifiers_m.group('classifiers')
    line = classifiers_re.sub('', line).strip()

  ret_dict['other'] = line

  return ret_dict

