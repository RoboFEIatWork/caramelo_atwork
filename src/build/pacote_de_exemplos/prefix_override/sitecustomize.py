import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/atwork/caramelo_atwork/src/install/pacote_de_exemplos'
