from modelscope.pipelines import pipeline

classifier = pipeline('zero-shot-classification',
                      'damo/nlp_structbert_zero-shot-classification_chinese-large')

def get_text_type(sentence):
    labels = ['叙述','核心观点','细节描写','情感共鸣',"科学技术","通知报告"]
    if len(sentence) < 30:
        text_type = {
            "叙述": 0,
            "情感共鸣": 0,
            "核心观点": 0,
            "细节描写": 0,
            "科学技术": 0,
            "通知报告": 0,
            "最终类型": "其他",
        }
        return text_type
    x = classifier(sentence, candidate_labels=labels, multi_label=True)
    z = x['labels'][0]

    text_type = {
        "叙述": 0,
        "情感共鸣": 0,
        "核心观点": 0,
        "细节描写": 0,
        "科学技术": 0,
        "通知报告": 0,
        "最终类型": "",
    }
    if z == '叙述' :
        if x['scores'][0] <= 0.65:
            text_type['最终类型']='其他'
        else :
            text_type['最终类型']=z
    elif z == '核心观点' :
        if x['scores'][0] <= 0.6:
            text_type['最终类型']='其他'
        else :
            text_type['最终类型']=z
    elif z == '情感共鸣':
        if x['scores'][0] <= 0.6:
            text_type['最终类型']='其他'
        else :
            text_type['最终类型']=z
    elif z == '细节描写':
        if x['scores'][0] <= 0.5:
            text_type['最终类型']='其他'
        else :
            text_type['最终类型']=z
    elif z == '科学技术':
        if x['scores'][0] <= 0.5:
            text_type['最终类型']='其他'
        else :
            text_type['最终类型']=z
    elif z == '通知报告':
        if x['scores'][0] <= 0.5:
            text_type['最终类型']='其他'
        else :
            text_type['最终类型']=z

    for index,label in enumerate(x['labels']):
        if label == '叙述':
            text_type['叙述'] = x['scores'][index]
        elif label == '核心观点':
            text_type['核心观点'] = x['scores'][index]
        elif label == '细节描写':
            text_type['细节描写'] = x['scores'][index]
        elif label == '情感共鸣':
            text_type['情感共鸣'] = x['scores'][index]
        elif label == '科学技术':
            text_type['科学技术'] = x['scores'][index]
        elif label == '通知报告':
            text_type['通知报告'] = x['scores'][index]
    #print(text_type)
    return text_type