import shutil
from pathlib import Path
from typing import Optional

import cv2
import numpy as np

from mhdwriter.args import WriteArgs, WriteType
from mhdwriter.header import generate_header


def write_mhd_raw(
    input_dir: Path, args: WriteArgs, out_path: Optional[Path] = None
) -> bool:
    """
    Convert a stack of files in a directory to a mhd/raw pair.

    Args:
        input_dir (Path): The directory containing the stack of files to convert to a volume.
        args (WriteArgs): WriteArgs object specifying parameters for the MHD header creation.
        out_path (Path): Optional path to specify output directory/file_base. If missing, metadata will be used
            to determine output file/path name in the input_dir.

    Returns:
        bool: Returns True upon successful mhd/raw creation, else False.

    """
    all_files = list(input_dir.glob("*"))
    all_files = [
        f
        for f in all_files
        if f.suffix.lower()
        in [".jpg", ".jxl", ".jp2", ".jpeg", ".png", ".tif", ".tiff"]
    ]
    img = cv2.imread(str(all_files[0]), cv2.IMREAD_UNCHANGED)
    args.height, args.width = img.shape[:2]
    if args.downsample_factor > 0:
        dx_factor = 2 ** args.downsample_factor
        args.height = args.height//dx_factor
        args.width = args.width//dx_factor
    args.length = len(all_files)
    metadata = generate_header(args)

    if not input_dir.exists():
        raise FileNotFoundError(f"Missing input dir {input_dir}")

    if out_path is None:
        if args.write_type == WriteType.NONE:
            out_path = input_dir
        else:
            out_path = input_dir.joinpath(f"{metadata['ElementDataFile']}")

    with out_path.open(mode="wb") as outfile:
        for idx, img_file in enumerate(all_files):
            try:
                img = cv2.imread(str(img_file), cv2.IMREAD_UNCHANGED)
            except Exception as e:
                print(f"Error reading {str(img_file)}: {e}")
                continue
            if img is None:
                print(f"Error reading {str(img_file)}")
                continue
            if args.is_rgb:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            if args.downsample_factor > 0:
                img = cv2.resize(
                    img, (args.width, args.height), interpolation=cv2.INTER_AREA
                )

            if args.write_type == WriteType.NONE:
                file_path = out_path.joinpath("slice_{0:04d}.jpg".format(idx + 1))
                cv2.imwrite(str(file_path), img)
            else:
                squeezed = np.squeeze(img)
                outfile.write(squeezed.tobytes())

    if not out_path.exists():
        return False
    mhd_path = out_path.parent.joinpath(f"{out_path.stem}.mhd")
    with mhd_path.open("w") as mhd:
        for key in metadata:
            mhd.write(f"{key} = {metadata[key]}\n")
    return True
