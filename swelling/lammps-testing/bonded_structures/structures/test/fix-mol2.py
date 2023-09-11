def modify_mol2_atom_field(input_file, output_file):
    with open(input_file, 'r') as f:
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

    with open(output_file, 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    input_file = "additive-bonded-at-base.mol2"  # Replace with the name of your input file
    output_file = "modified_output_file.mol2"  # Replace with the name you want for the output file
    modify_mol2_atom_field(input_file, output_file)

