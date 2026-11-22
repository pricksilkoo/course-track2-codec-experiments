from pathlib import Path
import torch
from ssp_codec.config import load_config
from ssp_codec.model import CourseCodec
from ssp_codec.io import read_bitstream,write_bitstream

ROOT=Path(__file__).resolve().parents[1]

def config():return load_config(ROOT/'configs/c6_30ms/b_s3407.yaml')

def test_only_approved_configuration_differences():
    old=load_config(ROOT/'configs/champion6/b_s3407_fourier_gru.yaml');new=config()
    old['model']['encoder_lookahead_frames']=2
    old['training'].update(output_dir='runs/c6_30ms_b_s3407',checkpoint_keep_last=20,recovery_checkpoint_interval_steps=1000)
    assert old==new
    assert new['seed']==new['training']['data_order_seed']==3407

def test_real_bytes_and_forced_future_boundary(tmp_path):
    torch.manual_seed(3407);model=CourseCodec(**config()['model'])
    with torch.no_grad():model(torch.randn(1,1,6400))
    model.eval();x=torch.randn(1,1,1607)
    with torch.no_grad():
        y,idx,_=model(x);assert idx.shape==(1,11,3) and y.shape==x.shape
        assert torch.isfinite(y).all() and torch.equal(idx,model.encode(x))
        p=tmp_path/'bits.bin';write_bitstream(p,idx[0],1607);v,meta=read_bitstream(p)
        assert p.stat().st_size==33 and meta['bits_per_frame']==24
        torch.testing.assert_close(y,model.decode(v[None],length=1607),atol=1e-6,rtol=1e-5)
        look=model.analysis_temporal.lookahead
        assert look.frames==2 and look.depthwise.kernel_size==(3,)
        look.depthwise.weight.zero_();look.depthwise.weight[...,-1]=1
        look.project.weight.zero_();look.project.bias.zero_()
        for c in range(160):look.project.weight[c,c,0]=1
        def analysis(z):
            return model.analysis_gru(model.analysis_temporal(model.latent_norm(model.encoder(z))))
        past_boundary=x.clone();past_boundary[...,480:]+=10
        within=x.clone();within[...,320:480]+=10
        z=analysis(x)
        torch.testing.assert_close(z[:,:1],analysis(past_boundary)[:,:1],atol=1e-6,rtol=1e-5)
        torch.testing.assert_close(z[:,:1],analysis(x[...,:480])[:,:1],atol=1e-6,rtol=1e-5)
        assert not torch.allclose(z[:,:1],analysis(within)[:,:1])
        torch.testing.assert_close(model(x)[0][...,:160],model(past_boundary)[0][...,:160],atol=1e-6,rtol=1e-5)
        changed=idx.clone();changed[:,1:]=(changed[:,1:]+1)%256
        torch.testing.assert_close(model.decode(idx)[...,:160],model.decode(changed)[...,:160],atol=1e-6,rtol=1e-5)

def test_finite_cpu_gradient():
    model=CourseCodec(**config()['model']).train();x=torch.randn(1,1,1600,requires_grad=True)
    y,_,commit=model(x);(y.square().mean()+commit).backward()
    assert torch.isfinite(x.grad).all() and x.grad.abs().sum()>0
    assert all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters())

def test_busy_project_reservation_does_not_query_or_replace_gpu(tmp_path,monkeypatch):
    import sys,fcntl
    sys.path.insert(0,str(ROOT/'scripts'))
    import supervise_c6_30ms as sup
    locks=[]
    for gpu in range(4):
        p=tmp_path/f'.champion4_gpu{gpu}.lock';p.touch();f=p.open('r')
        fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);locks.append(f)
    def forbidden(_):raise AssertionError('reserved GPU must not be queried')
    monkeypatch.setattr(sup,'gpu_state',forbidden)
    assert sup.choose_gpu(tmp_path) is None
    for f in locks:f.close()
