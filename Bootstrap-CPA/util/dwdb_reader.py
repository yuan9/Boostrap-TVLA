
import os
import re
import struct

import numpy as np

################################### CONVERSIONS
def uchar2char(arr):
  return np.subtract(arr, int(0x80), dtype=np.int8)

def char2uchar(arr):
  return arr.astype(np.uint8) + int(0x80)

def uchar2short(arr):
  return arr.astype(np.int16, copy=True) - int(0x80)

def uchar2double32(arr):
  return arr - np.float32(int(0x80))

def uchar2double64(arr):
  return arr - np.float64(int(0x80))

def ushort2short(arr):
  return np.subtract(arr, int(0x8000), dtype=np.int16)

def short2ushort(arr):
  return arr.astype(np.uint16) + int(0x8000)

def ushort2int(arr):
  return arr.astype(np.int32, copy=True) - int(0x8000)

def ushort2double32(arr):
  return arr - np.float32(int(0x8000))

def ushort2double64(arr):
  return arr - np.float64(int(0x8000))

def double2double(arr):
  return arr

################################### METADATA PARSER

def parse_metadata_line(line):
  line = line.strip()
  offset_re = re.compile(r'^(?P<offset>[+-]?\d+)(,\s+)?(?P<qvalue>[+-]?(\d+(\.*\d*)?|\.\d+)([eE][+-]?\d+)?\)?)?')
  classifiers_re = re.compile(r'(?P<classifiers>\{(0x)?[\da-fA-F]+\})')
  legacy_qvaluefield_re = re.compile(r'(?P<qvalueheader>\(\Q=\s*)(?P<qvalue>[+-]?(\d+(\.*\d*)?|\.\d+)([eE][+-]?\d+)?\)?)')
  #qvalue_re = re.compile(r'(\(\Q|qval)=\s*(?P<qvalue>[+-]?(\d+(\.*\d*)?|\.\d+)([eE][+-]?\d+)?)')
  #qvaluefield_re = re.compile(r'(?P<qvaluefield>(\(\Q|qval)=\s*[+-]?(\d+(\.*\d*)?|\.\d+)([eE][+-]?\d+)?\)?)')
  #qvaluefield_re = re.compile(r'(?P<qvalueheader>(qval=)\s*(?P<qvalue>[+-]?(\d+(\.*\d*)?|\.\d+)([eE][+-]?\d+)?)')

  ret_dict = {}
  columns = line.split()
  first_three = ' '.join(columns[0:3]) # offset must be within first three columns
  offset_m = offset_re.search(first_three)

  if offset_m:
    offset = offset_m.group('offset')

    legacy_qval_m = legacy_qvaluefield_re.search(line)

    qvalue_str = None
    if legacy_qval_m:
      qvalue_str = legacy_qval_m.group('qvalue')
      if qvalue_str:
        qvalue_str = qvalue_str.rstrip(')')
        line = legacy_qvaluefield_re.sub('', line).strip()
      ret_dict['filename'] = columns[1].strip()
    else:
      qvalue_str = offset_m.group('qvalue')
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

################################### FILE READER and WRITER
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

def read_trace(filename, offset=0, samples=-1):
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

  return np.fromfile(_fhandle, data_type[_data_width], samples)

def save_trace(filename, trace):
  data_width_dict = {
      np.dtype('uint8') : 8,
      np.dtype('uint16') : 16,
      np.dtype('uint32') : 32,
      np.dtype('float64') : 64,
      }

  trace = np.asanyarray(trace)
  trace = convert2dwfm(trace)
  dw = data_width_dict.get(trace.dtype)
  if not dw:
    raise TypeError("Only unsigned char, unsigned short and double types supported")

  with open(filename, 'wb') as f:
    f.write(struct.pack('h', 0x2F01)) # magic_number
    f.write(struct.pack('f', 0.0))    # sample_rate
    f.write(struct.pack('i', 0))      # range_mv
    f.write(struct.pack('f', 0.0))    # offset_mv
    f.write(struct.pack('B', dw))     # data_width
    f.write(struct.pack('i', 0))      # offset
    f.write(struct.pack('B', 2))      # sub_version
    f.write(struct.pack('B', 0x40))   # status_flag
    f.write(struct.pack('B', 0))      # pad1
    f.write(struct.pack('B', 0))      # pad2
    f.write(struct.pack('B', 0))      # pad3
    trace.tofile(f)

################################### RANGE READER
_dwfm_convert_dict = {
    np.dtype('int8') : char2uchar,
    np.dtype('int16') : short2ushort,
    np.dtype('float64') : double2double
    }

_info_dict = {
    np.dtype('int8') : np.iinfo(np.dtype('int8')),
    np.dtype('uint8') : np.iinfo(np.dtype('uint8')),
    np.dtype('int16') : np.iinfo(np.dtype('int16')),
    np.dtype('uint16') : np.iinfo(np.dtype('uint16')),
    np.dtype('int32') : np.iinfo(np.dtype('int32')),
    np.dtype('uint32') : np.iinfo(np.dtype('uint32')),
    np.dtype('float32') : np.finfo(np.dtype('float32')),
    np.dtype('float64') : np.finfo(np.dtype('float64'))
    }

