import zfit
import hist
import os
import zutils.utils as zut
import utils_noroot as utnr

from importlib.resources import files
from zutils.pdf          import SUJohnson
from hqm.tools.utility   import load_pickle
from hqm.tools.utility   import get_project_root
from hqm.tools.utility   import read_root
from hqm.tools.Cut       import Cut
from logzero             import logger


def get_correction_DSCB(obs, suffix):
    mu = zfit.Parameter(f"correction_DSCB_mu_{suffix}", 0, -100, 100)
    sigma = zfit.Parameter(f"correction_DSCB_sigma_{suffix}", 40, 0.1, 100)
    al = zfit.Parameter(f"correction_DSCB_al_{suffix}", 1.5, 0.001, 10)
    nl = zfit.Parameter(f"correction_DSCB_nl_{suffix}", 1, 0.001, 110)
    ar = zfit.Parameter(f"correction_DSCB_ar_{suffix}", 1.5, 0.001, 10)
    nr = zfit.Parameter(f"correction_DSCB_nr_{suffix}", 1, 0.001, 110)

    correction_DSCB = zfit.pdf.DoubleCB(
        obs=obs, mu=mu, sigma=sigma, alphal=al, nl=nl, alphar=ar, nr=nr, name="correction_DSCB"
    )
    return correction_DSCB


def get_correction_left_CB(obs, suffix):
    mu = zfit.Parameter(f"correction_left_CB_mu_{suffix}", -100, -500, 0)
    sigma = zfit.Parameter(f"correction_left_CB_sigma_{suffix}", 5, 0.001, 100)
    alpha = zfit.Parameter(f"correction_left_CB_alpha_{suffix}", 0.5, 0.001, 2)
    n = zfit.Parameter(f"correction_left_CB_n_{suffix}", 50, 1, 110)

    correction_left_CB = zfit.pdf.CrystalBall(obs=obs, mu=mu, sigma=sigma, alpha=alpha, n=n, name="correction_left_CB")
    return correction_left_CB


def get_correction_right_CB(obs, suffix):
    mu = zfit.Parameter(f"correction_right_CB_mu_{suffix}", 100, 0, 500)
    sigma = zfit.Parameter(f"correction_right_CB_sigma_{suffix}", 5, 0.001, 100)
    alpha = zfit.Parameter(f"correction_right_CB_alpha_{suffix}", -0.5, -2, -0.001)
    n = zfit.Parameter(f"correction_right_CB_n_{suffix}", 50, 1, 110)

    correction_right_CB = zfit.pdf.CrystalBall(
        obs=obs, mu=mu, sigma=sigma, alpha=alpha, n=n, name="correction_right_CB"
    )
    return correction_right_CB

def set_values(s_par, d_par, preffix):
    for par in s_par:
        name = par.name.replace(f'_{preffix}', '')
        try:
            val, err = d_par[name]
        except:
            logger.error(f'Cannot access {name}, found:')
            for key in d_par:
                logger.info(key)
            raise

        par.set_value(val)

def load_pdf(pickle_path, pdf, preffix):
    name      = pickle_path.replace('/', '_').replace('.', '_p_')
    json_path = files('hqm_data').joinpath(f'pars/{name}.json')
    if not os.path.isfile(json_path):
        obj    = load_pickle(pickle_path)
        res    = obj["result"]
        d_par  = zut.res_to_dict(res, frozen=True)
        utnr.dump_json(d_par, json_path)
    else:
        logger.debug(f'Loading parameters from: {json_path}')
        d_par  = utnr.load_json(json_path)

    s_par = pdf.get_params()
    set_values(s_par, d_par, preffix)

    return pdf


def get_data(kind, trigger, year, q2):
    project_root = get_project_root()
    BDT_cmb = Cut(lambda x: x.BDT_cmb > 0.831497)
    BDT_prc = Cut(lambda x: x.BDT_prc > 0.480751)
    BDT = BDT_cmb & BDT_prc
    path = project_root + f"root_sample/v5/{kind}/v10.21p2/{year}_{trigger}/{q2}_nomass.root"
    data_array = read_root(path, trigger)
    data_array = BDT.apply(data_array)
    return data_array


