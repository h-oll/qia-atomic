class Mixin:

    def util_qrng(self) :

        """
        return random 0 or 1 via hadarmard gate
        param:
            location_strings: string, node where the q.h is happening, 'Alice' by default
        
        """
        q=self.PREP()
        self.H(q)
        number = self.MEAS()
        print('Outcome of the measure:', number)
        return number

        

    
