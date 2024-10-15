import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/gustav/P5-Kuka-Dual-Arm/install/llm_pkg'
