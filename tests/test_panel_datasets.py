import unittest
from evals import panel_datasets as data


class DatasetTests(unittest.TestCase):
    def test_logiqa_keeps_original_choices_and_answer_index(self):
        samples = data.logiqa([{'example_id':7,'text':'P','question':'Q','options':['甲','乙','丙','丁'],'answer':2}])
        self.assertEqual(samples[0]['target'], 'C')
        self.assertEqual(samples[0]['criteria'], {'A':'甲','B':'乙','C':'丙','D':'丁'})
        self.assertEqual(samples[0]['input'], {'passage':'P','question':'Q'})

    def test_ocnli_excludes_only_no_consensus_and_hides_annotator_labels(self):
        samples = data.ocnli([{'id':1,'sentence1':'前提','sentence2':'假设','label':'neutral','label0':'entailment'},
                             {'id':2,'sentence1':'前提','sentence2':'假设','label':'-'}])
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0]['target'], 'neutral')
        self.assertEqual(samples[0]['input'], {'premise':'前提','hypothesis':'假设'})
        with self.assertRaises(ValueError):
            data.ocnli([{'id':3,'label':'unexpected'}])

    def test_banking_preserves_the_full_label_space(self):
        samples = data.banking([{'text':'Help with card','category':'card'}], ['card','cash','transfer'])
        self.assertEqual(samples[0]['target'], 'card')
        self.assertEqual(len(samples[0]['criteria']), 3)
        self.assertEqual(samples[0]['input'], 'Help with card')

    def test_boolq_sends_passage_but_not_answer(self):
        sample = data.boolq([{'question':'Is it red?','passage':'It is blue.','answer':False}])[0]
        self.assertEqual(sample['target'], 'No')
        self.assertEqual(sample['input'], {'question':'Is it red?','passage':'It is blue.'})

    def test_bfcl_extracts_only_unique_name_without_arguments(self):
        rows = [{'id':'m0','question':[[{'role':'user','content':'Add two numbers'}]],
                 'function':[{'name':'add','description':'Sum','parameters':{}},{'name':'sub','description':'Subtract','parameters':{}}]}]
        answer = [{'id':'m0','ground_truth':[{'add':{'x':[1],'y':[2]}}]}]
        sample = data.bfcl(rows, answer)[0]
        self.assertEqual(sample['target'], 'add')
        self.assertEqual(set(sample['criteria']), {'add','sub'})
        self.assertNotIn('ground_truth', sample['input'])
        with self.assertRaises(ValueError):
            data.bfcl(rows, [{'id':'m0','ground_truth':[{'missing':{}}]}])
