import os
import shutil
from pathlib import Path
import enzy_htp as eh







for lig in Path('../cleaned/').rglob('???_?.mol2'):
    
    os.system('/sb/apps/moe/bin/moebatch -script cmd.svl')
    shutil.copy(lig, 'temp.mol2')
    #shutil.copy(lig, 'temp.mol2')
    print(eh.interface.pymol.get_charge('temp.mol2'))
    break
    print(lig)
