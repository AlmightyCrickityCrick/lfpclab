#File contaning errors

#General error class. Details and formatting rules
class Error:
    def __init__(self,  error_name,pos_start, pos_end, details):
        self.error_name = error_name
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.details = details
    def as_string(self):
        result = f'{self.error_name}:{self.details} \n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'

        return result

#Specific error for introducing illegal character in a context
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__('Illegal Character',pos_start, pos_end, details)