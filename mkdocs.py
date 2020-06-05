from docstr_md.python import PySoup, compile_md
from docstr_md.src_href import Github

src_href = Github('https://github.com/dsbowen/sqlalchemy-orderingitem')

path = 'sqlalchemy_orderingitem/__init__.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
compile_md(soup, compiler='sklearn', outfile='docs_md/use.md')