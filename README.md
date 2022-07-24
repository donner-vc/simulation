# Donner: Domino attack simulation

A simulation measuring the damage each group of nodes can cause by performing the Domino attack on the Lightning Network.
We say an attacker controls a group of nodes, if they share the same alias, a heuristic pointed out in [1].
For each alias, we simulate that an attacker utilizes all of his/her channels to perform the Domino attack.
In practice, this is done by opening and subsequently closing a virtual channel over a victim path.
We compute for each alias the number of channels that can be closed. 
Note that this number is not optimal, as we use a greedy heuristic to identify which channels to close.


[1] M. Romiti, F. Victor, P. Moreno-Sanchez, P. S. Nordholt, B. Haslhofer, and M. Maffei, “Cross-layer deanonymization methods in the lightning protocol", in International Conference on Financial Cryptography and Data Security. 2021.

## Usage:

- Install Python >= 3.9.13
- Install dependencies (check requirements.txt)
- execute main.py > results.csv
- Inspect results.csv (The results are already precomputed in results_precomputed.csv)
- optional: Run stats.py to gain additional insights on the Lightning Network snapshot