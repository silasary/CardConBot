import yaml
import re
from typing import Optional

class Writeup():
    def __init__(self, filename: str) -> None:
        self.filename = filename
        with open(filename) as f:
            self.text = f.read()
            post = self.text.split('---', 2)
            self.yaml = yaml.safe_load(post[1])
            # self.yaml = docs.__next__()
            self.sections = post[2].split('* * *')

    def save(self) -> None:
        with open(self.filename, 'w') as f:
            f.write('---\n')
            yaml.dump(self.yaml, f)
            f.write('---')
            f.write('* * *'.join(self.sections))

    @property
    def title(self) -> str:
        return self.yaml['title']

    @property
    def prompt(self) -> Optional[str]:
        return self.yaml.get('prompt')

    @property
    def imgdir(self) -> str:
        val = self.yaml.get('imgdir')
        if val is None:
            val = re.sub(r'\W+', '', self.title).lower()
            self.yaml['imgdir'] = val
            self.save()
        return val

    def get_section_index(self, userid) -> int:
        i = 0
        for s in self.sections:
            if str(userid) in s:
                return i
            i = i + 1
        return -1
