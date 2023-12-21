#Sandpit to test out neutralNEMO functions

import grid
import surf
import os


tests_dir = os.path.abspath("../../tests/")
mm_path = tests_dir + "/mesh_mask.nc"
orc_path = tests_dir + "/ORCA_R2_zps_domcfg.nc"
t_path = tests_dir + "/GYRE_1m_04110101_04201230_grid_T.nc"

hgd = grid.load_hgriddata( mm_path, chunks="auto" )

neutral_grid = grid.build_nemo_hgrid( hgd, iperio=False, jperio = False)

zgd = grid.load_zgriddata( mm_path, chunks="auto")

tsd = surf.load_tsdata( t_path, zgd, to_varname="votemper", so_varname="vosaline")

surf_dataset = surf.find_omega_surfs( tsd, neutral_grid , zgd, [150., 300.], [10,10], [9,9], [-1,-1], eos="gsw",
                                      ITER_MAX=10, calc_veronis=True)

print(surf_dataset)

# print(surf_dataset["omsurf_s"])



