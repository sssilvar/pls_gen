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
        'ccbbm -obj2mesh ' + join(wsf, sb_snippet, h + files_target[2]) + ' ' + join(wsf, sb_snippet, h + files_target[3]),
        'ccbbm -enforce_manifold_topology ' + join(wsf, sb_snippet, h + files_target[3]) + ' ' + join(wsf, sb_snippet, h + files_target[4]),
        'ccbbm -close_boundaries ' + join(wsf, sb_snippet, h + files_target[3]) + ' ' + join(wsf, sb_snippet, h + files_target[4]),

        'mris_convert ' + join(sb_dir, 'surf', h + files_target[5]) + ' ' + join(wsf, sb_snippet, h + files_target[6]),
        'java -jar ' + join(bin_dir, 'ShapeTranslator.jar') + ' -input ' + join(wsf, sb_snippet, h + files_target[6]) + ' -output ' + join(wsf, sb_snippet, h + files_target[7]) + ' -obj',
        'ccbbm -obj2mesh ' + join(wsf, sb_snippet, h + files_target[7]) + ' ' + join(wsf, sb_snippet, h + files_target[8]),
        'ccbbm -enforce_manifold_topology ' + join(wsf, sb_snippet, h + files_target[8]) + ' ' + join(wsf, sb_snippet, h + files_target[9]),
        'ccbbm -close_boundaries ' + join(wsf, sb_snippet, h + files_target[10]) + ' ' + join(wsf, sb_snippet, h + files_target[11])
    ]

for key, val in pipeline_cmd.items():
    for cmd in val:
        command = str(cmd).replace('subject_id', '001')
        print(command)
        os.system(command)
