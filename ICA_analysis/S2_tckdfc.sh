#!/bin/bash
start_time=`date +%s`
Path=/path/to/data
CPU_COUNT=$(nproc)
MAX_CONCURRENT=$((CPU_COUNT - 5))

BASE_PATH="/path/to/fMRI"
RESTING_STATE_PATH="$BASE_PATH/resting_state"
DFC_PATH="$BASE_PATH/dfc/dfc_swm"

[ -e /tmp/fd1 ] || mkfifo /tmp/fd1
exec 3<>/tmp/fd1
rm -rf /tmp/fd1
for ((i=1; i<=5; i++)); do
    echo >&3
done

for folderpath in `ls /path/to/fMRI/HCP3T/resting_state`
do
read -u3
{
    folder="${folderpath: -6}"
    echo ${folder}
    # OUTPATH1=${DFC_PATH}/${folder}.mif
    # tckdfc /path/to/HCP_merged_tck/${folder}.tck /path/to/fMRI/dfc/BOLD/${folder}/BOLD_MNI.nii.gz ${OUTPATH1} -static -backtrack -nthreads 4 -vox 2
     
    OUTPATH2=${DFC_PATH}/${folder}_swm.nii.gz
    if [ ! -e ${OUTPATH2} ]; then
        tckdfc /path/to/swm/subject_swm/${folder}_swm.tck /path/to/fMRI/HCP3T/resting_state/${folder}/MNINonLinear/Results/rfMRI_REST2_LR/rfMRI_REST2_LR_hp2000_clean_filter.nii.gz ${OUTPATH2} -dynamic hamming 55 -backtrack -nthreads 4 -vox 2
    else
        echo "the file ${OUTPATH2} already exists"
    fi
    
    echo done for ${folder}
    echo >&3
}&
done
wait

stop_time=`date +%s`
echo "TIME:`expr $stop_time - $start_time`"
exec 3<&-
exec 3>&-

