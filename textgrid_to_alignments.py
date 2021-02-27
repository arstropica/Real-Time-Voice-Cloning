# use a different docker image!
# make build_align && make run_align
# bin/mfa_align \
#   /datasets/CommonVoice/en/speakers \
#   /datasets/slr60/english.dict \
#   /opt/Montreal-Forced-Aligner/dist/montreal-forced-aligner/pretrained_models/english.zip \
#   /output/montreal-aligned/cv-en/
# bin/mfa_validate_dataset \
#   /datasets/slr60/test-clean \
#   /datasets/slr60/english.dict\
#   english

import sys
import tgt
from pathlib import Path
from tqdm import tqdm
import argparse
from utils.argutils import print_args

#DATASET = 'dev-clean'
#dataset_path = Path('D:/dev/repos/Real-Time-Voice-Cloning/corpus/LibriSpeech/{}'.format(DATASET))
#base_path = Path('D:/dev/repos/Real-Time-Voice-Cloning/output/montreal-aligned/{}'.format(DATASET))

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_dir", type=str, default="output/montreal-aligned/dev-clean", help=\
    "Path to the input directory that contains the montreal aligned corpus.")
parser.add_argument("-o", "--output_dir", type=str, default="corpus/LibriSpeech/dev-clean", help= \
    "Path to the output directory that will contain the alignments.")
args = parser.parse_args()
print_args(args, parser)

base_path = args.input_dir
dataset_path = args.output_dir
speaker_dirs = [f for f in base_path.glob("*") if f.is_dir()]

for speaker_dir in tqdm(speaker_dirs):
    book_dirs = [f for f in speaker_dir.glob("*") if f.is_dir()]

    for book_dir in book_dirs:
        alignment_file = dataset_path.joinpath(
            speaker_dir.stem,
            book_dir.stem,
            "{0}-{1}.alignment.txt".format(speaker_dir.stem, book_dir.stem)
        )

        with open(alignment_file, 'w', encoding='utf-8') as out_file:
            # find our textgrid files
            textgrid_files = sorted([f for f in book_dir.glob("*.TextGrid") if f.is_file()])

            # process each grid file and add to our output
            for textgrid_file in textgrid_files:
                # read the raw transcript as well
                transcript_file = dataset_path.joinpath(
                    speaker_dir.stem,
                    book_dir.stem,
                    "{0}.txt".format(textgrid_file.stem)
                )
                with open(transcript_file, 'r', encoding='utf-8') as in_file:
                    transcript = in_file.read()

                # read the grid
                input = tgt.io.read_textgrid(textgrid_file)
                print("input: {}".format(input))

                # get all the word tiers
                word_tier = input.get_tier_by_name('words')
                #print("word tier: {}".format(word_tier))
                #print("first: {}".format(word_tier.intervals[0].start_time))
                #print("last: {}".format(word_tier.end_time))
                #sys.exit(1)

                out_file.write("{0} \",{1},\" \"{2},{3},{4}\"\n".format(
                    textgrid_file.stem,
                    ",".join(list(map(lambda interval: str("" if interval.text =="<unk>" else interval.text).upper(), word_tier.intervals))),
                    str(word_tier.start_time),
                    ",".join(list(map(lambda interval: str(interval.end_time), word_tier.intervals))),
                    word_tier.end_time
                ))