def get_hist_and_ratio(data_array, cmb_shape, plot_cmb):
    cmb_normalisation_region = (5500, 6000)
    mass_window = (4000, 6000)
    split_point = 5180

    cmb_normalisation_region_cut = Cut(
        lambda x: (x.B_M > cmb_normalisation_region[0]) & (x.B_M < cmb_normalisation_region[1])
    )
    mass_window_cut = Cut(lambda x: (x.B_M > mass_window[0]) & (x.B_M < mass_window[1]))
    split_point_cut = Cut(lambda x: x.B_M < split_point)
    part_reco_cut = mass_window_cut & split_point_cut
    sig_cut = mass_window_cut & ~split_point_cut

    cmb_total_yield = (
        cmb_normalisation_region_cut.get_entries(data_array)
        / cmb_shape.integrate(cmb_normalisation_region, norm=mass_window)[0]
    )
    part_reco_yield = (
        part_reco_cut.get_entries(data_array)
        - cmb_total_yield * cmb_shape.integrate((mass_window[0], split_point), norm=mass_window)[0]
    )
    sig_yield = (
        sig_cut.get_entries(data_array)
        - cmb_total_yield * cmb_shape.integrate((split_point, mass_window[1]), norm=mass_window)[0]
    )

    ratio = part_reco_yield / sig_yield

    # logger.info(f"cmb_total_yield: {cmb_total_yield}")
    # logger.info(f"part_reco_yield: {part_reco_yield}")
    # logger.info(f"sig_yield: {sig_yield}")
    # if plot_cmb is not None:
    #     plot_cmb_and_data(plot_cmb, data_array, cmb_shape, cmb_total_yield, mass_window)

    part_reco_region_data = part_reco_cut.apply(data_array)
    part_reco_region_hist = hist.Hist.new.Regular(
        100, mass_window[0], split_point, overflow=False, name="B_M"
    ).Double()
    part_reco_region_hist.fill(part_reco_region_data.B_M)

    binning = zfit.binned.RegularBinning(100, mass_window[0], split_point, name="B_M")
    binned_obs = zfit.Space("B_M", binning=binning)
    binned_pdf = cmb_shape.to_binned(binned_obs)
    cmb_hist = binned_pdf.to_hist()

    cmb_hist = (
        cmb_hist
        / cmb_hist.sum().value
        * zfit.run(cmb_total_yield * cmb_shape.integrate((mass_window[0], split_point), norm=mass_window)[0])
    )
    logger.info(f"cmb_hist.sum(): {cmb_hist.sum().value}")

    part_reco_hist = part_reco_region_hist - cmb_hist

    return part_reco_hist, ratio


def convolution_shape(cmb_shape, data_array, correction_function, name, plot_cmb):
    part_reco_hist, ratio = get_hist_and_ratio(data_array, cmb_shape, plot_cmb)
    part_reco_pdf = zfit.pdf.HistogramPDF(part_reco_hist)
    part_reco_unbinned = zfit.pdf.UnbinnedFromBinnedPDF(part_reco_pdf, zfit.Space("B_M", limits=(3000, 7000)))
    convolution_shape = zfit.pdf.FFTConvPDFV1(
        func=part_reco_unbinned,
        kernel=correction_function,
        name=f"convolution_shape_{name}",
        n=1000,
    )

    return convolution_shape, ratio, part_reco_hist


class CacheCmbShape:
    _all_cmb_shapes = {}

    @classmethod
    def __call__(cls, q2, pdf=None):
        if pdf is None:
            if q2 in cls._all_cmb_shapes:
                return cls._all_cmb_shapes[q2]
            else:
                return None
        else:
            cls._all_cmb_shapes[q2] = pdf


def get_cmb_mm_shape(q2, obs, preffix=''):
    cached_shape = CacheCmbShape()
    comb_mm = cached_shape(q2)
    if comb_mm is None:
        mu_cmb = zfit.Parameter(f"cmb_mm_mu_{q2}_{preffix}", 4000, 3500, 5000)
        scale_cmb = zfit.Parameter(f"cmb_mm_scale_{q2}_{preffix}", 10, 0.1, 100)
        a = zfit.Parameter(f"cmb_mm_a_{q2}_{preffix}", -10, -20, 0)
        b = zfit.Parameter(f"cmb_mm_b_{q2}_{preffix}", 1, 0, 10)
        comb_mm = SUJohnson(obs=obs, mu=mu_cmb, lm=scale_cmb, gamma=a, delta=b, name=f"comb_mm_{q2}_{preffix}")
        pickle_path = (
            get_project_root() + f"data/comb_mm/latest/{q2}_2018_B_M_NoBDTprc/{q2}_2018_B_M_NoBDTprc_fit_result.pickle"
        )
        comb_mm = load_pdf(pickle_path, comb_mm, preffix)
        cached_shape(q2, comb_mm)
    return comb_mm


