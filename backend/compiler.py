import multiprocessing as thread

path = 'test.txt'

class Code:
    
    def __init__(self, data):
        #------------------------------------#
        # exec function use only in class
        v = {}
        self.data = data
        exec(open(path).read(), None, v)
        # print(v)
        for name, value in v.items():
            setattr(self, name, value)
        #------------------------------------#
        # print(locals())
        self.timeLimit = 1
        # self.result = list()
        self.name = data['func']
        self.input, self.expected = self.get_testcase()
        # print(self.input[0])
        # print(self.expected[0])
    
    # def update_result(self, val):
    #     self.result.append(val)

    def get_testcase(self): # get testcase
        testcase = self.data['testcase']
        INPUT, OUTPUT = [], []
        for v in testcase:
            INPUT.append(v['input'])
            OUTPUT.append(v['output'])
        # print('input: ', INPUT)
        # print('output: ', OUTPUT)
        return INPUT, OUTPUT
        # print(testcase)
    
    def run_helper(self, INPUT, EXPECTED, case, ans):
        func = 'self.' + self.name
        # print(INPUT)
        # print(INPUT)
        print(EXPECTED)
        b = '(' + ', '.join(str(val) for key, val in INPUT.items()) + ')'
        # print(func+b)
        try:
            OUT = eval(func+b)
            print(OUT, EXPECTED)
            if OUT == EXPECTED:
                print('case%d: Passed' % (case+1))
                # self.update_result(1) # 1 for pass
                ans.put(1)
                # return 1
            else:
                print('case%d: Wrong Answer' % (case+1))
                # self.update_result(0) # 0 for not pass
                ans.put(0)
                # return 0
        except Exception as e:
            print('case%d: %s' % (case+1, e)) 
            # self.update_result(-2) # -2 for error in code
            ans.put(-2)
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

        ans = thread.Queue()
        job = []
        for case in range(len(self.input)):
            # sent[case] = False
            T = thread.Process(target = self.run_helper, args = (self.input[case], *self.expected[case], case, ans))
            job.append(T)
            T.start()
            T.join(self.timeLimit)
            if T.is_alive():
                print('case%d: Timeout' % (case+1))
                # self.update_result(-1) # -1 for timeout
                ans.put(-1)
                T.terminate()
                T.join()
        return [ans.get() for j in job]

    def get_result(self):
        return self.result

    def test(self):
        print(self.add(1, 2, 3))
        

# A = Code('add')
# A.run()


