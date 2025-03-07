
CRITERIA_BASED_JUDGING_PROMPT  = '''
Here is an academic survey about the topic "[TOPIC]":
---
[SURVEY]
---

<instruction>
Please evaluate this survey about the topic "[TOPIC]" based on the criterion above provided below, and give a score from 1 to 5 according to the score description:
---
Criterion Description: [Criterion Description]
---
Score 1 Description: [Score 1 Description]
Score 2 Description: [Score 2 Description]
Score 3 Description: [Score 3 Description]
Score 4 Description: [Score 4 Description]
Score 5 Description: [Score 5 Description]
---
Return the score without any other information:
'''

NLI_PROMPT = '''
---
Claim:
[CLAIM]
---
Source: 
[SOURCE]
---
Claim:
[CLAIM]
---
Is the Claim faithful to the Source? 
A Claim is faithful to the Source if the core part in the Claim can be supported by the Source.\n
Only reply with 'Yes' or 'No':
'''

ROUGH_OUTLINE_PROMPT = '''
You wants to write a overall and comprehensive academic survey about "[TOPIC]".\n\
You are provided with a list of papers related to the topic below:\n\
---
[PAPER LIST]
---
You need to draft a outline based on the given papers.
The outline should contains a title and several sections.
Each section follows with a brief sentence to describe what to write in this section.
The outline is supposed to be comprehensive and contains [SECTION NUM] sections.

Return in the format:
<format>
Title: [TITLE OF THE SURVEY]
Section 1: [NAME OF SECTION 1]
Description 1: [DESCRIPTION OF SENTCTION 1]

Section 2: [NAME OF SECTION 2]
Description 2: [DESCRIPTION OF SENTCTION 2]

...

Section K: [NAME OF SECTION K]
Description K: [DESCRIPTION OF SENTCTION K]
</format>
The outline:
'''


MERGING_OUTLINE_PROMPT = '''
You are an expert in artificial intelligence who wants to write a overall survey about [TOPIC].\n\
You are provided with a list of outlines as candidates below:\n\
---
[OUTLINE LIST]
---
Each outline contains a title and several sections.
Each section follows with a brief sentence to describe what to write in this section.
You need to generate a final outline based on these provided outlines to make the final outline show comprehensive insights of the topic and more logical.
Return the in the format:
<format>
Title: [TITLE OF THE SURVEY]
Section 1: [NAME OF SECTION 1]
Description 1: [DESCRIPTION OF SENTCTION 1]

Section 2: [NAME OF SECTION 2]
Description 2: [DESCRIPTION OF SENTCTION 2]

...

Section K: [NAME OF SECTION K]
Description K: [DESCRIPTION OF SENTCTION K]
</format>
Only return the final outline without any other informations:
'''

SUBSECTION_OUTLINE_PROMPT = '''
You are an expert in artificial intelligence who wants to write a overall survey about [TOPIC].\n\
You have created a overall outline below:\n\
---
[OVERALL OUTLINE]
---
The outline contains a title and several sections.\n\
Each section follows with a brief sentence to describe what to write in this section.\n\n\
<instruction>
You need to enrich the section [SECTION NAME].
The description of [SECTION NAME]: [SECTION DESCRIPTION]
You need to generate the framwork containing several subsections based on the overall outlines.\n\
Each subsection follows with a brief sentence to describe what to write in this subsection.
These papers provided for references:
---
[PAPER LIST]
---
Return the outline in the format:
<format>
Subsection 1: [NAME OF SUBSECTION 1]
Description 1: [DESCRIPTION OF SUBSENTCTION 1]

Subsection 2: [NAME OF SUBSECTION 2]
Description 2: [DESCRIPTION OF SUBSENTCTION 2]

...

Subsection K: [NAME OF SUBSECTION K]
Description K: [DESCRIPTION OF SUBSENTCTION K]
</format>
</instruction>
Only return the outline without any other informations:
'''

EDIT_FINAL_OUTLINE_PROMPT = '''
You are an expert in artificial intelligence who wants to write a overall survey about [TOPIC].\n\
You have created a draft outline below:\n\
---
[OVERALL OUTLINE]
---
The outline contains a title and several sections.\n\
Each section follows with a brief sentence to describe what to write in this section.\n\n\
Under each section, there are several subsections.
Each subsection also follows with a brief sentence of descripition.
Some of the subsections may be repeated or overlaped.
You need to modify the outline to make it both comprehensive and logically coherent with no repeated subsections.
Repeated subsections among sections are not allowed!
Return the final outline in the format:
<format>
# [TITLE OF SURVEY]

## [NAME OF SECTION 1]
Description: [DESCRIPTION OF SECTION 1]
### [NAME OF SUBSECTION 1]
Description: [DESCRIPTION OF SUBSECTION 1]
### [NAME OF SUBSECTION 2]
Description: [DESCRIPTION OF SUBSECTION 2]
...

### [NAME OF SUBSECTION L]
Description: [DESCRIPTION OF SUBSECTION L]
## [NAME OF SECTION 2]

...

## [NAME OF SECTION K]
...

</format>
Only return the final outline without any other informations:
'''

