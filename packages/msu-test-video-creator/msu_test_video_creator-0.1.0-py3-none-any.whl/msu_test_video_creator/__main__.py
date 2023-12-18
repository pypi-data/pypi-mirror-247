import logging
import sys
import argparse

from .video_creator import VideoCreator
from . import __version__

def cli():
    try:
        parser = argparse.ArgumentParser("msu_test_video_creator", description="Commandline Python application for generating mp4 and wav files for an msu")
        parser.add_argument("-f", "--files", help="The list of PCM files to include", type=str)
        parser.add_argument("-o", "--output", help="The output mp4 file to create", type=str)
        parser.add_argument("-v", "--version", help="Get the version number", action='store_true')
        args = parser.parse_args()

        if args.version == True:
            print("msu_test_video_creator v"+__version__)
            exit(1)

        if not args.files:
            print("usage: msu_test_video_creator [-h] [-f FILES] [-v]")
            print("msu_test_video_creator: error: the following arguments are required: -f/--files")
            exit(1)

        if not args.output:
            print("usage: msu_test_video_creator [-h] [-f FILES] [-o OUTPUT] [-v]")
            print("msu_test_video_creator: error: the following arguments are required: -o/--output")
            exit(1)

        pcm_files = args.files.split(",")

        print(pcm_files)

        creator = VideoCreator(pcm_files, args.output)

        creator.create_video()

        exit(0)
        
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    cli()