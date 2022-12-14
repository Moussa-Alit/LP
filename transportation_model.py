# function to return key for any value
def get_key(val, the_dict):
    for key, value in the_dict.items():
        if val == value:
            return key 
    return "key doesn't exist"

class TransportationModel():
    sources_supps = {'S1':20, 'S2':25, 'S3':30} #fill and balance method will fill this
    dests_demands = {'D1':33, 'D2':22, 'D3':11, 'D4':9} #fill and balance method will fill this
    basic_cells = {'X11':20, 'X21':13, 'X22':12, 'X32':10, 'X33':11, 'X34':9} #non eliminated cells #we need a func that to check if we need a 0 value cell to be not eliminated
    basic_cells_costs = {}
    costs = {'X11':4, 'X12':6, 'X13':8, 'X14':20, 'X21':10, 'X22':11, 'X23':7, 'X24':7, 'X31':3, 'X32':4, 'X33':15, 'X34':1} #Will fill into this dict all the costsfor all cells
    Us = {'U1':0, 'U2':6, 'U3':-1} #fill Us values
    Vs = {'V1':4, 'V2':5, 'V3':16, 'V4':2} #fill Vs values
    reduced_costs = {'X12':-1, 'X13':8, 'X14':-18, 'X23':15, 'X24':1, 'X31':0}
    teta_loop_basic_cells = {} #should be global 7atta ma tsaffir bl recrusion
    c = 1
    c1 = 0

    """def __init__(self, sources_nb, dests_nb):
        self.sources_nb = sources_nb
        self.dests_nb = dests_nb"""

    def calc_cost(self, costPerunitPerunit, unitsamount):
        costPerunit = costPerunitPerunit * unitsamount

    def fill_and_balance(self, sources_nb, dests_nb):
        for i in range(sources_nb): #i starts from 0
            self.sources_supps[f"S{i+1}"] = int(input(f"Enter the quatity supplied by S{i+1}: "))
        for i in range(dests_nb):
            self.dests_demands[f"D{i+1}"] = int(input(f"Enter the quantity demanded by D{i+1}: "))
        T_supp = sum(self.sources_supps.values())
        T_demand = sum(self.dests_demands.values())
        diff = T_supp - T_demand
        if diff > 0: #=> unbalanced add dummy destination
            self.dests_demands[f"D{dests_nb + 1}"] = diff
        elif diff < 0: #=> dummy source
            self.sources_supps[f"S{sources_nb + 1}"] = - diff
        print(self.sources_supps, self.dests_demands)
        return self.sources_supps, self.dests_demands

    def fill_cells(self):   #somthing is going falsy here 
        self.c, self.c1 = 1, 0 #revauling c & c1 lal e7tiyat    
        for dest in self.dests_demands:
            if self.sources_supps[f"S{self.c}"] == 0:
                self.c += 1 #if we assigned c to 0 and incremented it every iteration it will increment even if the demand of a destination turned to 0 and the supply is still>0
            self.c1 += 1
            minimum = min(self.sources_supps[f"S{self.c}"], self.dests_demands[f"D{self.c1}"])
            print(f"Minimum of S{self.c} & D{self.c1}", min(self.sources_supps[f"S{self.c}"], self.dests_demands[f"D{self.c1}"]))
            self.basic_cells[f"X{self.c}{self.c1}"] = minimum#min(self.sources_supps[f"S{self.c}"], self.dests_demands[f"D{self.c1}"])
            self.dests_demands[f"D{self.c1}"] -= minimum#min(self.sources_supps[f"S{self.c}"], self.dests_demands[f"D{self.c1}"])
            print("Dest rest from fill_cells without continue_filling_demands!", self.dests_demands[f"D{self.c1}"])
            self.sources_supps[f"S{self.c}"] -= minimum#min(self.sources_supps[f"S{self.c}"], self.dests_demands[f"D{self.c1}"])
            print(f"""Source {self.c} rest from fill_cells without continue_filling_demands!""", self.sources_supps[f"S{self.c}"])
            if self.dests_demands[f"D{self.c1}"] > 0:
                print("Going to continue_fillig_demands")
                self.continue_filling_demand(self.c, self.c1)#hayk bnkoun ksebna sha8ltayn bfard darbe tracked value of c & continued filling demand
        #self.check_4_not_eliminated_but_zero()
        print(self.basic_cells)
        return self.basic_cells

    def continue_filling_demand(self, row_index, col_index): #indexes here start from 1
        print("Continuing filling demand")
        self.c = row_index
        self.c1 = col_index
        self.c += 1 #what if source != 0; it shoulb be zero because if demand still > 0 => supp = 0
        minimum = min(self.sources_supps[f"S{self.c}"], self.dests_demands[f"D{self.c1}"]) #if substracting min(dem, supp) directly the last min(dem, supp) in front of self.sources_supps will be different and false
        self.basic_cells[f"X{self.c}{self.c1}"] = minimum
        self.dests_demands[f"D{self.c1}"] -= minimum
        self.sources_supps[f"S{self.c}"] -= minimum
        print(f"""In continue filling func: source rest{self.sources_supps[f"S{self.c}"]}; dest rest{self.dests_demands[f"D{self.c1}"]}""")
        if self.dests_demands[f"D{self.c1}"] > 0:
            self.continue_filling_demand(self.c, self.c1)

    def check_4_not_eliminated_but_zero(self):
        #this will occur when dest_demands/dest_rest == sources_supp/sources_rest so after substracting the source will be 0 and the dest
        #I can check using this method, but I prefer to use another to keep fill_cells simple
        #indexes method
        temper_dict = {self.basic_cells.values()[0]}
        for cell in self.basic_cells:
            c = int(cell[1])
            c1 = int(cell[2])
            if (c - int(temper_dict[-1][1])) != 0 and (c1 - int(temper_dict[-1][2])) != 0: #=> diagonal path 
                self.basic_cells[f"X{c-1}{c1}"]
            temper_dict[cell] = self.basic_cells[cell]
        #what I did , I substracted indexes from the last temper dict item wich is the previous basic cell and the act cell, to be a horizantal pass or vertical pass a substraction should be 0
        #so if both are not 0 => diagonal pass; => return one source backward at the same dest and add a basic_cell 

    def fill_basic_cells_costs(self, costPerunitPerunit=False): #not needed
        for cell in self.basic_cells:
            if costPerunitPerunit:
                costPerunitPerunit = int(input("Enter cost per unit per unit: "))
                unitamount = int(input("Enter unit amount: "))
                costPerunit = costPerunitPerunit * unitamount
            else:
                costPerunit = int(input("Enter cost per unit: "))
            self.basic_cells_costs[cell] = costPerunit

    def fill_costs(self, costPerunitPerunit=False): #costPerunitPerunit is True or False
        for s_i in range(len(self.sources_supps)): #Using range is, better for indexing
           for d_i in range(len(self.dests_demands)):
                cell = f"X{s_i+1}{d_i+1}"
                if costPerunitPerunit:
                    costPerunitPerunit = int(input(f"Enter cost per unit per unit for {cell}: "))
                    unitamount = int(input(f"Enter unit amount {cell}: "))
                    costPerunit = costPerunitPerunit * unitamount
                else:
                    costPerunit = int(input(f"Enter cost per unit {cell}: "))    
                self.costs[cell] = costPerunit
        print(self.costs)
        return self.costs
    
    def fill_Us_Vs(self):
        #Us and Vs are parameter calculated to use it in finding the reduced costs for the eliminated cells to see if we can optimize the transportation cost or not.
        #Rule: Ui + Vj = cij
        self.Us["U1"] = 0
        for cell in self.basic_cells:
            if f"U{cell[1]}" in self.Us: #checking the presence of Ui #cell[1] is the second character in the key's string
                self.Vs[f"V{cell[2]}"] = self.costs[cell] - self.Us[f"U{cell[1]}"]
            elif f"V{cell[2]}" in self.Vs:
                self.Us[f"U{cell[1]}"] = self.costs[cell] - self.Vs[f"V{cell[2]}"]
            else:
                print("Somthing went wrong!")
        print(self.Us, self.Vs)
        return self.Us, self.Vs

    def calc_reduced_costs(self):
        #reduced cost = Ui + Vj - cij
        #if all reduced costs <= 0    => optimum trasportation cost
        #loop over costs, check if eliminated cell then calculate
        for cost in self.costs: #cost is a cell index : Xij, So cost[1] => i, cost[2] => j
            print(cost)
            if cost in self.basic_cells:
                continue #we need only eliminated cells
            else:
                self.reduced_costs[cost] = self.Us[f"U{cost[1]}"] + self.Vs[f"V{cost[2]}"] - self.costs[cost] #hayk bn7otton bdict la7al
        print(self.reduced_costs)
        return self.reduced_costs

    def check_optimality(self):
        if all(self.reduced_costs) <= 0:
            return True
        else:
            return False

    def nearest_in_row(self, cell_to_workwith):
        distances = {}
        for cell in self.basic_cells:
            if cell != cell_to_workwith and cell[1] == cell_to_workwith[1]: 
                distance = int(cell[2]) - int(cell_to_workwith[2]) #distance is how many dest cell is away from entering cell
                print("Distance: ", distance)
                if distance < 0:
                    distance = -distance #we need absolute value of distance
                distances[cell] = distance
        nearest_cell = get_key(min(distances.values()), distances)
        print("Nearest cell in row:", nearest_cell)
        print("Nearest cell value: ", self.basic_cells[nearest_cell])
        return nearest_cell

    def nearest_in_col(self, cell_to_workwith):
        distances = {}
        for cell in self.basic_cells:
            if cell != cell_to_workwith and cell[2] == cell_to_workwith[2]: 
                distance = int(cell[1]) - int(cell_to_workwith[1]) #distance is how many dest cell is away from entering cell
                print("Distance: ", distance)
                if distance < 0:
                    distance = -distance #we need absolute value of distance
                distances[cell] = distance
        nearest_cell = get_key(min(distances.values()), distances)
        print("Nearest cell in col:", nearest_cell)
        print("Nearest cell value: ", self.basic_cells[nearest_cell])
        return nearest_cell

    def constructing_teta_loop(self, working_with_cell, entering_var):
        nearest_cell = self.nearest_in_row(working_with_cell)
        if nearest_cell != entering_var:
            self.teta_loop_basic_cells[nearest_cell] = self.basic_cells[nearest_cell]
            nearest_cell = self.nearest_in_col(nearest_cell)
            if nearest_cell != entering_var:
                self.teta_loop_basic_cells[nearest_cell] = self.basic_cells[nearest_cell]
                self.constructing_teta_loop(nearest_cell, entering_var)
            return self.teta_loop_basic_cells
        return "Should always start with entering var as working with cell"

    def enter_leave_vars(self):
        entering_var = get_key(max(self.reduced_costs.values()), self.reduced_costs)
        print("Entering var: ", entering_var)
        c = 0
        #we will add entering var to basic cells first, why first because we need from the enetring var to be the nearest cell in a certain stage of teta loop
        #So if its not a basic cell how can it be the nearest cell, so the loop stop
        self.teta_loop_basic_cells[entering_var] = 0
        self.basic_cells[entering_var] = 0
        #First looping over vbasic cells and filtering cells in the same row of entering_var to find the nearest one
        teta_loop_basic_cells = self.constructing_teta_loop(entering_var, entering_var)
        print(f"Teta loop basic cells: {teta_loop_basic_cells}")
        teta_value = min(teta_loop_basic_cells.values())
        c = 0
        for cell in teta_loop_basic_cells:
            print(cell)
            c += 1
            if c % 2 != 0:
                self.basic_cells[cell] += teta_value
            else:
                self.basic_cells[cell] -= teta_value
        leaving_var = get_key(teta_value, teta_loop_basic_cells)
        self.basic_cells.pop(leaving_var) #removing leaving variable
        print("New basic cells after add/sub teta:  ", self.basic_cells)
        return self.basic_cells        
   
    def do_all(self, sources_nb, dests_nb):
        self.fill_and_balance(sources_nb, dests_nb)
        self.fill_cells()
        self.fill_costs()
        self.fill_Us_Vs()
        self.calc_reduced_costs()
        check = self.check_optimality()
        if check: #if True
            return "Optimal"
        self.entering_leaving_vars()

TransportationModel().enter_leave_vars()

#returned infinite recrusion
#max reduced cost is always the same