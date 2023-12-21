from hqm.tools.utility   import get_project_root
from hqm.tools.utility   import read_root
from hqm.tools.Cut       import Cut
from importlib.resources import files
from logzero             import logger

import os
import zfit
import numpy
import awkward      as ak
import utils_noroot as utnr

def get_data(q2, kind_dir):
    data_path  = get_project_root() + f"root_sample/v5/{kind_dir}/v10.21p2/2018_ETOS/{q2}_nomass.root"
    data_name  = data_path.replace('/', '_').replace('.', '_p_')
    json_path  = files('hqm_data').joinpath(f'pars/{data_name}.json')
    if not os.path.isfile(json_path):
        data_array = read_root(data_path, "ETOS")
        bdt_cmb    = Cut(lambda x: x.BDT_cmb > 0.831497)
        bdt_prc    = Cut(lambda x: x.BDT_prc > 0.480751)
        bdt        = bdt_cmb & bdt_prc
        data_array = bdt.apply(data_array)
        data_array = ak.to_numpy(data_array.B_M)

        utnr.dump_json(data_array.tolist(), json_path)
    else:
        logger.debug(f'Loading KDE data from: {json_path}')
        l_data     = utnr.load_json(json_path)
        data_array = numpy.array(l_data)

    return data_array


def get_KDE_shape(obs, kind, q2, name, bandwidth=10):
    if kind == "jpsi":
        kind_dir = "ctrl"
    else:
        kind_dir = kind

    data_array = get_data(q2, kind_dir)

    zdata = zfit.Data.from_numpy(obs, array=data_array)
    shape = zfit.pdf.KDE1DimFFT(obs=obs, data=zdata, name=name, bandwidth=bandwidth)

    return shape

