"""Inspect the included presentation structure without claiming an implemented system."""
from pathlib import Path
import json
from xml.etree import ElementTree as ET
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'AI_Assisted_Mechanical_Design_Proposal.pptx'
with ZipFile(source) as z:
    assert z.testzip() is None
    names=sorted(n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml'))
    assert names, 'Presentation has no slides'
    texts=[]
    for name in names:
        node=ET.fromstring(z.read(name))
        texts.append({'slide_xml':name,'text_runs':len(node.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t'))})
result={'artifact':source.name,'slide_count':len(names),'scope':'Presentation structure checked; no CAD integration or ROI validation performed','slides':texts}
output=ROOT/'reports/artifact_check.json';output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps(result,indent=2)+'\n')
print(f'Valid PPTX archive with {len(names)} slides; concept only.')
