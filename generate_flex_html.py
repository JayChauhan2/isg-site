from collections import OrderedDict
from html import escape
from pathlib import Path
from re import findall
from zipfile import ZipFile
from xml.etree import ElementTree as ET

SOURCE = Path('/Users/jaychauhan/Downloads/ISC instructors Sp26.xlsx')
OUTPUT = Path('/Users/jaychauhan/isg-site/spring_2026_flex.html')
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

# Official-style department labels for the subject prefixes in the workbook.
DEPARTMENTS = {
    'AAS': 'Asian American Studies', 'ABE': 'Agricultural and Biological Engineering',
    'ACCY': 'Accountancy', 'ACE': 'Agr & Consumer Economics', 'ACES': 'Agr, Consumer, & Env Sciences',
    'ADV': 'Advertising', 'AE': 'Aerospace Engineering', 'AFAS': 'Air Force Aerospace Studies',
    'AFRO': 'African American Studies', 'AGCM': 'Agricultural Comm Pgm & Crse',
    'AIS': 'American Indian Studies Prgrm', 'ALEC': 'Agricultural Leadership, Education, and Communications Program',
    'ANSC': 'Animal Sciences', 'ANTH': 'Anthropology', 'ARAB': 'Arabic', 'ARCH': 'Architecture',
    'ART': 'Art', 'ARTD': 'Art--Design', 'ARTE': 'Art--Education', 'ARTF': 'Art--Foundation',
    'ARTH': 'Art--History', 'ARTJ': 'Japan House', 'ARTS': 'Art--Studio',
    'ASRM': 'Actuarial Science and Risk Management', 'ASTR': 'Astronomy', 'ATMS': 'Atmospheric Sciences',
    'BADM': 'Business Administration', 'BASQ': 'Basque', 'BCOG': 'Brain and Cognitive Science',
    'BDI': 'Business Data and Innovation', 'BIOC': 'Biochemistry', 'BIOE': 'Bioengineering',
    'BTW': 'Business and Technical Writing', 'BUS': 'Business', 'CB': 'Chemical Biology',
    'CEE': 'Civil and Environmental Engineering', 'CGGE': 'Comparative & Global Gender Studies',
    'CHBE': 'Chemical and Biomolecular Engineering', 'CHEM': 'Chemistry', 'CHIN': 'Chinese',
    'CHP': 'Campus Honors Program', 'CI': 'Curriculum and Instruction', 'CLCV': 'Classical Civilization',
    'CMN': 'Communication', 'CPSC': 'Crop Sciences', 'CS': 'Computer Science',
    'CSE': 'Computational Science and Engineering', 'CW': 'Creative Writing', 'CWL': 'Comparative and World Literature',
    'DANC': 'Dance', 'EALC': 'East Asian Languages and Cultures', 'ECE': 'Electrical and Computer Engineering',
    'ECON': 'Economics', 'EDUC': 'Education', 'EIL': 'English as an International Language',
    'ENG': 'Engineering', 'ENGL': 'English', 'ENVS': 'Environmental Studies',
    'EPOL': 'Education Policy, Organization and Leadership', 'EPSY': 'Educational Psychology',
    'ERAM': 'Education Research and Methods', 'ESE': 'Earth, Society, and Environmental Sustainability',
    'ESL': 'English as a Second Language', 'ETMA': 'Engineering Technology and Management for Agricultural Systems', 'EXP': 'EXP',
    'FAA': 'Fine and Applied Arts', 'FIN': 'Finance', 'FR': 'French',
    'FSHN': 'Food Science and Human Nutrition', 'GC': 'General Curriculum', 'GEOL': 'Geology',
    'GER': 'German', 'GGIS': 'Geography & Geographic Information Science', 'GLBL': 'Global Studies',
    'GRK': 'Greek', 'GRKM': 'Greek (Modern)', 'GSD': 'Game Studies and Design',
    'GWS': "Gender and Women's Studies", 'HDFS': 'Human Development and Family Studies',
    'HIST': 'History', 'HK': 'Health and Kinesiology', 'HORT': 'Horticulture', 'HT': 'Health Technology',
    'IB': 'Integrative Biology', 'IE': 'Industrial Engineering', 'INFO': 'Illinois Informatics Institute',
    'IS': 'Information Sciences', 'ITAL': 'Italian', 'JAPN': 'Japanese', 'JOUR': 'Journalism',
    'KOR': 'Korean', 'LA': 'Landscape Architecture', 'LAS': 'Liberal Arts and Sciences',
    'LAST': 'Latin American and Caribbean Studies', 'LAT': 'Latin', 'LAW': 'Law', 'LEAD': 'Leadership',
    'LER': 'Labor and Employment Relations', 'LING': 'Linguistics', 'LLS': 'Latina/Latino Studies',
    'MACS': 'Media and Cinema Studies', 'MATH': 'Mathematics', 'MBA': 'MBA Program',
    'MCB': 'Molecular and Cellular Biology', 'ME': 'Mechanical Engineering', 'MILS': 'Military Science',
    'MSE': 'Materials Science and Engineering', 'MUS': 'Music', 'MUSC': 'Music', 'MUSE': 'Museum Studies',
    'NE': 'NE', 'NPRE': 'Nuclear, Plasma, and Radiological Engineering',
    'NRES': 'Natural Resources and Environmental Sciences', 'NUTR': 'Nutrition', 'PATH': 'Pathobiology',
    'PHIL': 'Philosophy', 'PHYS': 'Physics', 'POL': 'Polish', 'PORT': 'Portuguese',
    'PS': 'Political Science', 'PSYC': 'Psychology', 'REES': 'Russian, East European, and Eurasian Studies',
    'REL': 'Religion', 'RHET': 'Rhetoric', 'RST': 'Recreation, Sport, and Tourism', 'RUSS': 'Russian',
    'SAME': 'South Asian and Middle Eastern Studies', 'SBC': 'Strategic Brand Communication', 'SCAN': 'Scandinavian',
    'SE': 'Systems Engineering and Design', 'SHS': 'Speech and Hearing Science', 'SLAV': 'Slavic',
    'SLCL': 'School of Literatures, Cultures, and Linguistics', 'SOC': 'Sociology', 'SOCW': 'Social Work', 'SPAN': 'Spanish',
    'SPED': 'Special Education', 'STAT': 'Statistics', 'TAM': 'Theoretical and Applied Mechanics',
    'TE': 'Technology Entrepreneur Ctr', 'THEA': 'Theatre', 'TRST': 'Translation Studies', 'TURK': 'Turkish',
    'UP': 'Urban & Regional Planning', 'VCM': 'Vet Clinical Medicine', 'VM': 'Veterinary Medicine',
}


