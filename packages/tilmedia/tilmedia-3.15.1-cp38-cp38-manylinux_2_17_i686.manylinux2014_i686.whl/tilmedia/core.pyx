from libcpp cimport bool
from libcpp.string cimport string
from .logger import LoggerWrapper

_logger_wrapper_backup = None
'Backup of the most recent instance, because tilmedia uses those functions to output messages from tilmedia functions.'

cdef extern from "Message_C.h":
    ctypedef void * TModelicaFormatMessage
    ctypedef void * TDymosimErrorLevWrapper

    ctypedef struct CallbackFunctions:
        TModelicaFormatMessage ModelicaFormatMessage
        TModelicaFormatMessage ModelicaFormatError
        TDymosimErrorLevWrapper DymosimErrorLevWrapper
        const double *time
        char *cacheInstanceName
        int isTopLevelInstance

        int lock_gas
        int lock_liq
        int lock_vle
        int lock_realmixture
        int lock_modelmap
        int lock_ntu
        int lock_modelmap_ntu
        int lock_lic_new
        int lock_AddOnLicenseCheck
        int lock_refprop
        int lock_multiflash

    cdef CallbackFunctions* CallbackFunctions_construct() nogil


include "c_externalobject.pxi"

include "c_logger.pxi"

include "c_batchcaller.pxi"

include "c_general.pxi"

include "c_liquid.pxi"

include "c_gas.pxi"

include "c_vlefluid.pxi"




