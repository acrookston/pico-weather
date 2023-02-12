# From: https://forums.raspberrypi.com/viewtopic.php?t=335431

def RemoveNonAscii(s):
  def RemoveNonAsciiByteArray(s):
    ba = bytearray()
    for b in s:
      if b < 0x7F:
        ba.append(b)
    return ba
  def RemoveNonAsciiBytes(s):
    o = b""
    for b in s:
      if b < 0x7F:
        o += bytes(chr(b), "ascii")
    return o
  def RemoveNonAsciiChar(s):
    o = ""
    for c in s:
      if ord(c) < 0x7F:
        o += c
    return o
  if isinstance(s, bytearray) : return RemoveNonAsciiByteArray(s)
  if isinstance(s, bytes)     : return RemoveNonAsciiBytes(s)
  else                        : return RemoveNonAsciiChar(s)

def Show(s):
  def ShowByteArray(s):
    o = "bytearray(b'"
    for b in s:
      if b >= 0x20 and b < 0x7F : o += chr(b)
      else                      : o += "\\x" + "{:02x}".format(b)
    return o + "')"
  def ShowBytes(s):
    o = "b'"
    for b in s:
      if b >= 0x20 and b < 0x7F : o += chr(b)
      else                      : o += "\\x" + "{:02x}".format(b)
    return o + "'"
  def ShowChar(s):
    o = "'"
    for c in s:
      b = ord(c)
      if b >= 0x20 and b < 0x7F : o += c
      else                      : o += "\\x" + "{:02x}".format(b)
    return o + "'"
  if isinstance(s, bytearray) : return ShowByteArray(s)
  if isinstance(s, bytes)     : return ShowBytes(s)
  else                        : return ShowChar(s)

def Test(func, s):
  o = func(s)
  print("{:<16} {:<24} -> len {} text = {}".format(func.__name__,
                                                   Show(s),
                                                   len(o),
                                                   Show(o)))

# Test( RemoveNonAscii, bytearray(b'\x80abc'))
# Test( RemoveNonAscii,           b'\x80abc')
# Test( RemoveNonAscii,            '\x80abc')
