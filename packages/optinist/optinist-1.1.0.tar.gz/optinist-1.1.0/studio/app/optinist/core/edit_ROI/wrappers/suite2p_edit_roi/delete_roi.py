import os

import numpy as np

from studio.app.optinist.core.edit_ROI.wrappers.suite2p_edit_roi.utils import (
    set_nwbfile,
)
from studio.app.optinist.dataclass import RoiData, Suite2pData


def excute_delete_roi(node_dirpath, ids):
    function_id = node_dirpath.split("/")[-1]
    print("start suite2p delete_roi:", function_id)

    ops = np.load(os.path.join(node_dirpath, "suite2p.npy"), allow_pickle=True).item()
    iscell = ops.get("iscell")
    delete_roi = ops.get("delete_roi", [])
    im = ops.get("im")

    delete_roi = ops.get("delete_roi") if ops.get("delete_roi") else []
    for id in ids:
        iscell[id] = False
        delete_roi.append(id)

    ops["iscell"] = iscell
    ops["delete_roi"] = delete_roi

    info = {
        "ops": Suite2pData(ops),
        "non_cell_roi": RoiData(
            np.nanmax(im[~iscell], axis=0),
            output_dir=node_dirpath,
            file_name="noncell_roi",
        ),
        "cell_roi": RoiData(
            np.nanmax(im[iscell], axis=0), output_dir=node_dirpath, file_name="cell_roi"
        ),
        "nwbfile": set_nwbfile(ops, function_id),
    }

    return info
