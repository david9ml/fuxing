import re
import nltk
import math
from django.conf import settings
import logging


class Answer(object):

    def __init__(self,):
        self.logger = logging.getLogger(__name__)
        nltk.data.path = [settings.NLTKDATAPATH]

    def SentenceAnalysis(self, fulltext, textfdist):
        ans_sentencelist = []
        text = fulltext.replace('\n', ' ')
        #p = re.compile(r'.+\.')
        p = re.compile(r'([\w\"\'\<\(][\S ]+?[\.!?])[ \n\"]')
        keysen = p.findall(text)
        sen_no = 0
        for sen in keysen:
            sen_no += 1
            text = nltk.word_tokenize(sen)
            text_words = list(nltk.corpus.wordnet.morphy(word.lower()) for (word, tag) in nltk.pos_tag(text))
            ans_sentencelist.append({'StuS': sen,
                                    'StuWords': list(word for word in text_words if word),
                                    'No': sen_no})
        for sentence in ans_sentencelist:
            fdist = nltk.FreqDist(sentence['StuWords'])
            senvec = {}
            for word in sorted(textfdist):
                if fdist[word]:
                    wordfreq = sum(1 for senten in ans_sentencelist if word in senten['StuWords'])
                    senvec[word] = (1 + math.log(2.0 * fdist[word])) * math.log(2.0 * len(keysen) / wordfreq)
                else:
                    senvec[word] = 0
            sentence['StuSVec'] = senvec
        return ans_sentencelist

    def Mark(self, std_sentencelist, std_pointlist_no, ans_sentencelist):
        detailedmarklist = []
        marklist = []
        for point_no in std_pointlist_no:
            if 'P0.' in point_no:
                pass
            else:
                std_senlist = []
                stu_senlist = []
                keyword_num = 0
                keyword_sum = 0
                sen_match = 0
                len_match = 0
                for std_sen in std_sentencelist:
                    if std_sen['Point_No'] == point_no:
                        std_senlist.append(std_sen['No'])
                        keyword_sum += len(std_sen['KeyBVec'])
                        max_cos = 0
                        match_sen = None
                        for stu_sen in ans_sentencelist:
                            q, s, qs = 0, 0, 0
                            '''
                            stdlen = sum(1 for set in set(weight for weight in std_sen["KeySVec"].values()) if set > 0)
                            stdlen = 0
                            for (word, weight) in std_sen['KeySVec'].items():
                                if weight > 0:
                                    stdlen += 1
                            stulen = 0
                            for (word, weight) in stu_sen['StuSVec'].items():
                                if weight > 0:
                                    stulen += 1
                            if stdlen < stulen:
                                for word in std_sen['KeySVec']:
                                    if std_sen['KeySVec'][word] > 0:
                                        q += std_sen['KeySVec'][word] * std_sen['KeySVec'][word]
                                        s += stu_sen['StuSVec'][word] * stu_sen['StuSVec'][word]
                                        qs += std_sen['KeySVec'][word] * stu_sen['StuSVec'][word]
                            elif stdlen > stulen:
                                for word in std_sen['KeySVec']:
                                    if stu_sen['StuSVec'][word] > 0:
                                        q += std_sen['KeySVec'][word] * std_sen['KeySVec'][word]
                                        s += stu_sen['StuSVec'][word] * stu_sen['StuSVec'][word]
                                        qs += std_sen['KeySVec'][word] * stu_sen['StuSVec'][word]
                            else:
                                for word in std_sen['KeySVec']:
                                    q += std_sen['KeySVec'][word] * std_sen['KeySVec'][word]
                                    s += stu_sen['StuSVec'][word] * stu_sen['StuSVec'][word]
                                    qs += std_sen['KeySVec'][word] * stu_sen['StuSVec'][word]
                            '''
                            for word in std_sen['KeySVec']:
                                if std_sen['KeySVec'][word] > 0:
                                    q += std_sen['KeySVec'][word] * std_sen['KeySVec'][word]
                                    s += stu_sen['StuSVec'][word] * stu_sen['StuSVec'][word]
                                    qs += std_sen['KeySVec'][word] * stu_sen['StuSVec'][word]
                            if q == 0 or s == 0:
                                qs_cos = 0
                            else:
                                qs_cos = qs / (math.sqrt(q * s))
                            stu_words = [word for word in stu_sen['StuSVec'] if stu_sen['StuSVec'][word] > 0]
                            if qs_cos > max_cos and len(stu_words) > 0:
                                max_cos = qs_cos
                                match_sen = stu_sen['No']
                                match_text = stu_sen['StuS']
                                #match_stu = stu_sen
                        '''
                        # xiangguandu juzi
                        print "Point_No:", point_no
                        print 'stdsen:', std_sen['No'], '---', std_sen['KeyS']
                        print 'stusen:', match_sen, '---', match_text
                        print 'Max Relevance:', max_cos
                        print 'Relevant Keyword:', [word for word in match_stu['StuSVec'] if match_stu['StuSVec'][word] > 0]
                        '''

                        if max_cos > 0.35:
                            sen_match += max_cos
                            len_match += 1
                            if std_sen['KeyBVec']:
                                keyword_freq = sum(1 for keyword in std_sen['KeyBVec']
                                                   if keyword.lower() in match_text.lower())
                                keyword_num += keyword_freq
                                keyword_match = 1.0 * keyword_freq / len(std_sen['KeyBVec'])
                            else:
                                keyword_match = None
                            stu_senlist.append({'Stand': std_sen['No'],
                                                'Max_Match': std_sen.get('TotalS_No'),
                                                'Stu': match_sen, 'Mat_Deg': max_cos,
                                                'Keyword_Match': keyword_match})

                #print stu_senlist

                if std_senlist and len_match:
                    #keyword_rate = 1.0 * keyword_num / keyword_sum
                    sen_rate = 1.0 * sen_match / len(std_senlist)
                    # moderate
                    sen_rate_match = 1.0 * sen_match / len_match if (1.0 * len_match / len(std_senlist) > 0.3) and len(std_senlist) > 1 else 0
                    # loose
                    #sen_rate_match = 1.0 * sen_match / len_match if (1.0 * len_match / len(std_senlist) > 0.1) and len(std_senlist) > 1 else 0
                    # strict
                    #sen_rate_match = sen_rate
                    #print sen_rate_match
                else:
                    sen_rate = 0
                    sen_rate_match = 0

                detailedmarklist.append({'Point_No': point_no,
                                        'Stand_senList': std_senlist,
                                        'Stu_SenList': stu_senlist,
                                        'Keyword_Rate': '%d/%d' % (keyword_num, keyword_sum),
                                        'Sentence_Rate': sen_rate,
                                        'Sentence_Rate_Match': sen_rate_match})
                #self.marklist = marklist

                # algo2: get complete match of every sentence in stdsenlist
                if stu_senlist and stu_senlist[0]['Max_Match'] and len(stu_senlist) > len(stu_senlist[0]['Max_Match']) * 0.7:
                    marklist.append(point_no)
        if not marklist:
            marklist = list(point['Point_No'] for point in detailedmarklist
                            if point['Sentence_Rate'] > 0.3 or point['Sentence_Rate_Match'] > 0.4)
        return marklist

    def Comparison(self, marklist, rulelist):
        match = True
        for rule in rulelist:
            for point in rule['Point']:
                if point not in marklist:
                    match = False
            if match:
                return rule['Mark'], rule['Point']
            else:
                match = True
        return 0, None

    def Omitted(self, marklist, std_pointlist, rulelist):
        mark, rule = self.Comparison(marklist, rulelist)
        omitted = []
        for point in std_pointlist:
            if 'P0.' not in point['Point_No']:
                if point['Point_No'] in marklist:
                    omitted.append('C' + point['Point_No'][1:] + point['Point_Text'])
                else:
                    omitted.append('W' + point['Point_No'][1:] + point['Point_Text'])
        return mark, omitted

    def Analysis(self, fulltext, textfdist, std_sentencelist, std_pointlist, rulelist):
        if not fulltext or not textfdist or not std_sentencelist or not std_pointlist or not rulelist:
            return None, None, None
        ans_sentencelist = self.SentenceAnalysis(fulltext, textfdist)
        std_pointlist_no = list(point['Point_No'] for point in std_pointlist)
        marklist = self.Mark(std_sentencelist, std_pointlist_no, ans_sentencelist)
        mark, omitted = self.Omitted(marklist, std_pointlist, rulelist)
        return mark, marklist, omitted


class ImageAnswer(object):
    def __init__(self,):
        self.logger = logging.getLogger(__name__)

    def Comparison(self, marklist, rulelist):
        match = True
        for rule in rulelist:
            for point in rule['Point']:
                if point not in marklist:
                    match = False
            if match:
                return rule['Mark'], rule['Point']
            else:
                match = True
        return 0, None

    def Omitted(self, marklist, std_pointlist, rulelist):
        mark, rule = self.Comparison(marklist, rulelist)
        omitted = []
        for point in std_pointlist:
            if 'P0.' not in point['Point_No']:
                if point['Point_No'] in marklist:
                    omitted.append('C' + point['Point_No'][1:] + point['Point_Text'])
                else:
                    omitted.append('W' + point['Point_No'][1:] + point['Point_Text'])
        return mark, omitted

    def Analysis(self, imgpoints, std_pointlist, rulelist):
        if imgpoints:
            marklist = list(imagepoint['Point_No'] for imagepoint, stuansimage in imgpoints)
            mark, omitted = self.Omitted(marklist, std_pointlist, rulelist)
            return mark, marklist, omitted
