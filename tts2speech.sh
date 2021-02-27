#!/bin/bash

DATASET="$(realpath -s $1)/*/"
for speakers in $DATASET
do 
    if [ -d "${speakers}" ]; then
        speaker=$(basename "${speakers%*/}")
        echo "Found speaker: $speakers"
        PSPEAKERS="$(realpath -s $speakers)/*/"
        for chapters in $PSPEAKERS
        do
            if [ -d "$chapters" ]; then
                chapter=$(basename "$chapters")
                echo "Found chapter: $chapter"
                outfile="${chapters%/*}/${speaker}-${chapter}.trans.txt"
                echo "outfile: $outfile ..."
                declare -a trans
                audio="${chapters}/*.mp3"
                for f in $audio
                do
                    fpath=${f%/*}
                    fname=${f##*/}
                    fbase=${fname%.*}
                    #echo "Processing $fname file... on path $fpath"
                    #echo "Looking for ${fbase}.txt ..."
                    tpt="${fpath}/${fbase}.txt"
                    if [ -f "${tpt}" ]; then
                        cnt=$(<$tpt)
                        #echo "Found  ${fbase}.txt ..."
                        trans+=("${fbase} ${cnt^^}")
                    else
                        echo "Did not find  ${fbase}.txt ..." 
                    fi
                done
                { [ "${#trans[@]}" -eq 0 ] || printf '%s\n' "${trans[@]}"; } > $outfile
                unset trans
            fi
        done
    fi
done
