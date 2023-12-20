from misID_tools.zmodel import misID_real_model_builder
from zutils.plot import plot as zfp

import zutils.utils as zut
import utils_noroot as utnr
import matplotlib.pyplot as plt
import zfit
import os

class data:
    ver = 'v1'              
    obs = zfit.Space('B_M', limits=(4500, 6500))
    out_dir = 'output/zmodel' 

    os.makedirs(out_dir, exist_ok=True) 

def test_real_model_IO():
    misID_builder = misID_real_model_builder('misID_1', version=data.ver, obs=data.obs)

    try:
        misID_builder.load_model()
        model = misID_builder.build_model()
    except:
        assert False

    zut.print_pdf(model, txt_path=f'{data.out_dir}/pdf_IO.txt') 
    
def test_real_model_function():
    misID_builder = misID_real_model_builder('misID_2', version=data.ver, obs=data.obs)

    misID_builder.load_model()
    # misID_builder.fix_mode = 'all' # Default option even if you don't sepcify.
    model = misID_builder.build_model()

    try:
        N = sum(misID_builder.params['yld'][1:])
        sampler = model.create_sampler(n=N,fixed_params=True)

        plotter = zfp(data=sampler, model=model)
        plotter.plot(nbins=50, plot_range=(4500, 6500))
        
        plt.savefig(f'{data.out_dir}/plot_misID.png', bbox_inches='tight')
        plt.close('all')
    except:
        assert False

    zut.print_pdf(model, txt_path=f'{data.out_dir}/pdf_function.txt') 

def test_real_model_fix_ratio():
    misID_builder = misID_real_model_builder('misID_3', version=data.ver, obs=data.obs)

    misID_builder.load_model()
    misID_builder.fix_mode = 'ratio' # Must be set before call "build_model()"
    model = misID_builder.build_model()

    try:
        N = 10000
        sampler = model.create_sampler(n=N,fixed_params=True)

        model.fit_to(sampler)

        plotter = zfp(data=sampler, model=model)
        plotter.plot(nbins=50, plot_range=(4500, 6500))
        
        plt.savefig(f'{data.out_dir}/plot_misID_ratio_mode.png', bbox_inches='tight')
        plt.close('all')
    except:
        assert False

    zut.print_pdf(model, txt_path=f'{data.out_dir}/pdf_fix_ratio.txt') 

if __name__ == '__main__':
    test_real_model_IO()
    test_real_model_function()
    test_real_model_fix_ratio()

