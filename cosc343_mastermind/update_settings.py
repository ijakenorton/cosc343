def update_settings(sample, lower_bound):
    with open('settings.py', 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "sample" in line:
            lines[i] = '   "sample": {},\n'.format(sample)
        elif "lower_bound" in line:
            lines[i] = '   "lower_bound": {},\n'.format(lower_bound)

    with open('settings.py', 'w') as f:
        f.writelines(lines)
