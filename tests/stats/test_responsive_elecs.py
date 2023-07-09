import pytest
import numpy as np

from naplib.stats import responsive_ttest
from naplib import Data

@pytest.fixture(scope='module')
def outstruct():
    rng = np.random.default_rng(1)
    x = rng.random(size=(800,4))
    x2 = rng.random(size=(700,4))
    x3 = rng.random(size=(400,4))
    x[100:,1] = 10+rng.random(700,)
    x2[100:,1] = 5+rng.random(600,)
    x3[100:,1] = 7+rng.random(300,)
    data_tmp = []
    for xx in [x,x2,x3]:
        data_tmp.append({'resp': xx, 'dataf': 100, 'befaft': np.array([1.,1.])})
    return Data(data_tmp)

def test_responsive_ttest_picks_correct_electrode_from_outstruct(outstruct):
    new_out, stats = responsive_ttest(data=outstruct, resp='resp', sfreq='dataf', befaft='befaft', random_state=2)
    assert new_out[0]['resp'].shape[1] == 1
    assert np.array_equal(stats['significant'], np.array([0,1,0,0]).astype('bool'))
    assert np.allclose(stats['stat'], np.array([-1.67113052, -63.20943622,   0.23296204,  -1.78460185]), atol=1e-7)
    assert np.allclose(stats['pval'], np.array([1.26958793e-001, 2.51319873e-266, 8.15870594e-001, 1.26958793e-001]), atol=1e-7)

def test_responsive_ttest_picks_correct_electrode_from_outstruct_alternative_less(outstruct):
    new_out, stats = responsive_ttest(data=outstruct, resp='resp', sfreq='dataf', befaft='befaft', random_state=2, alternative='less')
    assert new_out[0]['resp'].shape[1] == 1
    assert np.array_equal(stats['significant'], np.array([0,1,0,0]).astype('bool'))
    assert np.allclose(stats['stat'], np.array([-1.67113052, -63.20943622,   0.23296204,  -1.78460185]), atol=1e-7)
    assert np.allclose(stats['pval'], np.array([6.34793965e-002, 1.25659937e-266, 5.92064703e-001, 6.34793965e-002]), atol=1e-7)

def test_responsive_ttest_picks_correct_electrode_from_outstruct_alternative_greater(outstruct):
    new_out, stats = responsive_ttest(data=outstruct, resp='resp', sfreq='dataf', befaft='befaft', random_state=2, alternative='greater')
    assert new_out[0]['resp'].shape[1] == 0
    assert np.array_equal(stats['significant'], np.array([0,0,0,0]).astype('bool'))
    assert np.allclose(stats['stat'], np.array([-1.67113052, -63.20943622,   0.23296204,  -1.78460185]), atol=1e-7)
    assert np.allclose(stats['pval'], np.array([1., 1., 1., 1.]), atol=1e-7)

def test_responsive_ttest_picks_correct_electrode_pass_args_individually_vs_outstruct_same(outstruct):
    new_resp, stats_resp = responsive_ttest(resp=outstruct['resp'], sfreq=100, befaft=np.array([1.,1.]), random_state=2)
    new_out, stats_out = responsive_ttest(data=outstruct, resp='resp', sfreq='dataf', befaft='befaft', random_state=2)

    assert np.array_equal(new_resp[0], new_out[0]['resp'])
    assert np.array_equal(new_resp[1], new_out[1]['resp'])
    assert np.array_equal(new_resp[2], new_out[2]['resp'])

    assert np.array_equal(stats_resp['stat'], stats_out['stat'])
    assert np.array_equal(stats_resp['pval'], stats_out['pval'])
    assert np.array_equal(stats_resp['significant'], stats_out['significant'])
