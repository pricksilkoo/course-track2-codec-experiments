from pathlib import Path
import sys
import pytest
import torch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from ssp_codec.decoder_interpolation import interpolate_decoder


@pytest.mark.parametrize("alpha",[0.,.1,.25,1.])
def test_parameter_only_and_source_immutable(alpha):
    base={"encoder.weight":torch.tensor([1.]),"quantizer.output_projections.0.weight":torch.tensor([2.]),
          "quantizer.codebook":torch.tensor([3.]),"decoder.window":torch.tensor([4.]),
          "decoder.weight":torch.tensor([5.]),"synthesis_temporal.weight":torch.tensor([6.]),
          "quantizer.count":torch.tensor(7)}
    donor={k:v+10 for k,v in base.items()}
    params={"encoder.weight","quantizer.output_projections.0.weight","decoder.weight","synthesis_temporal.weight"}
    before={k:v.clone() for k,v in base.items()}
    mixed,keys=interpolate_decoder(base,donor,params,alpha)
    assert keys==["decoder.weight","synthesis_temporal.weight"]
    for k in base:
        assert torch.equal(base[k],before[k])
        assert torch.equal(mixed[k],(1-alpha)*base[k]+alpha*donor[k] if k in keys else base[k])


def test_reject_incompatible_state():
    with pytest.raises(ValueError):interpolate_decoder({"decoder.weight":torch.zeros(1)},
        {"decoder.weight":torch.zeros(2)},{"decoder.weight"},.1)


@pytest.mark.parametrize("alpha",[-.1,1.1,float("nan")])
def test_reject_bad_coefficient(alpha):
    with pytest.raises(ValueError):interpolate_decoder({"decoder.weight":torch.zeros(1)},
        {"decoder.weight":torch.ones(1)},{"decoder.weight"},alpha)
