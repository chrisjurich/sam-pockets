import os
import shutil
from pathlib import Path
from pymol import cmd, stored
#import enzy_htp as eh

def get_charge( fname ):
    cmd.delete('all')
    cmd.load( fname )
    stored.fc = 0
    cmd.iterate('all', 'stored.fc += formal_charge')
    print(stored.fc)


def validate_file( lig ):
    cmd.delete('all')    
    code = lig.stem.split('_')[0]
    cmd.fetch( code )
    cmd.load( lig )
    cmd.remove('hydrogens')

    assert cmd.count_atoms(code) == cmd.count_atoms(lig.stem)

    cmd.delete('all')

def protonate( lig ):
    shutil.copy(lig, 'temp.mol2')
    os.system('/sb/apps/moe/bin/moebatch -script cmd.svl 1>/dev/null 2>/dev/null')
    shutil.copy('temp.mol2', lig)
   

def parameterize( lig, outdir ):
    
    prepin = f"{outdir}/{code}.prepin"
    frcmod = f"{outdir}/{code}.frcmod"

    os.system(f'antechamber -i {lig} -fi mol2 -o {prepin} -fo prepi -c bcc -s 0 -nc {get_charge(lig)} ')
    os.system(f"parmchk2 -i {prepin} -f prepi -o {frcmod} ")


unique = dict()

for lidx, lig in enumerate(Path('../cleaned/').rglob('???_?.mol2')):
    # for each ligand
    # 1. check that it is correct
    print(lidx, lig)
    validate_file( lig )
    
    protonate( lig )

    unique[lig.stem.split('_')[0]] = lig


for vv in unique.values():
    print(f"Parming... {vv}")
    parameterize( vv, 'parms/')
