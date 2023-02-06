import shutil
from pathlib import Path
from copy import deepcopy
from pymol import cmd, stored
from Bio.PDB.Polypeptide import is_aa


from pdb2pqr.main import main_driver as run_pdb2pqr
from pdb2pqr.main import build_main_parser as build_pdb2pqr_parser


from enzy_htp import PDBParser
from enzy_htp.preparation import protonate_stru

def get_res_mapper( sele ):
    stored.holder = set()

    cmd.iterate( sele, 'stored.holder.add( ( chain, resi, resn ))' )

    return deepcopy( stored.holder )

for dname in sorted(Path('.').glob('????')):
    
    if str(dname).find('temp') != -1:
        continue

    if not dname.is_dir():
        continue


    if str(dname) != '1jg4':
        continue
    else:
        print(dname)


    fl = dname / "for_leap.pdb"
    prot = dname / "protonated.pdb"
    #if prot.exists():
    #    continue

    sp = PDBParser()
    
    stru = sp.get_structure(str(fl))
    #remove_solvent(stru)
    protonate_stru(stru, protonate_ligand = False)
    pdb_str = sp.get_file_str(stru)
    
    with open(prot, "w") as of:
        of.write(pdb_str)

    

#pdb_str = sp.get_file_str(stru)
#with open("3r24_ah.pdb", "w") as of:
    #of.write(pdb_str)



#AMBER="HIE HID".split()
#
#for dname in Path('.').glob('????'):
#    if not dname.is_dir():
#        continue
#
#    full, for_leap, for_leap_bk = dname / 'full.pdb', dname / 'for_leap.pdb', dname / 'for_leap.pdb.bk'
#
#    print( dname )
#    if not full.exists():
#        print('skipped... no missing loops')
#        continue
#    
#    if not for_leap_bk.exists():
#        shutil.copy(for_leap, for_leap_bk)
#
#    cmd.delete('all')
#    cmd.load(full)
#    cmd.load(for_leap)
#    stored.holder = []
#    cmd.iterate('for_leap', 'stored.holder.append( ( chain, resi, resn ))' )
#
#    for (chain, resi, resn ) in set(stored.holder):
#        if not is_aa(resn) and resn not in AMBER:   
#            print(resn)
#            continue
#        cmd.remove(f'for_leap//{chain}/{resi}/' )
#
#    #print(stored.holder)
#    cmd.save(for_leap)
#    cmd.delete('all')
