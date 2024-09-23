from ortools.sat.python import cp_model

# Instantiate model and solver
model = cp_model.CpModel()
solver = cp_model.CpSolver()

## colors: 0: Red, 1: Blue 2: Green
colors = {0 : 'Red',1:'Blue',2:'Green'}

SF = model.NewIntVar(0,2,'SF')
Alameda = model.NewIntVar(0,2,'Alameda')
Marin = model.NewIntVar(0,2,'Marin')
SanMateo = model.NewIntVar(0,2,'San Mateo')
SantaClara = model.NewIntVar(0,2,'Santa Clara')
ContraCosta = model.NewIntVar(0,2,'Contra Costa')
Solano = model.NewIntVar(0,2,'Solano')
Napa = model.NewIntVar(0,2,'Napa')
Sonoma = model.NewIntVar(0,2,'Sonoma')

## add edges
model.Add(SF != Alameda)
model.Add(SF != Marin)
model.Add(SF != SanMateo)
model.Add(ContraCosta != Alameda)
model.Add(Alameda != SanMateo)
model.Add(Alameda != SantaClara)
model.Add(SantaClara != SanMateo)
model.Add(Marin != Sonoma)
model.Add(Sonoma != Napa)
model.Add(Napa != Solano)
model.Add(Solano != ContraCosta)
model.Add(ContraCosta != Marin)

status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("SF: %s" % colors[solver.Value(SF)])
    print("Alameda: %s" % colors[solver.Value(Alameda)])
    print("Marin: %s" % colors[solver.Value(Marin)])
    print("Contra Costa: %s" % colors[solver.Value(ContraCosta)])
    print("Solano: %s" % colors[solver.Value(Solano)])
    print("Sonoma: %s" % colors[solver.Value(Sonoma)])
    print("Santa Clara: %s" % colors[solver.Value(SantaClara)])
    print("San Mateo: %s" % colors[solver.Value(SanMateo)])
    print("Napa: %s\n" % colors[solver.Value(Napa)])

# frequencies: 0: f1, 1: f2, 2: f3
frequencies = {0: 'f1', 1: 'f2', 2: 'f3'}

# Define variables for each antenna
A1 = model.NewIntVar(0, 2, 'A1')  # Antenna 1
A2 = model.NewIntVar(0, 2, 'A2')  # Antenna 2
A3 = model.NewIntVar(0, 2, 'A3')  # Antenna 3
A4 = model.NewIntVar(0, 2, 'A4')  # Antenna 4
A5 = model.NewIntVar(0, 2, 'A5')  # Antenna 5
A6 = model.NewIntVar(0, 2, 'A6')  # Antenna 6
A7 = model.NewIntVar(0, 2, 'A7')  # Antenna 7
A8 = model.NewIntVar(0, 2, 'A8')  # Antenna 8
A9 = model.NewIntVar(0, 2, 'A9')  # Antenna 9

# Add adjacency constraints (no two adjacent antennae can have the same frequency)
model.Add(A1 != A2)
model.Add(A1 != A3)
model.Add(A1 != A4)

model.Add(A2 != A1)
model.Add(A2 != A3)
model.Add(A2 != A5)
model.Add(A2 != A6)

model.Add(A3 != A1)
model.Add(A3 != A2)
model.Add(A3 != A6)
model.Add(A3 != A9)

model.Add(A4 != A1)
model.Add(A4 != A5)

model.Add(A5 != A2)
model.Add(A5 != A4)

model.Add(A6 != A2)
model.Add(A6 != A3)
model.Add(A6 != A7)
model.Add(A6 != A8)

model.Add(A7 != A6)
model.Add(A7 != A8)

model.Add(A8 != A6)
model.Add(A8 != A7)
model.Add(A8 != A9)

model.Add(A9 != A3)
model.Add(A9 != A8)

# Solve the model
status = solver.Solve(model)

# Print the results
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"Antenna 1: {frequencies[solver.Value(A1)]}")
    print(f"Antenna 2: {frequencies[solver.Value(A2)]}")
    print(f"Antenna 3: {frequencies[solver.Value(A3)]}")
    print(f"Antenna 4: {frequencies[solver.Value(A4)]}")
    print(f"Antenna 5: {frequencies[solver.Value(A5)]}")
    print(f"Antenna 6: {frequencies[solver.Value(A6)]}")
    print(f"Antenna 7: {frequencies[solver.Value(A7)]}")
    print(f"Antenna 8: {frequencies[solver.Value(A8)]}")
    print(f"Antenna 9: {frequencies[solver.Value(A9)]}")
else:
    print("No solution found.")
