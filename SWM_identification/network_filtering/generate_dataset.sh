#!/bin/bash

# Base paths — replace these with your actual paths
BASE_DIR="/path/to/Atlas/ORG"
CLUSTERS_DIR="${BASE_DIR}/Clusters_800"
DEFORMATION_DIR="${BASE_DIR}/DeformationField"
OUTPUT_BASE="/path/to/swm/data_swm+nonswm"

# Initialize an array from 001 to 800 (zero-padded)
full_range=($(seq -w 001 800))

# Array to store extracted cluster IDs
extracted_chars=()

# Iterate through directories starting with T_Sup*
for dir in "${BASE_DIR}"/AnatomicalClusters/T_Sup*; do
    if [ -d "$dir" ]; then
        for file in "$dir"/*; do
            filename=$(basename "$file")
            # Remove file extension and get last three characters
            base="${filename%.*}"
            last_three="${base: -3}"
            extracted_chars+=("$last_three")
        done
    fi
done

# Remove duplicates and sort
unique_chars=($(echo "${extracted_chars[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' '))
echo "SWM clusters: ${unique_chars[@]}"

# Array to store missing cluster IDs
missing_chars=()

# Find missing clusters not in unique_chars
for number in "${full_range[@]}"; do
    if [[ ! " ${unique_chars[@]} " =~ " $number " ]]; then
        missing_chars+=("$number")
    fi
done

echo "Non-SWM clusters: ${missing_chars[@]}"

cd "${CLUSTERS_DIR}" || exit

# Process training samples (1 to 5)
for j in {A..H}; do
    for i in {1..5}; do
        filename="${j}_${i}"
        folderpath="${OUTPUT_BASE}/train/${filename}"
        mkdir -p "${folderpath}/dwm" "${folderpath}/swm"
        echo "Processing ${folderpath}"

        for num in "${unique_chars[@]}"; do
            tcktransform "cluster_00${num}.tck" "${DEFORMATION_DIR}/${filename}.mif" "${folderpath}/swm/cluster_00${num}.tck"
        done
        for num in "${missing_chars[@]}"; do
            tcktransform "cluster_00${num}.tck" "${DEFORMATION_DIR}/${filename}.mif" "${folderpath}/dwm/cluster_00${num}.tck"
        done
    done
done

# Process validation samples (6 to 8)
for j in {A..H}; do
    for i in {6..8}; do
        filename="${j}_${i}"
        folderpath="${OUTPUT_BASE}/val/${filename}"
        mkdir -p "${folderpath}/dwm" "${folderpath}/swm"
        echo "Processing ${folderpath}"

        for num in "${unique_chars[@]}"; do
            tcktransform "cluster_00${num}.tck" "${DEFORMATION_DIR}/${filename}.mif" "${folderpath}/swm/cluster_00${num}.tck"
        done
        for num in "${missing_chars[@]}"; do
            tcktransform "cluster_00${num}.tck" "${DEFORMATION_DIR}/${filename}.mif" "${folderpath}/dwm/cluster_00${num}.tck"
        done
    done
done

# Process testing samples (9 to 11)
for j in {A..H}; do
    for i in {9..11}; do
        filename="${j}_${i}"
        folderpath="${OUTPUT_BASE}/test/${filename}"
        mkdir -p "${folderpath}/dwm" "${folderpath}/swm"
        echo "Processing ${folderpath}"

        for num in "${unique_chars[@]}"; do
            tcktransform "cluster_00${num}.tck" "${DEFORMATION_DIR}/${filename}.mif" "${folderpath}/swm/cluster_00${num}.tck"
        done
        for num in "${missing_chars[@]}"; do
            tcktransform "cluster_00${num}.tck" "${DEFORMATION_DIR}/${filename}.mif" "${folderpath}/dwm/cluster_00${num}.tck"
        done
    done
done
