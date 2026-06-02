#!/usr/bin/env python3

input_file = "C240Na6.xyz"     # TU archivo XYZ
output_file = "geometry.in"

cell_length = 35.0
cell_center = cell_length / 2.0

header = """#============================================
# FHI-aims geometry.in
# System: Carbon fullerene + Na dimer
# PBC: 7x7 slab with large vacuum in z
#============================================
lattice_vector 35.00000000 0.0 0.0
lattice_vector 0.0 35.00000000 0.0
lattice_vector 0.0 0.0 35.00000000

"""

atoms = []

with open(input_file, "r") as f:
    lines = f.readlines()

# Verificación mínima
if len(lines) < 3:
    raise ValueError("El archivo XYZ no es válido.")

# Número de átomos (opcional pero útil)
try:
    n_atoms = int(lines[0].strip())
except ValueError:
    raise ValueError("La primera línea no contiene el número de átomos.")

coord_lines = lines[2:]  # saltamos N y Energy

for line in coord_lines:
    line = line.strip()
    if not line:
        continue

    parts = line.split()
    if len(parts) != 4:
        raise ValueError(f"Línea mal formada: {line}")

    element = parts[0]
    x, y, z = map(float, parts[1:])
    atoms.append([x, y, z, element])

if len(atoms) != n_atoms:
    print(f"⚠ Aviso: se esperaban {n_atoms} átomos, se leyeron {len(atoms)}")

# Centro geométrico
x_avg = sum(a[0] for a in atoms) / len(atoms)
y_avg = sum(a[1] for a in atoms) / len(atoms)
z_avg = sum(a[2] for a in atoms) / len(atoms)

dx = cell_center - x_avg
dy = cell_center - y_avg
dz = cell_center - z_avg

with open(output_file, "w") as f:
    f.write(header)
    for x, y, z, el in atoms:
        f.write(
            f"atom  {x+dx: .8f}  {y+dy: .8f}  {z+dz: .8f}  {el}\n"
        )

print("✔ geometry.in generado y centrado correctamente")
print(f"Desplazamiento aplicado:")
print(f"dx = {dx:.6f} Å")
print(f"dy = {dy:.6f} Å")
print(f"dz = {dz:.6f} Å")