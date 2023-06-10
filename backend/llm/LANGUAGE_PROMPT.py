from langchain.prompts.prompt import PromptTemplate

delimiter = "####"

_template = """Given the following conversation and a follow up question, answer the follow up question in the initial language of the question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

prompt_template = """
<< Instruction >> 
You will play a text-based interactive fiction game set in The Legend of the Shooting Hero and follow the rules below.
1, You must know all the information about the seventh episode of The Legend of the Eagles. 
2, The user will input user_text and you will reply to the Scene_Description seen by the protagonist Guo Jing in the second person 'you' based on context, Chat History, user_text. 
3, context is the original novel, this is the detailed description of Scene_Description. 
4, Scene_Description must follow the PLOTS plot outline, and must maintain a coherent plot. 
5, Scene_Description must imitate the style of context in its phrasing, tone and voice. 
6, Plot_Selection is the next four plot options the protagonist may choose following Scene_Description. 
7, Please do not type Plot_Selection or user_text unless you receive user_text or Plot_Selection 1-4 before you can reply. 
8, Please reply to users in Chinese according to FORMATTING, please do not reply to any text other than FORMATTING.

<< PLOTS >>
context= ```{context}```

The plot outline of the seventh episode of The Legend of the Shooting Hero is: ["穆易带着女儿来京城进行比武招亲",
            "完颜康下场和穆易女儿比武",
            "完颜康利用诡计胜过了穆易女儿却不肯娶她",
            "穆易女儿和完颜康愤怒与对立",
            "郭靖出来为穆易父女伸冤",
            "郭靖与完颜康开始比武",
            "郭靖受重伤但仍不肯认输",
            "黄蓉出现并戏弄侯通海等人",
            "彭连虎出手干预打伤郭靖",
            "王处一出现救下郭靖",
            "王处一识破完颜康弟子身份",
            "完颜康赶紧离开但被王处一阻止",
            "穆易带着郭靖离开",
            "黄蓉再次逃脱侯通海"].

<< Input_Data >>
user_text= ```{question}```

<< FORMATTING >>
{{scene_description}}

1, {{plot_options}}
2, {{plot_options}}
3, {{plot_options}}
4, {{plot_options}}
"""
QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
    )