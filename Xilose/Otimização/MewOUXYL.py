import cobra
import mewpy
import time
from mewpy.simulation import SimulationMethod
from mewpy.problems import RKOProblem, ROUProblem, GKOProblem, GOUProblem
from mewpy.optimization.evaluation import TargetFlux
from mewpy.optimization import EA
from cobra.io import load_json_model
from mewpy.util.constants import EAConstants
from mewpy.optimization.evaluation import BPCY, WYIELD

EAConstants.NUM_CPUS = 8
modeloPKDupla = load_json_model("xylisopk2.json")
O2 = "R_O2xtI"
Xyl = "R_XYLxtI"
Biomassa = "R_VGRO"
modeloPKDupla.objective = Biomassa
fobj = 'R_3HPxtO'

condicoes = {Xyl: (-10.0, -9.99), O2: (-1000.0, 1000.0)}

evaluation_1 = BPCY(Biomassa,fobj,uptake=Xyl)
evaluation_2 = WYIELD(Biomassa,fobj,min_biomass_per=0.2)
alvo = TargetFlux(fobj, biomass=Biomassa, min_biomass_value=0.2)
problemaOU= ROUProblem(modeloPKDupla, fevaluation=[evaluation_1, evaluation_2], envcond=condicoes)

start_time = time.time()
ea = EA(problemaOU, max_generations=10000, visualizer=True, algorithm='SPEA2')
#print(type(ea))
final_pop=ea.run()
print(final_pop)
print(ea.dataframe())
ea.plot()
end_time = time.time()
execution_time = start_time - end_time
print("Tempo(s):",execution_time)

ROU = open('ROU_Xyl.txt', 'w')
for i in final_pop:
    ROU.write(str(i) + '\n')

ROU.close()