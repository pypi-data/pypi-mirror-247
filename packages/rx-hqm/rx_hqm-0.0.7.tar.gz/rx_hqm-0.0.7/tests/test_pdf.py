from hqm.model         import get_part_reco
from hqm.model         import get_Bu2Ksee_shape
from hqm.model         import get_Bd2Ksee_shape
from hqm.model         import get_signal_shape
from hqm.tools.utility import get_project_root
from logzero           import logger

import matplotlib.pyplot as plt
import zutils.utils      as zut
import numpy             as np
import os

def plot(shape, label, mass_window=(4500, 6000), d_const=None):
    plot_dir = 'output/tests/pdf'
    os.makedirs(plot_dir, exist_ok=True)

    plt.figure()
    x = np.linspace(mass_window[0], mass_window[1], 2000)
    y = shape.pdf(x)
    plt.plot(x, y, label=label)
    plt.legend()
    plt.xlim(mass_window)
    plt.ylim(bottom=0)
    logger.info(f"saving plot to {plot_dir}/{label}.pdf")
    plt.savefig(f'{plot_dir}/{label}.pdf')
    plt.close()

    zut.print_pdf(shape, txt_path=f'{plot_dir}/{label}.txt', d_const=d_const)

def test_part_reco():
    part_reco_shape = get_part_reco(preffix='prc', name='pr shape')
    plot(part_reco_shape, "part_reco")


def test_Bu2Ksee():
    Bu2Ksee_shape = get_Bu2Ksee_shape(year='2018', trigger='ETOS', name='Bu shape')
    plot(Bu2Ksee_shape, "Bu2Ksee")


def test_Bd2Ksee():
    Bd2Ksee_shape = get_Bd2Ksee_shape(year='2018', trigger='ETOS', name='Bd shape')
    plot(Bd2Ksee_shape, "Bd2Ksee")


def test_signal_shape_mm():
    signal_shape_mm, constraints = get_signal_shape(name='sig_mm', preffix='mm_18_tos', year="2018", trigger="MTOS")
    plot(signal_shape_mm, "signal_shape_mm", (5180, 5600), d_const=constraints)


def test_signal_shape_ee():
    signal_shape_ee, constraints = get_signal_shape(name='sig_ee', preffix='ee_18_tos', year="2018", trigger="ETOS")
    plot(signal_shape_ee, "signal_shape_ee", (4500, 6000), d_const=constraints)

def main():
    test_part_reco()
    test_Bu2Ksee()
    test_Bd2Ksee()
    test_signal_shape_ee()
    test_signal_shape_mm()


if __name__ == '__main__':
    main()

