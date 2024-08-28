import pdfminer
import json
import re
import pypdfium2 as pdfium
from pdfminer.high_level import extract_text

from reference import reference, reference2,appendix



'''pdf = pdfium.PdfDocument("column_Y_papers/#17340 - National 2016.pdf")
version = pdf.get_version()  # get the PDF standard version
n_pages = len(pdf)  # get the number of pages in the document

# Load a text page helper
page = pdf[18]
textpage = page.get_textpage()'''



def extract_relevant_content(pdf_path):

    # __________________Select pdf content before references and after appendix____________________


    txt_content = extract_text(pdf_path)  

    if reference2(txt_content)[0]!=[]:
        ref_mark = max([x[1] for x in reference2(txt_content)[0]])
        #Look for appendix after references
        after_ref_txt = txt_content[ref_mark:]
        if appendix(after_ref_txt)[0]!=[]:
            app_mark = ref_mark + min([x[1] for x in appendix(after_ref_txt)[0]])
        else:
            app_mark = -1
    else:
        ref_mark = -1
        app_mark = -1

    print(ref_mark,app_mark,len(txt_content))
    txt_content1 = txt_content[:ref_mark] 
    txt_content2 = txt_content[app_mark:]

    # __________________Choose delimiter for paragraphs____________________

    symbols = ['•','']
    paragraphs = []

    for txt_content in [txt_content1,txt_content2]:
        if len(txt_content)<10:
            continue
        segments = txt_content.split('\n\n')
        segments = [x for x in segments if x.strip()!='' and x.strip().isdigit()==False]
        avg_paragraph_length = sum([len(x) for x in segments])/len([len(x) for x in segments])
        print('Avg paragraph length: ',avg_paragraph_length)

        print(len(segments))
        if avg_paragraph_length < 85: # 85 is the upper limit for line char length
            # This means that individual lines are matched, the paragraphs are not identified correctly.  
            i = 0
            k = 0

            while i< len(segments):
                paragraph = ''
                segment = segments[i].strip()
                while (segment[-1]!='.' and segment[-1]!='!' and segment[-1]!='?' and segment[-4:-1] not in ['e.g','i.e',' al', 'rox'] and i< len(segments)):
                    paragraph = paragraph + ' ' + segments[i].strip()
                    i = i+1
                    if i<len(segments):
                        segment = segments[i].strip()
                if i<len(segments):
                    paragraph = paragraph + ' ' + segments[i].strip() 
                k += 1
                paragraphs.append(paragraph) #print(k,paragraph)   
                i += 1
            

        else: 
            # This means that paragraphs are mostly identified correctly.  
            i = 0
            k = 0
            while i< len(segments):
                segment = segments[i]
                if segment.strip().isdigit() and segment!='':
                    i += 1    
                else: 
                    paragraph = ''
                    segment = segments[i].strip()
                    while (segment[-1]!='.' and segment[-1]!='!' and segment[-1]!='?' and segment[-4:-1] not in ['e.g','i.e',' al', 'rox'] and i< len(segments)):
                        paragraph = paragraph + ' ' + segments[i].strip()
                        i = i+1
                        if i<len(segments):
                            segment = segments[i].strip()
                    if i<len(segments):
                        paragraph = paragraph + ' ' + segments[i].strip() 
                    k += 1
                    paragraphs.append(paragraph) #print(k,paragraph)   
                    i += 1
    return paragraphs                    

