entity_types = ['GPE.NAM','GPE.NOM','LOC.NAM','LOC.NOM',
                'ORG.NAM','ORG.NOM','PER.NAM','PER.NOM']

def get_entity(data, label):
    """
    给定实体类型，返回实体在文本中的起始位置，若无对应类型实体返回空列表
    """
    begins = []
    ends = []
    for index in range(len(data[1])):
        if data[1][index].startswith('B-'+label):
            begins.append(index)
    for begin in begins:
        if begin == len(data[0]):
            ends.append(begin)
        else: 
            for i in range(begin+1, len(data[1])):
                if not data[1][i].startswith('I-'+label):
                    ends.append(i-1)
                    break
            
    return begins,ends

def build_data(d):
    '''
    用字典的方式存储数据，
    text：训练文本，list
    entity_type-index：每种实体的起始位置，list
    '''
    data = {}
    data['text'] = d[0]
    for entity_type in entity_types:
        data[entity_type+'-index'] = get_entity(d, entity_type)
    return data

def get_final_data(path):
    raw_data = []
    with open(path, 'r', encoding = 'utf-8') as f:
        tmp = []
        for line in f:
            if line != '\n': 
                tmp.append(line.strip('\n'))
            else:
                raw_data.append(tmp)
                tmp = []
    seperated_data = []
    for data in raw_data:
        sentence = []
        marks = []
        for token in data:
            ch, mark = token.split('\t')
            ch = ch[0]
            sentence.append(ch)
            marks.append(mark)
        seperated_data.append([sentence, marks])
    final = {}
    for index in range(len(seperated_data)):
        final[index] = build_data(seperated_data[index])
    
    return final