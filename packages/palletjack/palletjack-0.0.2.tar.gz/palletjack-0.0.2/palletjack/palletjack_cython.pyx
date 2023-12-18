# distutils: include_dirs = .

import pyarrow as pa
import pyarrow.parquet as pq
from cython.cimports.palletjack import cpalletjack
from pyarrow.lib cimport Buffer

def GenerateRapidMetadata(parquet_path, index_file_path):
    cpalletjack.GenerateRapidMetadata(parquet_path.encode('utf8'), index_file_path.encode('utf8'))

cpdef ReadRowGroupMetadata(index_file_path, row_group):
    v = cpalletjack.ReadRowGroupMetadata(index_file_path.encode('utf8'), row_group)
    cdef char[::1] mv = <char[:v.size()]>&v[0]
    cdef Buffer pyarrow_buffer = pa.py_buffer(mv)
    return pq.core._parquet._reconstruct_filemetadata(pyarrow_buffer)
