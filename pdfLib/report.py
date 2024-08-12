"""report - simple PDF report generator for NDIToolbox

Chris R. Coughlin (TRI/Austin, Inc.)
"""

import pyPdf
from reportlab.lib.pagesizes import letter, portrait
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import utils
import os.path
import tempfile

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.lib.units import inch,cm,mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image
from reportlab.lib.enums import *   
     
from reportlab.lib import colors

from reportlab.lib.units import inch, cm

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, \
      PageBreak

from reportlab.pdfgen import canvas

import time

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY


import sys

sys.path.append("C:\\AitangResearch\\") # add the root directory to python path.


from configureFile.configFile import tomo_logo,sinogram_logo

print tomo_logo


class ReportSection(object):
    """Defines a section for the Report class"""

    def __init__(self, heading):
        self.heading = heading
        self.contents = []

    def add_figure(self, figure, caption=None):
        """Adds a figure and optional caption to the contents.  The figure argument should point to the full path
        and filename of the image to include."""
        self.contents.append({'figure':figure,
                              'caption':caption})

    def add_table(self, table, caption=None):
        """Adds a table and optional caption to the contents.  The table should be a 2D list, where table element
        [i][j] becomes the contents of the table cell at row[i] column [j].
        """
        self.contents.append({'table':table,
                              'caption':caption})

    def add_text(self, text):
        """Adds a block of text to the contents.  Text can be a single string or a list of strings; the final text
        block is separated by newline characters (\n).  To insert a blank line between paragraphs use the empty
        string '\n' in the block."""
        if isinstance(text, list):
            text = ''.join(text)
        self.contents.append({'text':text.split('\n')})


class Report(object):
    """Basic PDF report generator for NDIToolbox"""

    def __init__(self, output_filename, front_matter=None, end_matter=None):
        self.output_filename = os.path.normcase(output_filename)
        
        self.front_matter=front_matter
        
        self.end_matter=end_matter
        
        if front_matter is not None:
            self.front_matter = os.path.normcase(front_matter)
        if end_matter is not None:
            self.end_matter = os.path.normcase(end_matter)
        self.sections = []

    def build_table(self, data):
        """Generates and returns a simple ReportLab table from the specified 2D list.  The first row (data[0]) is taken
        as a header, use an empty row (data[0] = []) to skip."""
        style = []
        
        j=len(data)-1
        
             
        if len(data[0]) > 0:
##            style.extend([('BACKGROUND', (0, 0), (-1, 0), (0.31, 0.40, 0.51)),
##                          ('TEXTCOLOR', (0,0), (-1, 0), (0.89, 0.82, 0.60)),
##                          ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER')])


            style.extend([('LINEABOVE', (0, 0), (-1, 0),0.05*cm, colors.green),
                          ('LINEBELOW', (0, 0), (-1, 0),0.05*cm, colors.green),
                          ('LINEBELOW',(0,j),(-1,j),0.05*cm,colors.green),                          
                          ('ALIGNMENT', (0, 0), (-1, -1), 'LEFT'),
                          ('ALIGNMENT',(0,0),(0,j),'LEFT'),
                        ])
        else:
            
            data = data[1:]
            
            
        table = Table(data, style=style,hAlign='LEFT')
        
        
        return table
    
    
    def pageHeadFoot(self,canvas, doc):
        
        
        '''
        Draw the header and footer on every pages.         
                
        '''
        
        
        canvas.saveState()
        
        # draw head information on every pages        
        
        canvas.setFont('Times-Roman',23)
        canvas.drawString(4.2*cm,27.5*cm,'Tomo Plan MLC LOT Histogram Check')
      
        canvas.drawImage(tomo_logo, 1.1*cm,27*cm, width=0.9*inch,height=0.8*inch) 
        
        canvas.drawImage(sinogram_logo, 7.1*inch,27*cm, width=0.9*inch,height=0.8*inch)
        
        canvas.setStrokeColorRGB(0,0,1)
        
        canvas.setLineWidth(0.12*cm)
        
        canvas.line(0.2*inch,26.5*cm,8*inch,26.5*cm)
        
                
        # draw footer information
        
        
        canvas.setStrokeColorRGB(0,0,1)
        
        canvas.setLineWidth(0.12*cm)
        
        canvas.line(0.2*inch,2*cm,8*inch,2*cm)
        
               
        
        
        canvas.setFont('Times-Roman',12)
        canvas.drawString(4*inch, 0.7* cm, "Page %d" % doc.page)
        
        localtime = time.asctime( time.localtime(time.time()) )
        
        
        version='TomoLOTChecker V1.0 '
        
        canvas.drawString(0.2*inch, 0.7* cm,localtime)
        
        canvas.drawString(6*inch, 0.7* cm,version)
        
        
        canvas.restoreState()
        
    def write(self):
        """Assembles the final PDF and writes to disk."""
        pdf_writer = pyPdf.PdfFileWriter()
        if self.front_matter is not None:
            front_matter = pyPdf.PdfFileReader(file(self.front_matter, "rb"))
            for page in range(front_matter.getNumPages()):
                pdf_writer.addPage(front_matter.getPage(page))
        working_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        
        
        doc = SimpleDocTemplate(working_file,topMargin=1.4*inch,botomMargin=0.9*inch)
        
        
        doc.pagesize = portrait(A4)
        story = []
        styles = getSampleStyleSheet()
        for section in self.sections:
##            heading_text = section.heading
            
            heading_text='<u>'+section.heading+'<u>'
            
            story.append(Paragraph(heading_text, styles['Heading1']))
            for content in section.contents:
                
                story.append(Spacer(1, 10))
                
                if 'figure' in content:
                    figure = content['figure']
                    
                                       
                    if os.path.exists(figure):
                        im = utils.ImageReader(figure)
                        img_width, img_height = im.getSize()
                        aspect = img_height / float(img_width)
                        
                        img_width2=15*cm
                        story.append(Image(figure, width=img_width2, height=(img_width2*aspect)))
                    if content.get('caption', None) is not None:
                        caption_text = '<font size=15>{0}</font>'.format(content['caption'].strip())
                        story.append(Paragraph(caption_text, styles['Italic']))
                        story.append(Spacer(1, 10))
                        
##                    story.append(PageBreak())

                story.append(Spacer(1, 10))
                    
                if 'table' in content:
                    
                    if content.get('caption', None) is not None:
                        caption_text = '<font size=15>{0}</font>'.format(content['caption'].strip())
                        story.append(Paragraph(caption_text, styles['Italic']))
                        story.append(Spacer(1, 10))
                                        
                    _t = self.build_table(content['table'])
                    story.append(_t)
                                           
##                    story.append(PageBreak())
                    
                if 'text' in content:
                    for para in content['text']:
                        story.append(Paragraph(para, styles['Normal']))
                        story.append(Spacer(1, 12))
                        
##                    story.append(PageBreak())
                    
            story.append(PageBreak())
            
        doc.build(story,onFirstPage=self.pageHeadFoot, onLaterPages=self.pageHeadFoot)
        body_matter = pyPdf.PdfFileReader(working_file)
        for page in range(body_matter.getNumPages()):
            pdf_writer.addPage(body_matter.getPage(page))
        try:
            os.remove(working_file.name)
        except OSError: # Windows reports file in use, other OS errors, etc.
            pass
        if self.end_matter is not None:
            end_matter = pyPdf.PdfFileReader(file(self.end_matter, "rb"))
            for page in range(end_matter.getNumPages()):
                pdf_writer.addPage(end_matter.getPage(page))
        output_stream = file(self.output_filename, "wb")
        pdf_writer.write(output_stream)
        
        output_stream.close()