CHECK_CITATION_PROMPT = '''
You are an expert in artificial intelligence who wants to write a overall and comprehensive survey about [TOPIC].\n\
Below are a list of papers for references:
---
[PAPER LIST]
---
You have written a subsection below:\n\
---
[SUBSECTION]
---
<instruction>
The sentences that are based on specific papers above are followed with the citation of "paper_title" in "[]".
For example 'the emergence of large language models (LLMs) [Language models are few-shot learners; Language models are unsupervised multitask learners; PaLM: Scaling language modeling with pathways]'

Here's a concise guideline for when to cite papers in a survey:
---
1. Summarizing Research: Cite sources when summarizing the existing literature.
2. Using Specific Concepts or Data: Provide citations when discussing specific theories, models, or data.
3. Comparing Findings: Cite relevant studies when comparing or contrasting different findings.
4. Highlighting Research Gaps: Cite previous research when pointing out gaps your survey addresses.
5. Using Established Methods: Cite the creators of methodologies you employ in your survey.
6. Supporting Arguments: Cite sources that back up your conclusions and arguments.
7. Suggesting Future Research: Reference studies related to proposed future research directions.
---

Now you need to check whether the citations of "paper_title" in this subsection is correct.
A correct citation means that, the content of corresponding paper can support the sentences you write.
Once the citation can not support the sentence you write, correct the paper_title in '[]' or just remove it.

Remember that you can only cite the 'paper_title' provided above!!!
Any other informations like authors are not allowed cited!!!
Do not change any other things except the citations!!!
</instruction>
Only return the subsection with correct citations:
'''

CHECK_CITATION_PROMPT_CN = '''
您是一位人工智能专家，想要撰写一篇关于[TOPIC]的全面综述。\n\
以下是参考文献列表：
---
[PAPER LIST]
---
您已撰写了以下小节：\n\
---
[SUBSECTION]
---
<instruction>
基于上述特定论文的句子后面应附有“paper_title”的引用，格式为“[]”。
例如，“大型语言模型（LLMs）的出现[Language models are few-shot learners; Language models are unsupervised multitask learners; PaLM: Scaling language modeling with pathways]”

以下是关于何时在综述中引用论文的简明指南：
---
1. 总结研究：在总结现有文献时引用来源。
2. 使用特定概念或数据：在讨论特定理论、模型或数据时提供引用。
3. 比较研究结果：在比较或对比不同研究结果时引用相关研究。
4. 突出研究空白：在指出您的综述所解决的空白时引用先前的研究。
5. 使用已建立的方法：引用您在综述中使用的方法的创建者。
6. 支持论点：引用支持您结论和论点的来源。
7. 建议未来研究：参考与建议的未来研究方向相关的研究。
---

现在您需要检查此小节中“paper_title”的引用是否正确。
正确的引用意味着相应论文的内容可以支持您所写的句子。
一旦引用不能支持您所写的句子，请更正“[]”中的paper_title或直接删除。

请记住，您只能引用上面提供的“paper_title”!!!
不允许引用作者等其他信息!!!
除了引用外，不要更改任何其他内容!!!
</instruction>
仅返回具有正确引用的小节：
'''

SUBSECTION_WRITING_PROMPT = '''
You are an expert in artificial intelligence who wants to write a overall and comprehensive survey about [TOPIC].\n\
You have created a overall outline below:\n\
---
[OVERALL OUTLINE]
---
Below are a list of papers for references:
---
[PAPER LIST]
---

<instruction>
Now you need to write the content for the subsection:
"[SUBSECTION NAME]" under the section: "[SECTION NAME]"
The details of what to write in this subsection called [SUBSECTION NAME] is in this descripition:
---
[DESCRIPTION]
---

Here is the requirement you must follow:
1. The content you write must be more than [WORD NUM] words.
2. When writing sentences that are based on specific papers above, you cite the "paper_title" in a '[]' format to support your content. An example of citation: 'the emergence of large language models (LLMs) [Language models are few-shot learners; PaLM: Scaling language modeling with pathways]'
    Note that the "paper_title" is not allowed to appear without a '[]' format. Once you mention the 'paper_title', it must be included in '[]'. Papers not existing above are not allowed to cite!!!
    Remember that you can only cite the paper provided above and only cite the "paper_title"!!!
3. Only when the main part of the paper support your claims, you cite it.


Here's a concise guideline for when to cite papers in a survey:
---
1. Summarizing Research: Cite sources when summarizing the existing literature.
2. Using Specific Concepts or Data: Provide citations when discussing specific theories, models, or data.
3. Comparing Findings: Cite relevant studies when comparing or contrasting different findings.
4. Highlighting Research Gaps: Cite previous research when pointing out gaps your survey addresses.
5. Using Established Methods: Cite the creators of methodologies you employ in your survey.
6. Supporting Arguments: Cite sources that back up your conclusions and arguments.
7. Suggesting Future Research: Reference studies related to proposed future research directions.
---

</instruction>
Return the content of subsection "[SUBSECTION NAME]" in the format:
<format>
[CONTENT OF SUBSECTION]
</format>
Only return the content more than [WORD NUM] words you write for the subsection [SUBSECTION NAME] without any other information:
'''

