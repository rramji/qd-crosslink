import argparse

def process_mol2(input_filename, output_filename):
    with open(input_filename, 'r') as f:
        lines = f.readlines()

    process = False
    new_lines = []

    for line in lines:
        if '@<TRIPOS>ATOM' in line:
            process = True
        elif '@<TRIPOS>' in line and '@<TRIPOS>ATOM' not in line:
            process = False

        if process and line.strip().split(None, 1)[0].isdigit():
            fields = line.split(None, 7)
            original_whitespace = line.index(fields[1]) - line.index(fields[0]) - len(fields[0])
            fields[1] = fields[1][0]
            new_line = fields[0] + ' ' * original_whitespace + fields[1] + ' ' + ' '.join(fields[2:])
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    with open(output_filename, 'w') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process MOL2 files.')
    parser.add_argument('input_filename', type=str, help='Path to the input MOL2 file.')
    parser.add_argument('output_filename', type=str, help='Path to the output MOL2 file.')
    args = parser.parse_args()

    process_mol2(args.input_filename, args.output_filename)

