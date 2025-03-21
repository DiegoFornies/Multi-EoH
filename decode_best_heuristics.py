import csv
import ast

def parse_and_write_to_csv(input_filename, output_filename):
    try:
        # Leer el archivo de entrada
        with open(input_filename, 'r', encoding='utf-8') as infile:
            data = infile.read()

        # Convertir los datos leídos a un formato adecuado
        heuristics = {}
        # Esto supone que los datos están formateados como texto Python (diccionarios y listas)
        raw_heuristics = data.split('Heuristic id:')[1:]

        # Parsear cada bloque de heurístico
        for heuristic_block in raw_heuristics:
            heuristic_id_line, base_evaluation_line = heuristic_block.strip().split("\n", 1)
            heuristic_id = int(heuristic_id_line.strip())

            # Convertir la evaluación base en un diccionario de instancias
            base_evaluation = ast.literal_eval(base_evaluation_line.strip().split("Base evaluation:")[-1].strip())
            heuristics[heuristic_id] = base_evaluation

        # Crear el archivo CSV de salida
        with open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
            # Escribimos el encabezado con los nombres de las instancias
            fieldnames = ['Heuristic ID'] + [f'mk{i:02d}.txt_Makespan' for i in range(16)] + \
                         [f'mk{i:02d}.txt_Separation' for i in range(16)] + \
                         [f'mk{i:02d}.txt_Balance' for i in range(16)]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            # Escribir cada heurístico y sus valores correspondientes en el CSV
            for heuristic_id, evaluations in heuristics.items():
                row = {'Heuristic ID': heuristic_id}
                for instance, metrics in evaluations.items():
                    # Añadir los valores de makespan, separation y balance para cada instancia en columnas separadas
                    row[f'{instance}_Makespan'] = metrics['Makespan']
                    row[f'{instance}_Separation'] = metrics['Separation']
                    row[f'{instance}_Balance'] = metrics['Balance']
                writer.writerow(row)

        print(f"Archivo '{output_filename}' generado exitosamente.")

    except Exception as e:
        print(f"Hubo un error: {e}")

# Llamada a la función con los archivos de entrada y salida
parse_and_write_to_csv('ejecuciones/folder_2025-03-21_11-00-44/best_heuristics.txt', 'output.csv')
