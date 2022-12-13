obj_func_type = input("Enter the obj func(Max or Min):\n")
deci_vars_nb = int(input("Enter the Decisional variables number:\n"))
const_nb = int(input("Enter the constraints number:\n"))

def prepare_to_simplex(deci_vars_nb, const_nb):
    c = 0
    obj_func_coefs = [] #the items that will be appended to this list will be the values in the z-row
    constr_types = {} #constraint type: >= or <=
    coefs_dict = {}
    RHSides = {}
    #c0 is not constraint 0 its obj func
    #const_nb is slack/surplus vars nb
    #we need a loop for the rows of tha simplex table and another inside it for the coefs in each row
    while c < deci_vars_nb:
        coefs_list = [] #temperor list to store the coefs of one constrain all in one list
        c1 = 0 #count1
        while c1 < deci_vars_nb + const_nb:
            c1 += 1
            if c == 0: #=> obj func; this is onl;y for the prompt in input
                coef = int(input(f"Enter the coefficient{c1} of the objective function:\n"))
            else:
                coef = int(input(f"Enter the coefficient{c1} of the constraint{c}:\n"))
            coefs_list.append(coef)
        coefs_dict[f"c{c}"] = coefs_list
        #now we will take the one rhs for each constraint
        if c == 0: #=> obj func; this is onl;y for the prompt in input
            rhs = int(input("Enter the rhs of the objective func:\n"))
        else:
            rhs = int(input(f"Enter the RHS for the constraint{c}:\n"))
        RHSides[f"c{c}"] = rhs
        c += 1
    return coefs_dict, RHSides        
        
def simplex(obj_func_type, coefs_dict, RHSides):
    constr_ratios = {}
    pivot_column_index = coefs_dict["c0"].index(min(coefs_dict["c0"]))
    c = 0
    while c < (len(coefs_dict) - 1): #-1 to execlude z; because we need the contraint nb
        c += 1 #by putting c += 1 we except the ratio of obj func what is not needed
        ratio = RHSides[f"c{c}"] / coefs_dict[f"c{c}"][pivot_column_index]
        constr_ratios[f"c{c}"] = ratio
    min_ratio_row = min(constr_ratios)
    pivot_row = min_ratio_row
    pivot_element = coefs_dict[pivot_row][pivot_column_index]
    entering_var = f"x{pivot_column_index+1}"
    c = 0
    while c < len(coefs_dict["c0"]): #len of coefs_dict[c0] is the nb of columns(deci vars & slack/surp vars) => nb of columns execluding rhs
        coefs_dict[pivot_row][c] = coefs_dict[pivot_row][c]/pivot_element
    RHSides[pivot_row] = RHSides[pivot_row] / pivot_element
    #now we getted the new pivot row values 
    c = 0
    for i in coefs_dict:
        if i == coefs_dict[pivot_row]:
            continue #precalculated
        else:
            for a in coefs_dict[f"c{c}"]:
                a -= coefs_dict[i][pivot_column_index]*coefs_dict[pivot_row][coefs_dict[i].index(a)]
            RHSides[f"c{c}"] = RHSides[f"c{c}"] - coefs_dict[i][pivot_column_index]*RHSides[pivot_row]
            c += 1
    #now we updated all coefs to their new values
    RHSides_list = list(RHSides.values())
    if all(RHSides_list) > 0:
        print("Optimal")
        optimal_values = {}
        if obj_func_type == "Max":
            optimal_values["z"] = max(RHSides.values())
        elif obj_func_type == "Min":
            optimal_values["z"] = min(RHSides.values())
        c = 1
        for i in coefs_dict:
            if c == pivot_column_index+1:
                optimal_values[entering_var] = RHSides[pivot_row]
            else:
                optimal_values[f"S{c}"] = RHSides[f"c{c}"]
        return optimal_values
    else:
        simplex(obj_func_type, coefs_dict, RHSides)

prepare_to_simplex(deci_vars_nb, const_nb)
simplex(obj_func_type, coefs_dict, RHSides)