import argparse
import os
import requests
import subprocess

def create_file(out_filename,in_url):
    r = requests.get(in_url, allow_redirects=True)
    open(out_filename, 'wb').write(r.content)

def run_method(output_dir, name, bam_input, ref_input, parameters):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    log_file = os.path.join(output_dir, f'{name}.log.txt')

    # Find reference position from ref_input
    with open(ref_input, 'r') as file:
        ref_pos = file.readline().strip()

    # Find wrapper for anaconda environment with BAMboozle installed
    wrapper_bamboozle = "envs/BAMboozle-0.5.0_wrapper.sh"

    # Run BAMboozle
    anon_bam_pos = f"{output_dir}/{name}.anon.bam"
    bamboozle_command = f"{wrapper_bamboozle} --bam {bam_input} --out {anon_bam_pos} --fa {ref_pos}"
    content = f"Bamboozle command:\n{bamboozle_command}\n"
    a = subprocess.run(bamboozle_command.split(),capture_output=True,text=True)
    content += f"Bamboozle output:\n"
    content += a.stdout
    content += f"\n\n"

    # Run bamtofastq through CellRanger
    # Use the wrapper in envs to load Cellranger
    wrapper_bamtofastq = "envs/CellRanger-8.0.1_wrapper.sh"

    anon_fastq_pos = f"{output_dir}/anon_fastqs"
    bamtofastq_command = f"{wrapper_bamtofastq} bamtofastq --nthreads=16 {anon_bam_pos} {anon_fastq_pos}"
    content += f"Bamtofastq command:\n{bamtofastq_command}\n"
    a = subprocess.run(bamtofastq_command.split(),capture_output=True,text=True)
    content += f"Bamtofastq output:\n{a.stdout}\n\n"

    # Find name of bamtofastq folder
    a = subprocess.run(f"ls {anon_fastq_pos}".split(),capture_output=True,text=True)
    content += f"fastq foldername object: {a.stdout}\n"
    fastq_foldername = a.stdout[:-1]
    content += f"fastq foldername: {fastq_foldername}\n\n"

    anon_read_path = os.path.join(output_dir, f'{name}.readpath.txt')
    a = subprocess.run(f"touch {anon_read_path}".split(),capture_output=True,text=True)
    content += a.stdout

    with open(anon_read_path, 'w') as file:
        file.write(anon_fastq_pos)

    # Run samtools fastq to generate fastq files
    # R1_out = f"{output_dir}/{name}.anon_R1.fastq"
    # R2_out = f"{output_dir}/{name}.anon_R2.fastq"
    # unpaired_out = f"{output_dir}/{name}.anon_unpaired.fastq"
    # bamtofastq_command = f"samtools fastq -1 {R1_out} -2 {R2_out} -s {unpaired_out} {anon_bam_pos}"
    # a = subprocess.run(bamtofastq_command.split(),capture_output=True,text=True)
    # content += f"Bamtofastq output:\n"
    # content += a.stdout
    # content += f"\n\n"

    content += f"All clear - successfull run"

    with open(log_file, 'w') as file:
        file.write(content)

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run method on files.')

    # Add arguments
    parser.add_argument('--output_dir', type=str, help='output directory where method will store results.')
    parser.add_argument('--name', type=str, help='name of the dataset')
    parser.add_argument('--init.bam',type=str, help='input file')
    parser.add_argument('--refgenome.txt',type=str, help='path to reference fasta')

    # Parse arguments
    args, extra_arguments = parser.parse_known_args()

    bam_input = getattr(args, 'init.bam')
    ref_input = getattr(args, 'refgenome.txt')

    # run_method(args.output_dir, args.name, input_files, extra_arguments)
    run_method(args.output_dir, args.name, bam_input, ref_input, extra_arguments)


if __name__ == "__main__":
    main()
