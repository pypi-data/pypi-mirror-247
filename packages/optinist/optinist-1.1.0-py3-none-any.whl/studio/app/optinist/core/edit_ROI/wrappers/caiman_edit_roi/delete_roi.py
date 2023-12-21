from studio.app.optinist.core.edit_ROI.wrappers.caiman_edit_roi.utils import set_nwbfile
from studio.app.optinist.dataclass import CaimanCnmfData, RoiData


def excute_delete_roi(node_dirpath, ids):
    import numpy as np

    function_id = node_dirpath.split("/")[-1]
    print("start caiman delete_roi:", function_id)

    # load data
    cnmf_data = np.load(f"{node_dirpath}/caiman_cnmf.npy", allow_pickle=True).item()
    is_cell = cnmf_data.get("is_cell")
    delete_roi = cnmf_data.get("delete_roi", [])
    im = cnmf_data.get("im")

    # delete ROI
    is_cell[ids] = False
    delete_roi += ids

    cell_roi = np.zeros(im.shape)
    num_rois = im.shape[0]
    for i in range(num_rois):
        cell_roi[i, :, :] = np.where(im[i, :, :] != 0, i + 1, np.nan)
    cell_roi -= 1

    cnmf_data["is_cell"] = is_cell
    cnmf_data["delete_roi"] = delete_roi
    info = {
        "cell_roi": RoiData(
            np.nanmax(cell_roi[is_cell], axis=0),
            output_dir=node_dirpath,
            file_name="cell_roi",
        ),
        "cnmf_data": CaimanCnmfData(cnmf_data),
        "nwbfile": set_nwbfile(cnmf_data, function_id),
    }
    return info
