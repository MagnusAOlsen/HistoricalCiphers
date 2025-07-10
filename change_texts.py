def change(file):
    with open(file, 'r') as f:
        data = f.read().strip()
        data = data.replace(',', '0')
        data = data.replace('.', '1')
        data = data.replace('-', '2')
    
    with open('text_files/alphanumerical.txt', 'w') as f:
        f.write(data)


change('text_files/3.txt')