import os
import cv2
import numpy as np

import argparse
import logging
from pathlib import Path
from typing import *  # Any, Union, List, Optional
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


def str2bool(v: str) -> bool:
    return v.lower() in ('yes', 'true', 't', 'y', '1')


def argparser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='A converter to convert images to videos.')

    '''Overall parameters'''
    parser.add_argument('--img-dir',
                        type=str,
                        default=r"I:\图\DRONE",
                        require=True,
                        help='Directory with images to convert.')
    parser.add_argument('--img-ext',
                        type=str,
                        default=None,
                        help='Extension of images to convert. If not provided, will default to mixed extensions.')
    parser.add_argument('--output-dir',
                        type=str,
                        default=None,
                        help='Directory to save converted video. If not provided, will default to the images directory.')
    parser.add_argument('--vid-ext',
                        type=str,
                        default=None,
                        help='Extension of video to convert. If not provided, will default to .mp4.')

    '''Video parameters'''
    parser.add_argument('--fps',
                        type=int,
                        default=30,
                        help='Frames per second for the converted video.')
    parser.add_argument('-H', '--height',
                        type=int,
                        default=None,
                        help='Height of the converted video.')
    parser.add_argument('-W', '--width',
                        type=int,
                        default=None,
                        help='Width of the converted video.')

    '''Process parameters'''
    # TODO: Is there a way to parallel-process this?

    parser.add_argument('--sort-img',
                        type=str,
                        # action='store_true',
                        default='no',
                        help='Whether to sort images. If input \'ascending\', the images will be sorted in ascending '
                             'way; if input \'descending\', the images will be sorted in descending way; if default '
                             'to None (not None in string), the images will be arranged by the glob mechanism.')
    parser.add_argument('--interval',
                        type=int,
                        default=1,
                        help='Interval of images. For example, if interval is 5, then only images No. 1, 6, 11, 16... '
                             'will be used to convert into a video.')

    return parser.parse_args()


class img2vid(object):

    def __init__(self,
                 img_dir: Path,
                 img_ext: Union[str, List[str], None],
                 output_dir: Path,
                 vid_ext: str,
                 # parallel,
                 fps: int,
                 height: int,
                 width: int,
                 sort_img: str = 'no',
                 interval: int = 1):
        """
        Convert images to one video.

        :param img_dir: The directory containing images to be converted in a video.
        :param img_ext: The extension of the images to be converted in a video.
        :param output_dir: The output directory for the video to be converted.
        :param vid_ext: The extension of the video to be converted.
        # :param parallel: Whether to initialize CPU-based parallel processing to convert.
        :param fps: Frames per second for the converted video.
        :param height: Height of the converted video.
        :param width: Width of the converted video.
        :param sort_img: Whether to sort images before converting them.
        :param interval: Gap between the images to be gathered and converted.
        """

        self.imgDir = img_dir
        self.imgExt = img_ext
        self.outputDir = output_dir
        self.vidExt = vid_ext

        self.interval = interval
        self.fps = fps
        self.height = height
        self.width = width

        self.sortImg = sort_img
        # self.parallel = parallel
        # self.cores = os.cpu_count()

    def __call__(self):
        self._read_imgs()
        self._img2vid()

    def _read_imgs(self):

        # TODO:
        #  1. Get all images of supported formats.  [⍻]
        #  2. Verify height and width of all images.  [⍻]
        #  3. Define new video regardless of the video extension.  [×]
        #  4. Sort images according to filenames.  [⍻]

        # Get paths of all images
        self.imgPaths = self._get_all_images(self.imgDir, self.imgExt)

        # Get height and width of the converted video.
        self.height, self.width = self._get_h_and_w(self.imgPaths) if self.height is None and self.width is None \
            else (self.height, self.width)

        # Set the extension of the converted video.
        if self.vidExt is None:
            logging.warning("No converted video extension is given. Will set the video extension to .mp4.")
            self.vidExt = 'mp4'

        # Initialize the video writer.
        self.vw = cv2.VideoWriter(Path.joinpath(self.outputDir, f'{self.imgDir.stem}_Video.{self.vidExt}').as_posix(),
                                  cv2.VideoWriter_fourcc(*_VID_FOURCC_[self.vidExt].upper()),
                                  self.fps, (self.width, self.height))

    def _get_all_images(self, _dir: Path, _ext: Union[str, List[str], None], _sort: bool = False) -> List[Path]:
        paths = list()

        if _ext:
            if isinstance(_ext, str):
                paths.extend(list(Path(_dir).glob(f'*.{_ext}')))
            elif isinstance(_ext, list):
                for ext in _ext:
                    paths.extend(list(Path(_dir).glob(f'*.{ext}')))
        else:
            logging.warning("No specific extension of images is given. Will only get support type of images.")
            for ext in _SUPPORT_IMAGE_EXTENSIONS_:
                paths.extend(list(Path(_dir).glob(f'*.{ext}')))

        if _sort is not None:
            paths = sorted(paths, key=lambda x: Path(x).stem, reverse=True if _sort == "descending" else False)

        return paths

    def _get_h_and_w(self, _paths: List[Path]) -> Tuple[int, int]:
        logging.warning("No height and width are given. Will only automatically set width and height.")

        max_h, max_w = -1, -1
        for _path in tqdm(_paths, desc="Getting the height and width"):
            assert _path.exists(), f"Path \"{_path}\" does not exist."
            img = cv2.imdecode(np.fromfile(_path.as_posix(), dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
            h, w = img.shape
            max_h = h if h > max_h else max_h
            max_w = w if w > max_w else max_w

        return max_h, max_w

    def _img2vid(self):
        for i, path in tqdm(enumerate(self.imgPaths), desc='Converting images to one video'):
            if not i % self.interval:
                img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                self.vw.write(img)
        self.vw.release()
        print(f"The video is successfully converted to {self.outputDir}.")


if __name__ == '__main__':
    args = argparser()

    '''Verification'''
    # Verify img_dir
    assert Path(args.img_dir).exists() and Path(args.img_dir).is_dir(), \
        f"The directory \'{args.img_dir}\' does not exist or is not a directory."
    args.img_dir = Path(args.img_dir)

    # Verify img_ext
    assert args.img_ext in _SUPPORT_IMAGE_EXTENSIONS_, (f"Image extension {args.img_ext} is not supported. "
                                                        f"Only {_SUPPORT_IMAGE_EXTENSIONS_} are currently supported.")

    # Verify output_dir
    if args.output_dir is None:
        logging.warning(f"No output directory. The output directory will be set in the input directory.")
        args.output_dir = args.img_dir.joinpath('output')
        Path.mkdir(args.output_dir, exist_ok=True)
    else:
        assert Path(args.output_dir).is_dir(), f"Output directory is not valid: {args.output_dir}"
        args.output_dir = Path(args.output_dir)

    # Verify vid_ext
    assert args.vid_ext in _SUPPORT_VIDEO_EXTENSIONS_, (f"Video extension {args.vid_ext} is not supported. "
                                                        f"Only {_SUPPORT_VIDEO_EXTENSIONS_} are currently supported.")

    # Verify sort_img
    assert args.sort_img in ['ascending', 'descending', 'no'], \
        "Sort image must be 'ascending' or 'descending'. Otherwise, don't set this."

    '''End of verification'''

    img2vid(
        img_dir=args.img_dir,
        img_ext=args.img_ext,
        output_dir=args.output_dir,
        vid_ext=args.vid_ext,
        # parallel=args.parallel,
        fps=args.fps,
        height=args.height,
        width=args.width,
        sort_img=args.sort_img,
    )()
