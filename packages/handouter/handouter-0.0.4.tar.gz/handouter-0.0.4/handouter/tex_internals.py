HEADER = r"""
\documentclass{minimal}
\usepackage[paperwidth=210mm,paperheight=297mm,top=5mm,bottom=5mm,left=5mm,right=5mm]{geometry}
\usepackage{polyglossia}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{calc}
\usepackage[document]{ragged2e}
\setmainfont{Arial}
\newlength{\boxwidth}
\newlength{\boxwidthinner}
\begin{document}
\fontsize{14pt}{16pt}\selectfont
\setlength\parindent{0pt}
\tikzstyle{box}=[draw, dashed, rectangle, inner sep=1mm]
\raggedright
\raggedbottom
""".strip()

GREYTEXT = r"""{\fontsize{9pt}{11pt}\selectfont \textcolor{gray}{<GREYTEXT>}}"""

GREYTEXT_LANGS = {
    "by": "Да пытаньня {}",
    "en": "Handout for question {}",
    "kz": "{}-сұрақтың үлестіру материалы",
    "ru": "К вопросу {}",
    "sr": "Materijal za deljenje uz pitanje {}",
    "ua": "До запитання {}",
    "uz": "{} саволга тарқатма материал",
}

TIKZBOX_START = r"""{<CENTERING><FONTSIZE>
"""

TIKZBOX_INNER = r"""
\begin{tikzpicture}
\node[box, minimum width=\boxwidth<TEXTWIDTH><ALIGN>] {<CONTENTS>};
\end{tikzpicture}
""".strip()

TIKZBOX_END = "\n}"

IMG = r"""\includegraphics<IMGWIDTH>{<IMGPATH>}"""

IMGWIDTH = r"[width=<QWIDTH>\textwidth]"
