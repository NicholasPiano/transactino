
from sys import argv
from shutil import copy2, copytree, rmtree, make_archive
from os.path import join, exists, abspath
from os import walk, mkdir

if len(argv) != 2:
  raise SystemExit('Must specify a version')

# 1. Take in arg to use as version
version = argv[1]

# 2. Copy Jormungand directory to correct location in Wotan
JORMUNGAND_ROOT = '../../jormungand/'
WOTAN_ASSETS = '../../wotan/woot/assets/'

jormungand_directory = 'jormungand_{}'.format(version)
wotan_directory = join(WOTAN_ASSETS, jormungand_directory)
wotan_target = join(WOTAN_ASSETS, '{}.zip'.format(jormungand_directory))

if exists(wotan_directory) or exists(wotan_target):
  raise SystemExit('Destination version exists: {}'.format(version))

mkdir(wotan_directory)

copytree(join(JORMUNGAND_ROOT, 'commands'), join(wotan_directory, 'commands'))
copytree(join(JORMUNGAND_ROOT, 'requirements'), join(wotan_directory, 'requirements'))
copytree(join(JORMUNGAND_ROOT, 'util'), join(wotan_directory, 'util'))
copy2(join(JORMUNGAND_ROOT, 'constants.py'), wotan_directory)
copy2(join(JORMUNGAND_ROOT, 'jormungand.py'), wotan_directory)
copy2(join(JORMUNGAND_ROOT, 'settings.py'), wotan_directory)
copy2(join(JORMUNGAND_ROOT, 'JORMUNGAND.md'), wotan_directory)

# 3. Delete unnecessary files
unwanted_directories = [
  '__pycache__',
]

for root, dirs, files in walk(wotan_directory):
  for name in dirs:
    if name == '__pycache__':
      pycache = join(root, '__pycache__')
      rmtree(pycache)

# 4. Create zip file
wotan_abspath = abspath(wotan_directory)
make_archive(
  wotan_abspath,
  'zip',
  root_dir=abspath(WOTAN_ASSETS),
  base_dir=jormungand_directory,
)

# 5. Remove copied directory
rmtree(wotan_abspath)
