from django.test import TestCase
from django.utils import unittest
import logging
from standard import *
from markscheme import *
from answer import *
import os
import pprint

#@unittest.skip("Too much time")
class AlgorithmTest(TestCase):

    def setUp(self):
        self.logger = logging.getLogger(__name__)

    @unittest.skip("Too much time")
    def test_standard(self):
        self.logger.info("Test Standard Answer Analysis")
        testStandardAnswerFile="ans_Q1.txt"
        filePath=os.path.join("algo/testdata/raw/Q1",testStandardAnswerFile)
        self.logger.info("filepath:%s" % filePath)
        if not os.path.isfile(filePath):
            self.logger.error("Test file doesn't exist:%s" % testStandardAnswerFile)
            assert False
        fh=file(filePath,"r")
        filetext=fh.read()
        fh.close()
        sinst=Standard()
        pointlist,textfdist,slist = sinst.Analysis(filetext)
        #for word,freq in textfdist.items():
        #    print "%s:%d" % (word,freq)
        pprint.pprint(slist)
        self.logger.info("Test Standard Answer Analysis finished")

    #@unittest.skip("Too much time")
    def test_markscheme(self):
        self.logger.info("Test Marking Scheme Analysis/Rule Generation")

        mocktemplates=""
        mockplist=['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7','P3.4']
        #mockplist=['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7','P8','P9','P10','P11']
        #Negative
        mocktemplates+='all except P3 and P22,8,'
        mocktemplates+='only P1 or Ps,1,'
        mocktemplates+='only some  from all,8,'
        mocktemplates+='only 2 from all,8,'
        #Positive
        mocktemplates+='all less two combination of p1 and p2 and p3 and p4 and p5 and p6 and p7 and p8 and p9 and p10 and 11'
        mocktemplates+='all less P5,8,'
        mocktemplates+='all less P3 and P22 or P4 and P5 or P6 or P7,8,'
        mocktemplates+='all,10,'
        mocktemplates+='only P1 or P6 and P7 and P4 or P88 or P89 or P90 and P2,8,'
        mocktemplates+='only P1 or P3.4,8,'
        mocktemplates+='any 2 combinations of P1;P3;P5;P99;P7,8,'
        mocktemplates+='any 2 combinations of P1;P3;P5;P99;P7 and any 1 combinations of P4;P6 and any 3 combinations of P2;P3.4,8,'
        mocktemplates+='less 2 combinations of P1;P3;P5;P99;P7 and less 1 combinations of P4;P6 and less 3 combinations of P2;P3.4,8,'
        mocktemplates+='all less 2 combinations of P1;P3;P5;P9,1,'
        mocktemplates+='all less 0 combinations of P1;P3;P5;P9,1,'
        mocktemplates+='all less -1 combinations of P1;P3;P5;P9,1,'

        #be careful, last case has no trailing comma
        mocktemplates+='all less 4 combinations of P1;P3;P5,1'
        ms=MarkScheme(mockplist)
        rulelist=ms.GetRules(mocktemplates)
        pprint.pprint(rulelist)
        self.logger.info("Test Marking Scheme Analysis/Rule Generation Finished")

    @unittest.skip("Too much time")
    def test_answer(self):
        self.logger.info("Test Student Answer Analysis")

        testStandardAnswerFile="ans_Q1.txt"
        stdFilePath=os.path.join("algo/testdata/raw/Q1",testStandardAnswerFile)
        self.logger.info("stdanswer filepath:%s" % stdFilePath)
        if not os.path.isfile(stdFilePath):
            self.logger.error("Standard Test file doesn't exist:%s" % testStandardAnswerFile)
            assert False
        fh=file(stdFilePath,"r")
        stdtext=fh.read()
        fh.close()

        sinst=Standard()
        pointlist,textfdist,slist = sinst.Analysis(stdtext)
        std_pointlist_no=[point['Point_No'] for point in pointlist]
        self.logger.info("Points:%s" % std_pointlist_no)

        testAnswerFile="ans_Q1.txt"
        ansFilePath=os.path.join("algo/testdata/raw/Q1",testAnswerFile)
        self.logger.info("answer filepath:%s" % ansFilePath)
        if not os.path.isfile(ansFilePath):
            self.logger.error("Answer file doesn't exist:%s" % testAnswerFile)
            assert False
        fh=file(ansFilePath,"r")
        anstext=fh.read()
        fh.close()

        mockrulelist=[
                {'Mark':10,'Point':['P1.1','P1.2','P1.3','P2','P3','P4','P5']},
                {'Mark':7,'Point':['P1.1','P2','P3','P4','P5']},
                {'Mark':6,'Point':['P1.1','P2','P3','P4']},
                {'Mark':5,'Point':['P1.1','P2','P3']},
                {'Mark':3,'Point':['P1.1','P2']},
                {'Mark':2,'Point':['P1.1']},
                ]
        pprint.pprint(mockrulelist)

        ans=Answer()
        mark,ommited = ans.Analysis(anstext,textfdist,slist,pointlist,mockrulelist)
        pprint.pprint(mark)
        pprint.pprint(ommited)

        self.logger.info("Test Student Answer Analysis Finished")

