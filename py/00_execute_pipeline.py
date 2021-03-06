import os
from os.path import join
import pandas as pd


# Set parameters
dataset_folder = '/home/jullygh/Downloads/test_nii/'
workspace_folder = '/home/jullygh/Downloads/workspace/'

root = join(os.getcwd(), '..')
bin_dir = join(root, 'bin')

# Cast variables
csv_df = join(root, 'data', 'data_df.csv')
dsf = os.path.normpath(dataset_folder)
wsf = os.path.normpath(workspace_folder)

# Add environment variable
os.system('export SUBJECTS_DIR=%s' % dsf)

# Load dataset: df
df = pd.read_csv(csv_df)

# Define the pipeline (list of commands): pipeline_cmd
sb_snippet = 'subject_id'
sb_dir = join(dataset_folder, sb_snippet)
pipeline_cmd = {}

hemispheres = ['lh', 'rh']
surface_file_ext = ['', '.vtk', '.obj', '.m', '.m', '.m']
files_orig = ['.white', '.sphere.reg']

files_target = []
for f in files_orig:
    for ext in surface_file_ext:
        files_target.append(f + ext)

for h in hemispheres:
    pipeline_cmd[h] = [
        'mris_convert ' + join(sb_dir, 'surf', h + files_target[0]) + ' ' + join(wsf, sb_snippet, h + files_target[1]),
        'java -jar ' + join(bin_dir, 'ShapeTranslator.jar') + ' -input ' + join(wsf, sb_snippet, h + files_target[1]) + ' -output ' + join(wsf, sb_snippet, h + files_target[2]) + ' -obj',
        join(bin_dir, 'ccbbm') + ' -obj2mesh ' + join(wsf, sb_snippet, h + files_target[2]) + ' ' + join(wsf, sb_snippet, h + files_target[3]),
        join(bin_dir, 'ccbbm') + ' -enforce_manifold_topology ' + join(wsf, sb_snippet, h + files_target[3]) + ' ' + join(wsf, sb_snippet, h + files_target[4]),
        join(bin_dir, 'ccbbm') + ' -close_boundaries ' + join(wsf, sb_snippet, h + files_target[3]) + ' ' + join(wsf, sb_snippet, h + files_target[4]),

        'mris_convert ' + join(sb_dir, 'surf', h + files_target[6]) + ' ' + join(wsf, sb_snippet, h + files_target[7]),
        'java -jar ' + join(bin_dir, 'ShapeTranslator.jar') + ' -input ' + join(wsf, sb_snippet, h + files_target[7]) + ' -output ' + join(wsf, sb_snippet, h + files_target[8]) + ' -obj',
        join(bin_dir, 'ccbbm') + ' -obj2mesh ' + join(wsf, sb_snippet, h + files_target[8]) + ' ' + join(wsf, sb_snippet, h + files_target[9]),
        join(bin_dir, 'ccbbm') + ' -enforce_manifold_topology ' + join(wsf, sb_snippet, h + files_target[9]) + ' ' + join(wsf, sb_snippet, h + files_target[10]),
        join(bin_dir, 'ccbbm') + ' -close_boundaries ' + join(wsf, sb_snippet, h + files_target[10]) + ' ' + join(wsf, sb_snippet, h + files_target[11]),

        join(bin_dir, 'ccbbm') + ' -transform ' + join(wsf, sb_snippet, h + files_target[11]) + ' ' + join(bin_dir, 'one_hundredth.txt') + ' ' + join(wsf, sb_snippet, h + files_target[11]),

        'mris_convert -c ' + join(sb_dir, 'surf', h + '.thickness') + ' '+ join(sb_dir, 'surf', h + '.white') + ' ' + join(wsf, sb_snippet, h + '_thick.asc'),
        join(bin_dir, 'FSthick2raw') + ' ' + join(wsf, sb_snippet, h + '_thick.asc') + ' ' + join(wsf, sb_snippet, h + '_thick.raw'),

        # 14 - 15
        join(bin_dir, 'ccbbm') + ' -gausssmooth_attribute3 256 ' + join(wsf, sb_snippet, h + '.sphere.reg.m') + ' ' + join(wsf, sb_snippet, h + '_thick.raw') + ' 2e-4 ' + join(wsf, sb_snippet, h + '_thick_2e-4.raw'),
        join(bin_dir, 'ccbbm') + ' fastsampling ' + join(wsf, sb_snippet, h + '.sphere.reg.m') + \
            '[' + join(bin_dir, 'FreeSurfer_IC7_RH_sym.m') + ', ' + join(bin_dir, 'FreeSurfer_IC7.m') + '] ' + join(wsf, sb_snippet, h + '.white.sampled.m') + ' -tmp_atts ' + \
            join(wsf, sb_snippet, h + '_thick_2e-4.raw') + ' -tar_atts ' + join(wsf, sb_snippet, h + ']_thick_2e-4_sampled.raw')

    ]

for key, val in pipeline_cmd.items():
    for cmd in val:
        command = str(cmd).replace('subject_id', '001')
        print(command)
        os.system(command)
