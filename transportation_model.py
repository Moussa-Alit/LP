# function to return key for any value
def get_key(val, the_dict):
    for key, value in the_dict.items():
        if val == value:
            return key 
    return "key doesn't exist"

class TransportationModel():
    sources_supps = {'S1':20, 'S2':25, 'S3':30} #fill and balance method will fill this
    dests_demands = {'D1':33, 'D2':22, 'D3':11, 'D4':9} #fill and balance method will fill this
    basic_cells = {}#{'X11':20, 'X21':13, 'X22':12, 'X32':10, 'X33':11, 'X34':9} #non eliminated cells #we need a func that to check if we need a 0 value cell to be not eliminated
    basic_cells_costs = {}
    costs = {'X11':4, 'X12':6, 'X13':8, 'X14':20, 'X21':10, 'X22':11, 'X23':7, 'X24':7, 'X31':3, 'X32':4, 'X33':13, 'X34':1} #Will fill into this dict all the costsfor all cells
    Us = {}#{'U1':0, 'U2':6, 'U3':-1} #fill Us values
    Vs = {}#{'V1':4, 'V2':5, 'V3':14, 'V4':2} #fill Vs values
    reduced_costs = {}#{'X12':-1, 'X13':8, 'X14':-18, 'X23':15, 'X24':1, 'X31':0}
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

    def fill_costs(self, costPerunitPerunit=False): #costPerunitPerunit is True or False
        for s_i in range(len(self.sources_supps)): #Using range is, better for indexing
           for d_i in range(len(self.dests_demands)):
                cell = f"X{s_i+1}{d_i+1}"
                if costPerunitPerunit:
                    costPerunitPerunit = float(input(f"Enter cost per unit per unit for {cell}: "))
                    unitamount = float(input(f"Enter unit amount {cell}: "))
                    costPerunit = costPerunitPerunit * unitamount
                else:
                    costPerunit = float(input(f"Enter cost per unit {cell}: "))    
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
            if cost in self.basic_cells:
                continue #we need only eliminated cells
            else:
                self.reduced_costs[cost] = self.Us[f"U{cost[1]}"] + self.Vs[f"V{cost[2]}"] - self.costs[cost] #hayk bn7otton bdict la7al
        print("Reduced costs: ", self.reduced_costs)
        return self.reduced_costs

    def optimized_cost(self):
        optimized_cost = 0
        for cost in self.costs: #cost is a cell
            if cost in self.basic_cells:
                optimized_cost += self.basic_cells[cost] * self.costs[cost]
            else:
                continue
        return optimized_cost

    def check_optimality(self):
        #if all(self.reduced_costs.values()) <= 0: #Surprized all() cant tets < 0 values!!!!! 
        for reduced_cost_v in self.reduced_costs.values():
            if reduced_cost_v > 0:
                return False
            else:
                continue
        optimized_cost = self.optimized_cost()
        print(optimized_cost)
        return True

    def nearest_in_row(self, working_with_cell):
        distances = {}
        for cell in self.basic_cells:
            if cell != working_with_cell and cell[1] == working_with_cell[1]: 
                distance = int(working_with_cell[2]) - int(cell[2])#distance is how many dest cell is away from entering cell
                print("Distance: ", distance)
                if distance < 0:
                    distance = -distance #we need absolute value of distance
                distances[cell] = distance
        if not distances:
            #self.teta_loop_basic_cells.pop(working_with_cell)
            #aslan ba3d ma fwwatta
            nearest_cell_in_col = self.nearest_in_col_if_no_nearest_in_row(working_with_cell)
            self.teta_loop_basic_cells[nearest_cell_in_col] = self.basic_cells[nearest_cell_in_col]
            return self.nearest_in_row(nearest_cell_in_col)
        nearest_cell = get_key(min(distances.values()), distances)
        #print("Nearest cell in row:", nearest_cell)
        #print("Nearest cell value: ", self.basic_cells[nearest_cell])
        print("Nearest cell returned by nearest_in_row: ", nearest_cell)
        return nearest_cell

    def nearest_in_col_if_no_nearest_in_row(self, working_with_cell):
        distances = {}
        for cell in self.basic_cells:
            if cell != working_with_cell and cell[2] == working_with_cell[2]: 
                distance = int(working_with_cell[1]) - int(cell[1]) #distance is how many dest cell is away from entering cell
                print("Distance: ", distance)
                if distance < 0:
                    continue #here we want to continue in the same direction
                distances[cell] = distance
        try:
            nearest_cell = get_key(min(distances.values()), distances)
        except ValueError():
            raise ValueError("No solution teta loop arrived to a cell that have no near cells in row and and when tried to find in column, didn't find an more advanced cell!")
        print("Nearest cell in row:", nearest_cell)
        #print("Nearest cell value: ", self.basic_cells[nearest_cell])
        return nearest_cell

    def nearest_in_col(self, working_with_cell):
        distances = {}
        for cell in self.basic_cells:
            if cell != working_with_cell and cell[2] == working_with_cell[2]: 
                distance = int(working_with_cell[1]) - int(cell[1]) #distance is how many dest cell is away from entering cell
                print("Distance: ", distance)
                if distance < 0:
                    distance = -distance #we need absolute value of distance
                distances[cell] = distance
        if not distances:
            nearest_cell_in_row = self.nearest_in_row_if_no_nearest_in_col(working_with_cell) #bas ra7 tkoun hiyye hiyye l entering var aw bl a7ra lli kmonna 3anda lamma sh8alna nearest in row awwal marra
            self.teta_loop_basic_cells[nearest_cell_in_row] = self.basic_cells[nearest_cell_in_row]
            return self.nearest_in_col(nearest_cell_in_row)
        else:
            nearest_cell = get_key(min(distances.values()), distances)
            print("Nearest cell returned by nearest_in_col: ", nearest_cell)
            return nearest_cell

    def nearest_in_row_if_no_nearest_in_col(self, working_with_cell):
        #first la ndman 2eenno l nearest cell in row ma tkoun l cell lli jina menna bnemna3 l distance tkoun negative
        #teta----cell_but_no_nearest_in_col----cell_but_no_nearest_in_col----nothing----nothing----cell_with_nearest_in_col
        distances = {}
        for cell in self.basic_cells:
            if cell != working_with_cell and cell[1] == working_with_cell[1]: 
                distance = int(working_with_cell[2]) - int(cell[2]) #distance is how many dest cell is away from entering cell
                print("Distance: ", distance)
                if distance < 0:
                    continue #here we want to continue in the same direction
                distances[cell] = distance
        nearest_cell = get_key(min(distances.values()), distances)
        print("Nearest cell in row:", nearest_cell)
        return str(nearest_cell)

    def constructing_teta_loop(self, working_with_cell, entering_var):
        #self.teta_loop_basic_cells = {} #if we are contructing teta loop for the second, third.. time we should restart from {}, but since contructing_teta_loop recrusion itself we should clearing it in another place
        #if there is a status where I should start with nearest col
        #I will test it see the resulting error, then using try nearest_in row w kol code, except l error try nearest_in_col w be2e l code
        nearest_cell = self.nearest_in_row(working_with_cell)
        if nearest_cell != entering_var:
            self.teta_loop_basic_cells[nearest_cell] = self.basic_cells[nearest_cell]
            nearest_cell = self.nearest_in_col(nearest_cell)#[1] + self.nearest_in_col(nearest_cell)[2]
            print(f"Nearest cell provided by nearest_in_col: {nearest_cell}")
            if nearest_cell != entering_var:
                self.teta_loop_basic_cells[nearest_cell] = self.basic_cells[nearest_cell]
                self.constructing_teta_loop(nearest_cell, entering_var)
            return self.teta_loop_basic_cells
        return "Should always start with entering var as working with cell"

    def find_teta_leaving_var(self):
        #In this func the cells where we will substract teta will be filtered
        #teta_value is where the min value
        #leaving var is where teta_value
        cells_where_minus_teta = {}
        c = 0
        for cell in self.teta_loop_basic_cells:
            c += 1 
            if c % 2 == 0:
                cells_where_minus_teta[cell] = self.teta_loop_basic_cells[cell]
        print(f"Cells where minus teta {cells_where_minus_teta}")
        teta_value = min(cells_where_minus_teta.values())
        print("Teta value; ", teta_value)
        leaving_var = get_key(teta_value, self.teta_loop_basic_cells)
        return teta_value, leaving_var

    def enter_leave_vars(self):
        entering_var = get_key(max(self.reduced_costs.values()), self.reduced_costs)
        print("Entering var: ", entering_var)
        c = 0
        #we will add entering var to basic cells first, why first because we need from the enetring var to be the nearest cell in a certain stage of teta loop
        #So if its not a basic cell how can it be the nearest cell, so the loop stop
        self.teta_loop_basic_cells = {} #should do this, because teta_loop_basic_cells can be full of data from a previous self.constructing_teta_loop()
        self.teta_loop_basic_cells[entering_var] = 0
        self.basic_cells[entering_var] = 0
        print(f"teta_loop_basic_cells when adding entering var {self.teta_loop_basic_cells}")
        #First looping over vbasic cells and filtering cells in the same row of entering_var to find the nearest one
        teta_loop_basic_cells = self.constructing_teta_loop(entering_var, entering_var)
        print(f"Teta loop basic cells: {teta_loop_basic_cells}")
        teta_value = self.find_teta_leaving_var()[0]
        c = 0
        for cell in teta_loop_basic_cells:
            #print(cell)
            c += 1
            if c % 2 != 0:
                self.basic_cells[cell] += teta_value
            else:
                self.basic_cells[cell] -= teta_value
        leaving_var = get_key(teta_value, self.teta_loop_basic_cells)
        print(f"Leaving var: {leaving_var}")
        self.basic_cells.pop(leaving_var) #removing leaving variable
        self.reduced_costs.pop(entering_var) #if not removing entering var from reduced costs the max reduced cost what telled us about optima;ity will still the same and we will never acheive optimality
        print("New basic cells after add/sub teta:  ", self.basic_cells)
        return self.basic_cells        

    def redo(self):
        self.enter_leave_vars()
        self.fill_Us_Vs()
        self.calc_reduced_costs()
        check = self.check_optimality()
        print("Check in redo ", check)
        if check:
            return "Optimal", self.basic_cells
        self.redo()
        

    def do_all(self, sources_nb, dests_nb):
        self.fill_and_balance(sources_nb, dests_nb)
        self.fill_cells()
        
        cost_type = int(input("Choose the cost type:\n { To choose Cost/unit Enter '0', To choose enter Cost/unit/unit '1' }\n"))
        try:
            cost_type = bool(cost_type)
        except:
            raise ValueError("Should enter 0 or 1")
        self.fill_costs(cost_type)
        self.fill_Us_Vs()
        self.calc_reduced_costs()
        check = self.check_optimality()
        print("Check in do_all: ", check)
        if check: #if True
            return "Optimal"
        self.redo()

#TransportationModel().enter_leave_vars()
TransportationModel().do_all(3, 4)
#returned infinite recrusion
#max reduced cost is always the same