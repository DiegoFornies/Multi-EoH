import csv
import ast

def get_best_heuristic(execution_name):
    with open(f'ejecuciones/{execution_name}/best_heuristics.txt', 'r', encoding='utf-8') as infile:
        data = infile.read()

    heuristics = {}
    raw_heuristics = data.split('Heuristic id:')[1:]

    for heuristic_block in raw_heuristics:
        heuristic_id_line, base_evaluation_line = heuristic_block.strip().split("\n", 1)
        heuristic_id = int(heuristic_id_line.strip())

        base_evaluation = ast.literal_eval(base_evaluation_line.strip().split("Base evaluation:")[-1].strip())
        heuristics[heuristic_id] = base_evaluation
    return heuristics
