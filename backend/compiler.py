import os
from pathos.helpers import mp as thread
# import multiprocessing as thread

class Code:
    
    def __init__(self, rawdata):
        self.timeLimit = 1
        # self.result = list()
        # print(rawdata)
        self.raw = rawdata
        self.data = self.raw['taskData']
        self.name = self.data['functionName']
        self.input, self.expected = self.get_testcase()
        self.Error = False
        self.ExecuteProg()
        # print(self.input[0])
        # print(self.expected[0])
    
    # def update_result(self, val):
    #     self.result.append(val)

    def ExecuteProg(self):
        if self.raw['Type'] == 'py': # create function from python file
            v = {}
            self.Error = False
            try:
                exec(self.raw['userCode'], None, v)
                for name, value in v.items():
                    setattr(self, name, value)
            except Exception as e:
                self.Error = True
                self.ee = e
            # print(v)

        elif self.raw['Type'] == 'c/c++': # create function from c++ file
            with open('test.cpp', 'w') as f:
                f.write('#ifdef __cplusplus\nextern \"C\"\n#endif\n') # important for c
                f.write(self.raw['userCode'])
            try:
                os.system("g++ -Wall test.cpp -shared -o test.dll") # compile
            except Exception as e:
                self.Error = True
                self.ee = e
            else: # if done 
                import ctypes
                self.funOfC = getattr(ctypes.cdll.LoadLibrary('./test.dll'), self.name) # get function
                # print('************')
                # print(getattr(self.funOfC, 'MMM')(1, 2))
                # print('************')

    def get_testcase(self): # get testcase
        testcase = self.data['testcase']
        INPUT, OUTPUT = [], []
        for v in testcase:
            INPUT.append(v['input'])
            OUTPUT.append(v['output'])
        # print('input: ', INPUT)
        # print('output: ', OUTPUT)
        return INPUT, OUTPUT
    
    def run_helper(self, INPUT, EXPECTED, case, ans):
        func = 'self.' + (self.name if self.raw['Type'] == 'py' else 'funOfC')
        # for v in INPUT:
        # print(eval('self.funOfC(1, 2)'))
        #     print(*v.values())
        b = '(' + ', '.join('\'' + str(*list(*v.values())) + '\'' if isinstance(*list(*v.values()), str) else str(*list(*v.values())) for v in INPUT) + ')'
        print(func+b)
        try:
            OUT = eval(func+b) # get output
            print(OUT, '|', EXPECTED)
            if str(OUT) == str(EXPECTED): # 1 for pass
                print('case%d: Passed' % (case+1))
                # self.update_result(1) 
                ans.put([case, 1, OUT])
                # return 1
            else: # 0 for not pass
                print('case%d: Wrong Answer' % (case+1))
                # self.update_result(0) 
                ans.put([case, 0, OUT])
                # return 0
        except Exception as e: # -2 for error in code
            print('case%d: %s' % (case+1, e))
            # self.update_result(-2) 
            ans.put([case, -2, str(e)])
            # return -2

    def run(self):
        '''
            ****************
            -2: Error
            -1: Timeout
            0 : Wrong Answer
            1 : Passed
            ****************
        '''
        if self.Error: # Compile error or Syntax Error
            return [[-1, -2, str(self.ee)]]
        ans = thread.Queue()
        job = []
        for case in range(len(self.input)):
            # sent[case] = False
            # print(self.input[case])
            # print(self.expected[case])
            T = thread.Process(target = self.run_helper, args = (self.input[case], self.expected[case], case, ans))
            job.append(T)
            T.start()
            T.join(self.timeLimit)
            if T.is_alive():
                print('case%d: Timeout' % (case+1)) # -1 for timeout
                # self.update_result(-1) 
                ans.put([case, -1])
                T.terminate()
                T.join()
        return [ans.get() for j in job]

    def get_result(self):
        return self.result

    def test(self):
        print(self.add(1, 2, 3))
        

# A = Code('add')
# A.run()




