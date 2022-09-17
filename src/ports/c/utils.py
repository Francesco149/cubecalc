def enum_bits(e, x, suff=""):
  return " | ".join([b.name + suff for b in e if x & b])
