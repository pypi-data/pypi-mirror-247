'''
Programmed by Universe Reo (AKA Zikai Liao) ©.
This script is initially from an online GitHub source. Thanks for their hardworking.
'''

import os
import cv2
import argparse
import shutil
import numpy as np
import logging

from glob import glob
from pathlib import Path
from typing import Any, Union
from joblib import Parallel, delayed
from tqdm import tqdm

_SUPPORT_VIDEO_EXTENSIONS_ = [
    '.mp4', '.avi', 'flv', 'mkv',
]

_SUPPORT_IMAGE_EXTENSIONS_ = [
    '.jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff',
]

_VID_FOURCC_ = {
    'mp4': 'avc1',  # 'h264',
    'avi': 'xvid',  # 'xvid'. 'i420' is uncompressed yuv, might be very large
    'mkv': 'h264',
    'flv': 'h264',
}


def str2bool(value: str):
    return value.lower() in ('true', 't', 'yes', 'y', '1')


class vid2img(object):

    def __init__(self,
                 vid_path: Path,
                 output_dir: Path,
                 img_ext: str,
                 height: int = None,
                 width: int = None,
                 parallel: bool = True,
                 interval: int = 1) -> None:
        self.vidPath = vid_path
        self.outputDir = output_dir
        self.imgExt = img_ext
        self.height = height
        self.width = width
        self.interval = interval

        self.parallel = parallel
        self.cores = os.cpu_count()

    def __call__(self, *args: Any, **kwds: Any):
        self._read_vid()
        self._vid2img()

    def _read_vid(self):
        vid = cv2.VideoCapture(self.vidPath)
        self.frameCnt = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

    def _get_block(self, i):
        vid = cv2.VideoCapture(str(self.vidPath))
        start = self.positions[i]
        vid.set(cv2.CAP_PROP_POS_FRAMES, start)
        return vid

    def _save_block(self, vid):
        for _ in range(self.block):
            frameCnt = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
            ret, frame = vid.read()
            if frameCnt % self.interval == 0 and ret:
                cv2.imencode(f'.{self.imgExt}', frame)[1].tofile(self.outputDir.joinpath(f'{frameCnt:04d}.{self.imgExt}'))

    def _vid2img(self):

        if self.parallel:
            self.block = self.frameCnt // (self.cores - 1)
            self.positions = list(range(0, self.frameCnt, self.block))
            try:
                proc = [delayed(self._save_block)(self._get_block(core)) for core in
                        range(self.cores)]  # If exception occurs, try: range(self.cores - 1)
            except RuntimeError as e:
                proc = [delayed(self._save_block)(self._get_block(core)) for core in
                        range(self.cores - 1)]
            except:
                logging.error('Unknown error occurred. Please contact the code maker.')

            Parallel(n_jobs=self.cores, backend='threading', verbose=1)(proc)
        else:
            vid = cv2.VideoCapture(str(self.vidPath))
            for i in range(self.frameCnt):
                ret, frame = vid.read()
                if i % self.interval == 0 and ret:
                    cv2.imencode(f'.{self.imgExt}', frame)[1].tofile(self.outputDir.joinpath(f'{i:04d}.{self.imgExt}'))


def get_arguments():
    parser = argparse.ArgumentParser()

    # Basic parameters
    parser.add_argument('--vid-path',
                        type=str,
                        default=r'',
                        required=True,
                        help='Path of video file to be converted into a set of images.')
    parser.add_argument('--output-dir',
                        type=str,
                        default=r'',
                        help='Output directory of the converted images.')
    parser.add_argument('--img-ext',
                        type=str,
                        default='png',
                        help='Extension of the converted images.')

    # Parameters for image
    parser.add_argument('-H', '--height',
                        type=int,
                        default=None,
                        help='Height of the converted images. If not set, will use video resolution.')
    parser.add_argument('-W', '--width',
                        type=int,
                        default=None,
                        help='Width of the converted images. If not set, will use video resolution.')

    # Process parameters
    parser.add_argument('-I', '--interval',
                        type=int,
                        default=1,
                        help='Interval between frames. For example, if interval is 5, then only images No. 1, 6, 11... '
                             'will be used to convert to images.')
    parser.add_argument('-P', '--parallel',
                        type=str2bool,
                        default=True,
                        help='Whether to process video-to-image in a CPU-based parallel manner.')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_arguments()
    
    '''Verification'''

    # Verify vid_path
    assert Path(args.vid_path).exists() and Path(args.vid_path).is_file(), \
        f"The file path \'{args.vid_path}\' does not exist or is not a valid video file."
    args.vid_path = Path(args.vid_path)

    # Verify output_dir
    if args.output_dir is None:
        logging.warning(f"No output directory. Will automatically create a folder at where the video is.")
        args.output_dir = args.vid_path.parent.joinpath(f'{args.vid_path.stem}_output')
        Path.mkdir(args.output_dir, exist_ok=True)
    else:
        assert Path(args.output_dir).is_dir(), f"Output directory is not valid: {args.output_dir}"
        args.output_dir = Path(args.output_dir)

    # Verify img_ext
    assert args.img_ext in _SUPPORT_IMAGE_EXTENSIONS_, (f"Image extension {args.img_ext} is not supported. "
                                                        f"Only {_SUPPORT_IMAGE_EXTENSIONS_} are currently supported.")
    
    '''End of verification'''
    
    vid2img(
        vid_path=args.vid_path,
        output_dir=args.output_dir,
        img_ext=args.img_ext,
        height=args.height,
        width=args.width,
        parallel=args.parallel,
        interval=args.interval
    )()
