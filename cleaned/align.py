from pymol import cmd
from pathlib import Path


for dd in Path('.').glob('????'):
    if not dd.is_dir():
        continue

    full, for_leap = dd / "full.pdb", dd / "for_leap.pdb"


    if not full.exists() and for_leap.exists():
        continue

    print(dd)

    cmd.delete('all')
    cmd.load(full)
    cmd.load(for_leap)
    cmd.align('full', 'for_leap')
    cmd.save( full, 'full' )
    cmd.delete('all')
