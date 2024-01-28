from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import BaseDocTemplate, PageTemplate
import json

def json_to_pdf(file_path, pdf_file, header):
    # Load data from the JSON file
    with open(file_path) as file:
        data = json.load(file)

    # Create a PDF document with two columns
    doc = BaseDocTemplate(pdf_file, pagesize=letter, rightMargin=60, leftMargin=60, topMargin=72, bottomMargin=18)

    # Define two columns
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2')

    two_column_layout = PageTemplate(frames=[frame1, frame2])
    doc.addPageTemplates([two_column_layout])

    # Get and modify styles
    styles = getSampleStyleSheet()
    styles['Heading1'].fontSize = 12 
    styles['Heading2'].fontSize = 9
    styles['BodyText'].fontSize = 6
    styles['Heading1'].fontName = 'Courier'
    styles['Heading2'].fontName = 'Courier'
    styles['Heading1'].alignment = TA_CENTER

    styles['BodyText'].fontName = 'Courier'
    styles.add(ParagraphStyle(name='DayTotalFootage', parent=styles['Heading1'], alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='TotalBoardFootage', parent=styles['Heading1'], fontSize=14, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='HeaderInfo', fontSize=14, alignment=TA_CENTER))

    # Prepare a list to hold our PDF elements (e.g., paragraphs)
    elements = []

    # Loop through the data
    for day, day_info in data.items():
        # Day header and total footage at the top, centered
        elements.append(Paragraph(f"Day {day} | Date: {day_info['date']}", styles['Heading1']))
        elements.append(Paragraph(f"Total for Day {day}: {day_info['total_day_footage']} BF", styles['DayTotalFootage']))
        elements.append(Spacer(1, 12))
        # Loop through each tree
        for tree, tree_info in day_info['trees'].items():
            original_logs = ', '.join([str(log) for log in tree_info['original_logs']])
            elements.append(Paragraph(f"{tree.upper()}: [{original_logs}]", styles['Heading2']))

            # Loop through each log
            for log, log_info in tree_info['logs_info'].items():
                elements.append(Paragraph(
                    f"{log:6} - Diameter: {log_info['diameter']:<2}\" | Length {log_info['length']:<2}' | Taper {log_info['taper']:<3} ->   [{log_info['footage']:<4} BF]", styles['BodyText']))
            elements.append(Paragraph(
                f"        >>> Total for this tree: [{tree_info['total_footage']:<4} BF] <<<", styles['BodyText']))

        elements.append(PageBreak())  # Break after each day for simplicity; adjust as needed

    # Add final page with header information
    elements.append(Paragraph(f"Total Board Footage: {header['total_board_footage']}", styles['TotalBoardFootage']))
    elements.append(Spacer(1, 24))

    # Create two separate lists for totals and averages, and then combine them into a table
    totals = [f"Total Days: {header['total_days']}", f"Total Trees: {header['total_trees']}", f"Total Logs: {header['total_logs']}"]
    averages = [f"Average Tree Footage: {header['average_tree_footage']}", f"Average Logs/Tree: {header['average_logs_per_tree']}"]
    totals_paragraphs = [Paragraph(text, styles['BodyText']) for text in totals]
    averages_paragraphs = [Paragraph(text, styles['BodyText']) for text in averages]
    table_data = [[totals_paragraphs[i] if i < len(totals_paragraphs) else '', averages_paragraphs[i] if i < len(averages_paragraphs) else ''] for i in range(max(len(totals), len(averages)))]

    table = Table(table_data)
    table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT')]))
    elements.append(table)

    # Add total count of each log length
    elements.append(Spacer(1, 24))
    log_count_data = [[Paragraph(f"{length}: {count}", styles['BodyText']) for length, count in header['total_count_of_each_log_length'].items()]]
    log_count_table = Table(log_count_data)
    log_count_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
    elements.append(log_count_table)

    # Build the PDF file
    doc.build(elements)

# example usage