def get_shape(kind, preffix='', plot_cmb=None):
    project_root = get_project_root()
    pickle_path = project_root + f"data/part_reco/fit_convolution/latest/{kind}/fit_result.pickle"
    obs = zfit.Space("B_M", limits=(4000, 6000))

    if   kind == "psi2S_high":
        mm_data = get_data(kind="data", trigger="MTOS", year="2018", q2="psi2")
        obs_kernel = zfit.Space("B_M", limits=(-800, 1200))
        correction_function = get_correction_right_CB(obs_kernel, suffix=f'{kind}_{preffix}')
        correction_function = load_pdf(pickle_path, correction_function, preffix)
        cmb_shape = get_cmb_mm_shape(q2="psi2", obs=obs, preffix=preffix)
        return convolution_shape(
            cmb_shape=cmb_shape,
            data_array=mm_data,
            correction_function=correction_function,
            name=kind,
            plot_cmb=plot_cmb,
        )
    elif kind == "psi2S_psi2S":
        mm_data = get_data(kind="data", trigger="MTOS", year="2018", q2="psi2")
        obs_kernel = zfit.Space("B_M", limits=(-1000, 1000))
        correction_function = get_correction_DSCB(obs_kernel, suffix=f'{kind}_{preffix}')
        correction_function = load_pdf(pickle_path, correction_function, preffix)
        cmb_shape = get_cmb_mm_shape(q2="psi2", obs=obs, preffix=preffix)
        return convolution_shape(
            cmb_shape=cmb_shape,
            data_array=mm_data,
            correction_function=correction_function,
            name=kind,
            plot_cmb=plot_cmb,
        )
    elif kind == "psi2S_Jpsi":
        mm_data = get_data(kind="data", trigger="MTOS", year="2018", q2="psi2")
        obs_kernel = zfit.Space("B_M", limits=(-1200, 800))
        correction_function = get_correction_DSCB(obs_kernel, suffix=f'{kind}_{preffix}')
        correction_function = load_pdf(pickle_path, correction_function, preffix)
        cmb_shape = get_cmb_mm_shape(q2="psi2", obs=obs, preffix=preffix)
        return convolution_shape(
            cmb_shape=cmb_shape,
            data_array=mm_data,
            correction_function=correction_function,
            name=kind,
            plot_cmb=plot_cmb,
        )
    elif kind == "Jpsi_psi2S":
        mm_data = get_data(kind="data", trigger="MTOS", year="2018", q2="jpsi")
        obs_kernel = zfit.Space("B_M", limits=(-800, 1200))
        correction_function = get_correction_DSCB(obs_kernel, suffix=f'{kind}_{preffix}')
        correction_function = load_pdf(pickle_path, correction_function, preffix)
        cmb_shape = get_cmb_mm_shape(q2="jpsi", obs=obs, preffix=preffix)
        return convolution_shape(
            cmb_shape=cmb_shape,
            data_array=mm_data,
            correction_function=correction_function,
            name=kind,
            plot_cmb=plot_cmb,
        )
    elif kind == "Jpsi_Jpsi":
        mm_data = get_data(kind="data", trigger="MTOS", year="2018", q2="jpsi")
        obs_kernel = zfit.Space("B_M", limits=(-1000, 1000))
        correction_function = get_correction_DSCB(obs_kernel, suffix=f'{kind}_{preffix}')
        correction_function = load_pdf(pickle_path, correction_function, preffix)
        cmb_shape = get_cmb_mm_shape(q2="jpsi", obs=obs, preffix=preffix)
        return convolution_shape(
            cmb_shape=cmb_shape,
            data_array=mm_data,
            correction_function=correction_function,
            name=kind,
            plot_cmb=plot_cmb,
        )
    else:
        raise