def workbook_rows():
    with ZipFile(SOURCE) as book:
        shared_root = ET.fromstring(book.read('xl/sharedStrings.xml'))
        shared = [''.join(t.text or '' for t in item.findall('.//m:t', NS))
                  for item in shared_root.findall('m:si', NS)]
        sheet = ET.fromstring(book.read('xl/worksheets/sheet1.xml'))
        for row in sheet.findall('.//m:sheetData/m:row', NS)[1:]:
            values = {}
            for cell in row.findall('m:c', NS):
                value = cell.find('m:v', NS)
                text = '' if value is None else value.text
                if cell.get('t') == 's' and text:
                    text = shared[int(text)]
                values[cell.get('r')[0]] = text
            yield values


def main():
    departments = {}
    for row in workbook_rows():
        course = row.get('B', '')
        # The first subject is the controlling department.  Retain every course
        # number in a joint listing (for example, SPED 526 / SPED 566) while
        # keeping the entry in that controlling department only.
        course_codes = findall(r'([A-Z]+)\s+(\d+)', course.split(',', 1)[0])
        if not course_codes:
            raise ValueError(f'Could not parse course: {course}')
        code, _ = course_codes[0]
        department = DEPARTMENTS.get(code, code)
        given = row.get('D', '')
        family = row.get('E', '')
        name = family if given in ('', '-') else f"{family}, {given[:1]}"
        role = 'TA' if row.get('G') == 'TA' else 'Instructor'
        # NetID is used only as an internal grouping key: it prevents people
        # who share the same public "Family, G" display name from being merged.
        # It is never written to the generated public HTML.
        netid = row.get('F', '')
        key = (netid, name, role)
        courses = departments.setdefault(department, OrderedDict()).setdefault(key, [])
        courses.extend(int(number) for _, number in course_codes)

    blocks = [
        '<details class="season-block" open="">',
        '    <summary>Spring 2026</summary>',
        '    <div class="season-content">',
        '        <p class="note">',
        '            (Based on Data Collected Spring 2026)<br>',
        '            Instructors\' names are listed by course number (ascending) within each department. &nbsp;<strong>T.A.</strong> indicates Teaching Assistant.',
        '        </p>',
    ]
    for department in sorted(departments):
        people = departments[department]
        # Match the Fall 2025 convention: when the course number ties, sort
        # alphabetically by displayed name.  NetID makes identical display
        # names deterministic without exposing it publicly.
        ordered = sorted(people.items(), key=lambda item: (min(item[1]), item[0][1].casefold(), item[0][0].casefold()))
        lines = []
        for (_, name, role), courses in ordered:
            course_list = ', '.join(str(number) for number in sorted(set(courses)))
            marker = 'T.A. ' if role == 'TA' else ''
            lines.append(f'{escape(name)} - {marker}{course_list}')
        blocks.append('        <details>')
        blocks.append(f'            <summary style="cursor:pointer;font-size:14px;padding:2px 8px;"><strong>{escape(department)}</strong></summary>')
        blocks.append('            <p style="font-size:14px;line-height:1.6;margin:5px 0;padding-left:20px;">')
        for index, line in enumerate(lines):
            suffix = '<br>' if index < len(lines) - 1 else ''
            blocks.append(f'                {line}{suffix}')
        blocks.extend(['            </p>', '        </details>'])
    blocks.extend(['    </div>', '</details>', ''])
    OUTPUT.write_text('\n'.join(blocks), encoding='utf-8')
    print(f'Wrote {OUTPUT} with {len(departments)} departments.')


if __name__ == '__main__':
    main()
