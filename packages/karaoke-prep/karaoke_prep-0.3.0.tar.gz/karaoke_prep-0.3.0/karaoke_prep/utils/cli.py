#!/usr/bin/env python
import argparse
import logging
import pkg_resources
from karaoke_prep import KaraokePrep


def main():
    logger = logging.getLogger(__name__)
    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(fmt="%(asctime)s.%(msecs)03d - %(levelname)s - %(module)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)

    parser = argparse.ArgumentParser(
        description="Fetch audio and lyrics for a specified song, to prepare karaoke video creation.",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=50),
    )

    parser.add_argument("url", nargs="?", help="YouTube URL of the song to prep.", default=None)
    parser.add_argument("artist", nargs="?", help="Artist name for the song to prep.", default=None)
    parser.add_argument("title", nargs="?", help="Title of the song to prep.", default=None)

    package_version = pkg_resources.get_distribution("karaoke-prep").version
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {package_version}")

    parser.add_argument(
        "--log_level",
        default="info",
        help="Optional: logging level, e.g. info, debug, warning (default: %(default)s). Example: --log_level=debug",
    )

    parser.add_argument(
        "--model_name",
        default="UVR_MDXNET_KARA_2",
        help="Optional: model name to be used for separation (default: %(default)s). Example: --model_name=UVR-MDX-NET-Inst_HQ_3",
    )

    parser.add_argument(
        "--model_file_dir",
        default="/tmp/audio-separator-models/",
        help="Optional: model files directory (default: %(default)s). Example: --model_file_dir=/app/models",
    )

    parser.add_argument(
        "--output_dir",
        default=".",
        help="Optional: directory to write output files (default: <current dir>). Example: --output_dir=/app/karaoke",
    )

    parser.add_argument(
        "--output_format",
        default="MP3",
        help="Optional: output format for separated audio (default: MP3). Example: --output_format=FLAC",
    )

    parser.add_argument(
        "--use_cuda",
        action="store_true",
        help="Optional: use Nvidia GPU with CUDA for separation (default: %(default)s). Example: --use_cuda=true",
    )

    parser.add_argument(
        "--use_coreml",
        action="store_true",
        help="Optional: use Apple Silicon GPU with CoreML for separation (default: %(default)s). Example: --use_coreml=true",
    )

    parser.add_argument(
        "--denoise",
        type=lambda x: (str(x).lower() == "true"),
        default=True,
        help="Optional: enable or disable denoising during separation (default: %(default)s). Example: --denoise=False",
    )

    parser.add_argument(
        "--normalize",
        type=lambda x: (str(x).lower() == "true"),
        default=True,
        help="Optional: enable or disable normalization during separation (default: %(default)s). Example: --normalize=False",
    )

    parser.add_argument(
        "--no_track_subfolders",
        action="store_false",
        help="Optional: do NOT create a named subfolder for each track. Example: --no_track_subfolders",
    )

    args = parser.parse_args()

    log_level = getattr(logging, args.log_level.upper())
    logger.setLevel(log_level)

    if not hasattr(args, "artist") or not hasattr(args, "title"):
        if not args.url:
            parser.print_help()
            exit(1)
        else:
            # Proceed with only URL
            logger.info("Artist and title will be guessed from the provided URL.")

    logger.info(f"KaraokePrep beginning with url: {args.url} artist: {args.artist} and title: {args.title}")

    kprep = KaraokePrep(
        artist=args.artist,
        title=args.title,
        url=args.url,
        log_formatter=log_formatter,
        log_level=log_level,
        model_name=args.model_name,
        model_file_dir=args.model_file_dir,
        output_dir=args.output_dir,
        output_format=args.output_format,
        use_cuda=args.use_cuda,
        use_coreml=args.use_coreml,
        normalization_enabled=args.normalize,
        denoise_enabled=args.denoise,
        create_track_subfolders=args.no_track_subfolders,
    )

    track = kprep.prep()

    logger.info(f"Karaoke Prep complete! Output files:")

    logger.info(f"")
    logger.info(f"Track: {track['artist']} - {track['title']}")
    logger.info(f" YouTube Video: {track['youtube_video']}")
    logger.info(f" YouTube Audio: {track['youtube_audio']}")
    logger.info(f" YouTube Still Image: {track['youtube_still_image']}")
    logger.info(f" Lyrics: {track['lyrics']}")
    logger.info(f" Instrumental: {track['instrumental_audio']}")
    logger.info(f" Vocals: {track['vocals_audio']}")


if __name__ == "__main__":
    main()
