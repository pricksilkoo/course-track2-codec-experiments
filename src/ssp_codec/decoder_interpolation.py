"""Parameter-only decoder interpolation; encoder, RVQ and every buffer stay fixed."""
import math
import torch

DECODER_PREFIXES=("decoder.","decoder_refinement.","synthesis_temporal.",
                  "synthesis_transformer.","synthesis_conv2former.")


def interpolate_decoder(base, donor, parameter_names, alpha):
    if not math.isfinite(alpha) or not 0 <= alpha <= 1:
        raise ValueError("alpha must be finite and in[0,1]")
    if base.keys()!=donor.keys():raise ValueError("state keys differ")
    eligible={k for k in parameter_names if k.startswith(DECODER_PREFIXES)}
    if not eligible or not eligible<=base.keys():raise ValueError("invalid decoder parameter set")
    result={}
    with torch.no_grad():
        for k,b in base.items():
            d=donor[k]
            if b.shape!=d.shape or b.dtype!=d.dtype:raise ValueError(f"incompatible tensor:{k}")
            if k in eligible:
                if not b.is_floating_point():raise ValueError(f"nonfloating parameter:{k}")
                result[k]=((1.0-alpha)*b+alpha*d).clone()
            else:
                result[k]=b.clone()
    return result,sorted(eligible)
