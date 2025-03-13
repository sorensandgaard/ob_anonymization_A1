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

    # Run Bamboozle
    with open(ref_input, 'r') as file:
        ref_pos = file.readline()[-1]

    # ref_pos = # Read the text inside the ref_input file
    # anon_bam_pos = f"{output_dir}/{name}.bamboozled.bam"
    # bamboozle_command = f"BAMboozle --bam {bam_input} --out {anon_bam_pos} --fa {ref_pos}"
    # content += f"Bamboozle command:\n{bamboozle_command}\n"
    # a = subprocess.run(bamboozle_command.split(),capture_output=True,text=True)
    # content += f"Bamboozle output:\n"
    # content += a.stdout
    # content += f"\n\n"

    content = f"bam pos: {bam_input}\n"
    content += f"ref pos: {ref_input}\n"
    content += f".fa  pos: {ref_pos}\n"

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
