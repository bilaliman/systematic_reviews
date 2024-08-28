import re
import pypdfium2 as pdfium

author = r"(?:[A-Z][0-9A-Za-z'`\?-]+)"
etal = r"(?:et al\.?)"
vol = r"(?:Vol\.? [0-9]+,? No\.? [0-9]+)"
additional = f"(?:,? (?:(?:and |& )?{author}|{etal}|{vol}))"
date_num = "(?:January|February|March|April|May|June|July|August｜September｜October｜November｜December)*[, ]*[0-9]{0,2}"
year_num = "(?:19|20)[0-9][0-9] *[–-]? *(?:(?:19|20)[0-9][0-9])?"
page_num = "(?:p+\.? [0-9]+)?"  # Always optional
year = fr"(?:, *{date_num}[, ]*{year_num}[, ]*{page_num}| *\({date_num}{year_num}{page_num}\))"
regex_references_incontent = fr'\b(?!(?:Although|Also)\b){author}{additional}*{year}'

regex_references_end = "(?i:(?:Reference|references|References|Referências|Bibliography|Endnotes|Literatur|Bibliografia|Bibliografía|KIRJALLISUUS|Literature):.+)"
regex_references_end2 = "(?!(?<=(?i:Terms of) )|(?<=(?i:cheme))|(?<=(?i:Annotated) )|(?<=(?i:the) )|(?<=(?i:Funding) )|(?<=(?i:end) )|(?<=(?i:Available) ))(?:Reference|references|References|Referências|Referencias|REFERENCE|REFERENCES|Bibliography|bibliography|Bibliografia|Bibliografía|BIBLIOGRAPHY|Endnotes|ENDNOTES|Literatur|KIRJALLISUUS|Sources|Literature|NOTES|Notes) (?!(?i:Review|Cited｜Case|group|PRICING|guide|Board|list|Committee|Curriculum|Note|Appendix|Annex|Annexes|Appendices|Applicability|Acknowledgement|Manual|Boxes|Code|Codes|Effectiveness|new|index|Laboratory|Abstract|Under|Patient|[.]+)) ?[^a-zA-Z]*(?:[A-Z](?:(?!(?:\. |\.){10,}).)+)$"
case1 = "R\s*[eE]\s*[fF]\s*[eE]\s*[rR]\s*[eE]\s*[nN]\s*[cC]\s*[eE]\s*[sS]?.+"
case2 = "[rR]\s*E\s*[fF]\s*[eE]\s*[rR]\s*[eE]\s*[nN]\s*[cC]\s*[eE]\s*[sS]?.+"
case3 = "[rR]\s*[eE]\s*F\s*[eE]\s*[rR]\s*[eE]\s*[nN]\s*[cC]\s*[eE]\s*[sS]?.+"
case4 = "[rR]\s*[eE]\s*[fF]\s*E\s*[rR]\s*[eE]\s*[nN]\s*[cC]\s*[eE]\s*[sS]?.+"
case5 = "[rR]\s*[eE]\s*[fF]\s*[eE]\s*R\s*[eE]\s*[nN]\s*[cC]\s*[eE]\s*[sS]?.+"
case6 = "[rR]\s*[eE]\s*[fF]\s*[eE]\s*[rR]\s*E\s*[nN]\s*[cC]\s*[eE]\s*[sS]?.+"
case7 = "[rR]\s*[eE]\s*[fF]\s*[eE]\s*[rR]\s*[eE]\s*N\s*[cC]\s*[eE]\s*[sS]?.+"
case8 = "[rR]\s*[eE]\s*[fF]\s*[eE]\s*[rR]\s*[eE]\s*[nN]\s*C\s*[eE]\s*[sS]?.+"
case9 = "[rR]\s*[eE]\s*[fF]\s*[eE]\s*[rR]\s*[eE]\s*[nN]\s*[cC]\s*E\s*[sS]?.+"
case10 = "[rR]\s*[eE]\s*[fF]\s*[eE]\s*[rR]\s*[eE]\s*[nN]\s*[cC]\s*[eE]\s*S.+"
case11 = "S\s*E\s*C\s*N\s*E\s*R\s*E\s*F\s*E\s*R.+"
regex_references_end3 = "{case1}|{case2}|{case3}|{case4}|{case5}|{case6}|{case7}|{case8}|{case9}|{case10}|{case11}"
regex_acknowledgment = "((?:Acknowledgments|Acknowledgements|ACKNOWLEDGMENTS|ACKNOWLEDGEMENTS|Acknowledgement |Acknowledge )(?!(?i: Executive Summary)):? ?[—.(]?(?:\(cid:2\))? ?[a-zA-Z].+?)(?:(?i:Executive Summary|Table of Contents|Contents|Introduction|PREAMBLE|Highlights|Overview|Contributions))"

references_incontent = []
references_end = []
acknowledgments = []


def reference(txt_content):
    txt_content = re.sub("\n+", " ", txt_content)
    txt_content = re.sub("\s+", " ", txt_content)
    
    temp = re.findall(regex_references_end, txt_content)
    if len(temp) > 0:
        temp = temp[0]
    else:
        temp = re.findall(regex_references_end2, txt_content)
        if len(temp) > 0:
            temp = temp[0]
        else:
            temp = re.findall(regex_references_end3, txt_content)
            if len(temp) > 0:
                temp = temp[0]
            else:
                temp = ""
    if re.search("[.]{20,}", temp):
        temp = ""
    
    matches = re.findall(regex_references_incontent, txt_content)
    if len(matches) > 0:
        matches = matches
    else:
        matches = []
    
    ack_matches = ''
    ack_index = [(m.start(0), m.end(0)) for m in re.finditer("(?:Acknowledgments|Acknowledgements|ACKNOWLEDGMENTS|ACKNOWLEDGEMENTS|Acknowledgement |Acknowledge )", txt_content)]
    if len(ack_index) > 0:
        ack_index = ack_index[-1][0]
        if ack_index / len(txt_content) <= 0.3: # acknowledgment at the beginning
            ack_matches = re.findall(regex_acknowledgment, txt_content)
            if len(ack_matches) > 0:
                ack_matches = ack_matches[0]
            else:
                ack_matches = ""
        else: # acknowledgment at the end
            ack_matches = re.findall("(?:Acknowledgments|Acknowledgements|ACKNOWLEDGMENTS|ACKNOWLEDGEMENTS|Acknowledgement |Acknowledge ):? ?[—.(]?(?:\(cid:2\))? ?[a-zA-Z].+", txt_content)
            if len(ack_matches) > 0:
                ack_matches = ack_matches[0]
            else:
                ack_matches = ""

    return references_end,references_incontent,acknowledgments   



def reference2(txt_content):
    references = 'Reference|References|Referências|Referencias|REFERENCE|REFERENCES|Bibliography|Bibliografia|Bibliografía|Endnotes|KIRJALLISUUS'
    references = references.lower().split('|')
    mylist = []

    for reference in references:
        last_pos = txt_content.lower().rfind(reference)     
        if last_pos!= -1:
            mylist.append((reference,last_pos))

    return mylist, len(txt_content)   

def appendix(txt_content):
    appendices = 'appendix|appendices' 
    appendices = appendices.lower().split('|') 
    mylist = []

    for app in appendices:
        first_pos = txt_content.lower().find(app)
        if first_pos!= -1:
            mylist.append((app,first_pos))
    return mylist,len(txt_content)
    


