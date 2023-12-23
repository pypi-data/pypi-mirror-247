from .tags_precitor import TagsPredictor
from .morph_precitor import MorphPredictor

morph = {
  "=ADJ": 83832,
  "=ADP": 83843,
  "=ADV": 83842,
  "=CONJ": 83837,
  "=DET": 83836,
  "=H": 83828,
  "=INTJ": 83833,
  "=LATN": 83831,
  "=NOUN": 83840,
  "=NUM": 83839,
  "=PART": 83838,
  "=PRON": 83830,
  "=PUNCT": 83841,
  "=SYM": 83834,
  "=VERB": 83835,
  "=X": 83829
}.keys()

class RUMorph:
    def __init__(self) -> None:
        self.t = TagsPredictor()
        self.m = MorphPredictor()
    def load(self):
        self.t.load("/Users/denis/Codes/RUMorph/rumorph/models/onnx_syntax_2")
        self.m.load("/Users/denis/Codes/RUMorph/rumorph/models/onnx_morph")

    def _convert_lists(self, list1, list2):
        converted_list = []
        for item1, item2 in zip(list1, list2):
            #print(item1)
            converted_item = {
                "word": item1["word"],
                "tags": item2["entity"] + "|" + item1["entity"]
            }
            converted_list.append(converted_item)
        return converted_list
    def _convert_morph(self, list1):
        out = []
        for chunk in list1:
            out.append(chunk["word"].strip() + "=" + chunk["entity"])
        return out
    
    def _convert_out(self, list_1):
        out = []
        for chunk in list_1:
            if chunk["word"] in morph:
                out[-1] = out[-1] + chunk["word"]
            else:
                out.append(chunk["word"])
        for i in range(len(out)):
            out[i] = out[i] + "|" + list_1[i]['entity']
        return [item.split('=',1) for item in out]
    

    def process(self, text):
        processed2 = self._convert_morph(self.m.predict_morph(text))
        processed1 = self.t.predict_tags(processed2)
        print(processed1)
        return self._convert_out(processed1)#self._convert_lists(processed1, processed2)