_convert_dict = {
    np.dtype('uint8') : uchar2char,
    np.dtype('uint16') : ushort2short,
    np.dtype('float64') : double2double
    }

def read_range(filename, roi, offset=0, convert=False, fill='zero'):
  offset = roi.start + offset
  samples = roi.stop - roi.start

  # Read
  padl = min(max(0, -offset), samples)
  trace_read = read_trace(filename, offset, samples - padl)

  data_range = trace_read

  # Convert
  # Conversion may affect performance and don't change the result
  if convert:
    # Convert to signed values
    data_range = _convert_dict[trace_read.dtype](trace_read)

  # Pad
  # Padding eats up performance. Do it only when required
  if padl > 0:
    info = _info_dict[data_range.dtype]
    pad_value = 0 if fill=='zero' else info.max if fill == 'max' else info.min
    padl = np.full(padl, pad_value, info.dtype)
    data_range = np.concatenate((padl, data_range))

  padr = max(0, samples - len(data_range))
  if padr > 0:
    info = _info_dict[data_range.dtype]
    pad_value = 0 if fill=='zero' else info.max if fill == 'max' else info.min
    padr = np.full(padr, pad_value, info.dtype)
    if data_range.size > 0:
      data_range = np.concatenate((data_range, padr))
    else:
      data_range = padr

  return data_range

def convert2dwfm(trace):
  if trace.dtype in _convert_dict.keys():
    return trace

  return _dwfm_convert_dict[trace.dtype](trace)


################################### RANGE READER

class dwdb_reader(object):
  def __init__(self, dwdb, base_path='.'):
    self.base_path = base_path
    self.dwdb = dwdb
    self._fdwdb = open(dwdb)

  def read_next(self, start=0, stop=-1):
    line = self._fdwdb.next().strip()
    line_meta = parse_metadata_line(line)
    filename = line_meta['filename']
    off = line_meta.get('offset')
    off = -int(off) if off is not None else 0
    sample_len = stop - start
    start += off
    full_fn = os.path.join(self.base_path, filename).replace('\\', '/')
    # Read the trace
    trace = read_trace(full_fn, start, sample_len)
    # Convert to signed values
    trace = _convert_dict[trace.dtype](trace)
    return trace, line_meta

  def read_batch(self, tr_count, start=0, stop=-1):
    data, meta = [], []
    for i in range(tr_count):
        trace, line_meta = self.read_next(start, stop)
        data.append(trace)
        meta.append(line_meta)
    return data, meta

def convert2tmpl(trace, c=0):
    all_tmpls = re.findall(r"00+", trace)

    if len(all_tmpls) == 0:
      return trace

    tmpl = all_tmpls[0]
    l = len(tmpl)
    num2tmpl = '{' + '{0}:0{1}d'.format(c, l) + '}'
    return convert2tmpl(re.sub(tmpl, num2tmpl, trace, 1))


class dwdb_writer(object):
  def __init__(self, dwdb, trace='', base_path=None):
    self._base_path = base_path if base_path is not None else os.path.dirname(dwdb)

    trace = convert2tmpl(trace)

    dwdb_dir_name = os.path.dirname(dwdb)
    if dwdb_dir_name and not os.path.exists(dwdb_dir_name):
      os.makedirs(dwdb_dir_name)

    self._fdwdb = open(dwdb, 'w')
    self._dwfm_tmpl = trace if trace else 'traces/d{0:04d}/d{1:04d}.dwfm'
    self._counters = [0] * len(re.findall(r"{\d", self._dwfm_tmpl))

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()

  def close(self):
    self._fdwdb.close()

  def write_next(self, trace, meta=None):
    fn = self._dwfm_tmpl.format(*self._counters)
    trace_fn = os.path.join(self._base_path, fn)

    tr_dir_name = os.path.dirname(trace_fn)
    if not os.path.exists(tr_dir_name):
      os.makedirs(tr_dir_name)

    save_trace(trace_fn, trace)

    _ = meta.pop('filename') # throw away filename
    off = meta.pop('offset', None)
    dwdb_line = fn if off is None else '{:+12d} {}'.format(int(off), fn)

    if meta is not None:
        meta_line = ' '.join("{!s}={!s}".format(k,v) for (k,v) in meta.iteritems())
        dwdb_line += ' ' + meta_line

    dwdb_line += '\n'
    self._fdwdb.write(dwdb_line)
    self._counters[-1] += 1
    if self._counters[-1] == 10000:
      self._counters[-1] = 0
      self._counters[-2] += 1

  def write_batch(self, traces, metas=None):
    if metas is not None:
      for t, m in zip(traces, metas):
        self.write_next(t, m)
    else:
      for t in traces:
        self.write_next(t)
