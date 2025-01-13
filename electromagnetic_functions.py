# Electromagnetic calculations: just for resonance frequency and beta for half cell and
# end group

class emfn():
    def __init__(self):
        self.description='electromagnetic_parameters'

    # resonance frequency
    def Resonance_frequency(self, path):
        sfo_file  = open(path+'\\elmg_file\\OUTFIS.TXT', 'r')
        cont = sfo_file.readlines()
        sfo_file.close()
        for k in range(len(cont)-1,0,-1):
            if str([x for x in cont[k].split(' ') if x][0]) == 'FREQ':
                F_resonance = float([x for x in cont[k].split(' ') if x][1])
                break
        print('F ', F_resonance)
        return F_resonance
    
    # beta calculations
    def def_beta_IC_EC(self, F_target, CELL):
        l = CELL[6]/1000
        lambda_2 = 299792458/(2*F_target*10**6)
        self.beta = round(2*l/(lambda_2),2)
        if self.beta > 1:
            self.beta = 1
        return self.beta
    
    # beta calculation for EG
    def def_beta_EG(self, F_target, CAV):     
        l = (CAV[0,6] + CAV[2,6])/1000
        lambda_2 = 299792458/(F_target*10**6)
        self.beta = round(2*l/(lambda_2),2)
        if self.beta > 1:
            self.beta = 1
            
        return self.beta