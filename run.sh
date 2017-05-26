#!/bin/bash

usage () {
  echo "Generate rollsum stats from testdata.
Usage: $0 [-N] [-B <blocksize>] [-C <blockcount>] [<outdir>]

Where:
  -N regenerate summary files only.
  <blocksize> is the blocksize with optional K, or M suffix.
  <blockcount> is the number of blocks to generate stats for.
  <outdir> is the directory to write results to (default: .).
"
  exit 1
}

OPTIONS=$(getopt 'NB:C:h?' "$@")
[ $? == 0 ] || usage
eval set -- "$OPTIONS"

BLOCKSIZE=1K
BLOCKCOUNT=10000
while true;  do
  case "$1" in
    -N ) SKIPTESTS=1; shift ;;
    -B ) BLOCKSIZE=$2; shift 2 ;;
    -C ) BLOCKCOUNT=$2; shift 2 ;;
    -h ) usage ;;
    -- ) shift; break ;;
  esac
done
OUTDIR=${1:-.}

rollsum () {
  # rollsum <seed> <offs> <base> <map> <zip|cvs>
  args="-C ${BLOCKCOUNT} -B ${BLOCKSIZE} --seed=$1 --offs=$2 --base=$3 --map=$4"
  echo "doing ${args} <data/$5.dat"
  ./rollsum.py ${args} <data/$5.dat >${OUTDIR}/$5-${BLOCKSIZE}-$1-$2-$3-$4.txt
}

runtests () {
  # runtests <src>
  # Do librsync.
  rollsum 0 31 0x10000 ord $1
  # Do map=mul.
  rollsum 1 0 0xffff mul $1
  for base in 0x10000 0xffff 0xfff1; do
    for map in ord pow; do
      rollsum 1 0 ${base} ${map} $1
    done
  done
}  

for src in csv zip; do
  [ -z $SKIPTESTS ] && runtests ${src}
  for s in 'rollsum' 's1sum' 's2sum' 'mask_fff' 'mod_fff'; do
    for f in ${OUTDIR}/${src}-${BLOCKSIZE}-*-*-*-*.txt; do
      run=$(sed -n '/Results/ {s:Results for ::; p}' $f)
      stats=$(sed -n "/^$s:/ {s:.* min/:min:; p}" $f)
      echo ${run} ${stats}
    done | sort -n -t/ -k6 > ${OUTDIR}/${src}-${BLOCKSIZE}-${s}-summary.txt
  done
done
