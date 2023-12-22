import sys
import os
import numpy as np

# add a reference to load the module
ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT, '..'))

# load the package
from cloudwatcher import Wavecar, BlenderRender

def main():   
    filename = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'WAVECAR_aligned')
    contcar = os.path.join(ROOT, '..', 'samples', 'carbonmonoxide_gasphase', 'CONTCAR_aligned')
    wf = Wavecar(filename, lgamma=True)
    
    # create output folder if it does not exist
    outpath = os.path.join(ROOT, 'output')
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    
    # build BlenderRender object
    br = BlenderRender()
    br.render_kohn_sham_state(wf=wf, outpath=outpath, mo_indices=np.arange(0,wf.get_nbands()),
                              camera='x', contcar=contcar, camera_scale=8, ispin=1,
                              prefix='CO', isovalue=0.03)
    
if __name__ == '__main__':
    main()