SUBSECTION_WRITING_PROMPT_CN = '''
您是一位人工智能专家，想要撰写一篇关于[TOPIC]的全面综述。\n\
您已创建了一个总体大纲如下：\n\
---
[OVERALL OUTLINE]
---
以下是参考文献列表：
---
[PAPER LIST]
---

<instruction>
现在您需要为小节撰写内容：
"[SUBSECTION NAME]"，位于章节："[SECTION NAME]"下
关于这个名为[SUBSECTION NAME]的小节的写作细节在此描述中：
---
[DESCRIPTION]
---

您必须遵循以下要求：
1. 您撰写的内容必须超过[WORD NUM]字。
2. 在撰写基于上述特定论文的句子时，您需要在'[]'格式中引用"paper_title"以支持您的内容。引用示例：'the emergence of large language models (LLMs) [Language models are few-shot learners; PaLM: Scaling language modeling with pathways]'
    请注意，"paper_title"不允许在没有'[]'格式的情况下出现。一旦提到'paper_title'，它必须包含在'[]'中。不允许引用上面不存在的论文！
    请记住，您只能引用上面提供的论文，并且只能引用"paper_title"！
3. 只有当论文的主要部分支持您的主张时，您才引用它。


以下是撰写综述时引用论文的简明指南：
---
1. 总结研究：在总结现有文献时引用来源。
2. 使用特定概念或数据：在讨论特定理论、模型或数据时提供引用。
3. 比较研究结果：在比较或对比不同研究结果时引用相关研究。
4. 突出研究空白：在指出您的综述所解决的空白时引用先前的研究。
5. 使用已建立的方法：引用您在综述中使用的方法的创建者。
6. 支持论点：引用支持您的结论和论点的来源。
7. 建议未来研究：参考与建议的未来研究方向相关的研究。
---

</instruction>
以以下格式返回小节"[SUBSECTION NAME]"的内容：
<format>
[CONTENT OF SUBSECTION]
</format>
仅返回您为小节[SUBSECTION NAME]撰写的超过[WORD NUM]字的内容，不包含任何其他信息：
'''


LCE_PROMPT = '''
You are an expert in artificial intelligence who wants to write a overall and comprehensive survey about [TOPIC].

Now you need to help to refine one of the subsection to improve th ecoherence of your survey.

You are provied with the content of the subsection along with the previous subsections and following subsections.

Previous Subsection:
--- 
[PREVIOUS]
---

Following Subsection:
---
[FOLLOWING]
---

Subsection to Refine: 
---
[SUBSECTION]
---


If the content of Previous Subsection is empty, it means that the subsection to refine is the first subsection.
If the content of Following Subsection is empty, it means that the subsection to refine is the last subsection.

Now refine the subsection to enhance coherence, and ensure that the content of the subsection flow more smoothly with the previous and following subsections. 

Remember that keep all the essence and core information of the subsection intact. Do not modify any citations in [] following the sentences.

Only return the whole refined content of the subsection without any other informations (like "Here is the refined subsection:")!

The subsection content:
'''

LCE_PROMPT_CN = '''
您是一位人工智能专家，想要撰写一篇关于[TOPIC]的全面综述。

现在，您需要帮助改进其中一个小节，以提高您的综述的连贯性。

您将获得该小节的内容以及前后小节的内容。

前一小节：
---
[PREVIOUS]
---

后一小节：
---
[FOLLOWING]
---

需要改进的小节：
---
[SUBSECTION]
---

如果前一小节的内容为空，这意味着需要改进的小节是第一小节。
如果后一小节的内容为空，这意味着需要改进的小节是最后一小节。

现在，请改进该小节以增强连贯性，并确保该小节的内容与前后小节更顺畅地衔接。

请记住，保持小节的所有精髓和核心信息不变。不要修改句子后面的[]中的任何引用。

仅返回整个改进后的小节内容，不包含任何其他信息（例如“这是改进后的小节：”）！

小节内容：
'''
