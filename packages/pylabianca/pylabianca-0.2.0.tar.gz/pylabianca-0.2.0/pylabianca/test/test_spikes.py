import os.path as op
import numpy as np
import pandas as pd
import pylabianca as pln
from pylabianca.utils import (download_test_data, get_data_path,
                              get_fieldtrip_data)


download_test_data()
data_dir = get_data_path()


def create_fake_spikes():
    times = [[-0.3, -0.1, 0.025, 0.11, 0.22, 0.25, 0.4,
              -0.08, 0.12, 0.14, 0.19, 0.23, 0.32],
             [-0.22, -0.13, -0.03, 0.08, 0.16, 0.33, -0.2,
              -0.08, 0.035, 0.148, 0.32]]
    trials = [[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]]
    spk = pln.SpikeEpochs(times, trials)
    return spk


def create_random_spikes(n_cells=4, **args):
    n_trials = 25
    tmin, tmax = -0.5, 1.5
    tlen = tmax - tmin
    n_spikes_per_tri = [10, 21]

    times = list()
    trials = list()
    for cell_idx in range(n_cells):
        this_tri = list()
        this_tim = list()
        for tri_idx in range(n_trials):
            n_spk = np.random.randint(*n_spikes_per_tri)
            tms = np.random.rand(n_spk) * tlen + tmin
            this_tri.append(np.ones(n_spk) * tri_idx)
            this_tim.append(tms)
        this_tri = np.concatenate(this_tri)
        this_tim = np.concatenate(this_tim)
        times.append(this_tim)
        trials.append(this_tri)
    return pln.SpikeEpochs(times, trials, **args)


def test_crop():
    spk = create_fake_spikes()
    spk.crop(tmin=0.1)

    assert (spk.time[0] == np.array(
        [0.11, 0.22, 0.25, 0.4, 0.12, 0.14, 0.19, 0.23, 0.32])).all()
    assert (spk.time[1] == np.array([0.16, 0.33, 0.148, 0.32])).all()
    assert (spk.trial[0] == np.array([0, 0, 0, 0, 1, 1, 1, 1, 1])).all()
    assert (spk.trial[1] == np.array([0, 0, 1, 1])).all()


def test_repr():
    spk = create_fake_spikes()
    should_be = '<SpikeEpochs, 2 epochs, 2 cells, 12.0 spikes/cell on average>'
    assert str(spk) == should_be


def test_pick_cells():
    spk = create_fake_spikes()
    assert len(spk.time) == 2
    spk.pick_cells('cell001')
    assert len(spk.time) == 1
    assert spk.time[0][0] == -0.22


def test_pick_cells_cellinfo_query():
    from copy import deepcopy
    cellinfo = pd.DataFrame({'cell_idx': [10, 15, 20, 25],
                             'letter': list('abcd')})
    spk = create_random_spikes(cellinfo=cellinfo)

    spk2 = deepcopy(spk)
    spk2.pick_cells(query='cell_idx > 18')
    assert len(spk2.time) == 2
    assert spk2.cellinfo.shape[0] == 2
    assert (spk2.cellinfo.letter.values == np.array(['c', 'd'])).all()

    spk3 = deepcopy(spk)
    spk3.pick_cells(query="letter in ['a', 'c']")
    assert len(spk3.time) == 2
    assert len(spk3.time[1]) == len(spk.time[2])
    assert (spk3.cellinfo.cell_idx.values == [10, 20]).all()


def test_to_raw():
    times = [[-0.3, -0.28, -0.26, 0.15, 0.18, 0.2],
             [-0.045, 0.023, -0.1, 0.13]]
    trials = [[0, 0, 0, 0, 0, 0], [0, 0, 1, 1]]
    spk = pln.SpikeEpochs(times, trials)

    spk_tm, spk_raw = pln.spikes._spikes_to_raw(spk, sfreq=10)
    print(spk_raw)
    good_tms = np.arange(-0.3, 0.21, step=0.1)
    good_raw = np.array(
        [[[3, 0, 0, 0, 1, 2], [0, 0, 0, 2, 0, 0]],
         [[0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0]]]
    )
    assert (spk_tm == good_tms).all()
    assert (spk_raw == good_raw).all()


def test_epoching_vs_fieldtrip():
    ft_data = get_fieldtrip_data()

    # read and epoch data
    events_test = np.array([[22928800, 0, 1],
                            [171087520, 0, 1],
                            [300742480, 0, 1]])

    spk = pln.io.read_plexon_nex(ft_data)
    spk_epo_test = (spk.copy().pick_cells(['sig002a_wf', 'sig003a_wf'])
                    .epoch(events_test, tmin=-2.75, tmax=3.,
                           keep_timestamps=True)
    )

    # read fieldtrip results
    fname = 'ft_spk_epoched.mat'
    spk_epo_test_ft = pln.io.read_fieldtrip(
        op.join(data_dir, fname), kind='epochs', data_name='spikeTrials_test')

    # check that the results are the same
    for ch_idx in range(2):
        assert (spk_epo_test_ft.timestamps[ch_idx]
                == spk_epo_test.timestamps[ch_idx]).all()

        assert (spk_epo_test_ft.trial[ch_idx]
                == spk_epo_test.trial[ch_idx]).all()

        np.testing.assert_almost_equal(
            spk_epo_test.time[ch_idx], spk_epo_test_ft.time[ch_idx])
