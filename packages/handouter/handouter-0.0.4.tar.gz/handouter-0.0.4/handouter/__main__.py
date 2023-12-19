#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import shutil
import subprocess
import sys

from pecheny_utils import install_tectonic, get_tectonic_path
from handouter.tex_internals import (
    GREYTEXT,
    GREYTEXT_LANGS,
    HEADER,
    IMG,
    IMGWIDTH,
    TIKZBOX_END,
    TIKZBOX_INNER,
    TIKZBOX_START,
)


def read_file(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        contents = f.read()
    return contents


def write_file(filepath, contents):
    with open(filepath, "w", encoding="utf8") as f:
        f.write(contents)


def replace_ext(filepath, new_ext):
    if not new_ext.startswith("."):
        new_ext = "." + new_ext
    dirname = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    base, _ = os.path.splitext(basename)
    return os.path.join(dirname, base + new_ext)


class HandoutGenerator:
    RESERVED_WORDS = [
        "image",
        "for_question",
        "columns",
        "rows",
        "resize_image",
        "font_size",
        "no_center",
    ]

    def __init__(self, args):
        self.args = args
        self.blocks = [HEADER]

    def wrap_val(self, key, val):
        if key in ("columns", "rows", "no_center"):
            return int(val.strip())
        if key in ("resize_image", "font_size"):
            return float(val.strip())
        return val.strip()

    def parse_input(self, filepath):
        contents = read_file(filepath)
        blocks = contents.split("\n---\n")
        result = []
        for block_ in blocks:
            block = block_.strip()
            block_dict = {}
            text = []
            lines = block.split("\n")
            for line in lines:
                sp = line.split(":", 1)
                if sp[0] in self.RESERVED_WORDS:
                    block_dict[sp[0]] = self.wrap_val(sp[0], sp[1])
                else:
                    text.append(line.strip())
            if text:
                block_dict["text"] = "\linebreak\n".join(text)
            result.append(block_dict)
        return result

    def generate_for_question(self, question_num):
        return GREYTEXT.replace(
            "<GREYTEXT>", GREYTEXT_LANGS[self.args.lang].format(question_num)
        )

    def make_tikzbox(self, block):
        if block.get("no_center"):
            align = ""
        else:
            align = ", align=center"
        textwidth = ", text width=\\boxwidthinner"
        return (
            TIKZBOX_INNER.replace("<CONTENTS>", block["contents"])
            .replace("<PT>", str(8 * block["columns"] - 1))
            .replace("<ALIGN>", align)
            .replace("<TEXTWIDTH>", textwidth)
        )

    def generate_regular_block(self, block_):
        block = block_.copy()
        if bool(block.get("image")) == bool(block.get("text")):
            print(
                f"error in block {block}: exactly one of (image, text) should be present",
                file=sys.stderr,
            )
            sys.exit(1)
        boxwidth = round((198 - (block["columns"] - 1) * 1.5)/ block["columns"], 1)
        boxwidthinner = boxwidth - 2
        header = [
            r"\setlength{\boxwidth}{<Q>mm}%".replace("<Q>", str(boxwidth)),
            r"\setlength{\boxwidthinner}{<Q>mm}%".replace("<Q>", str(boxwidthinner)),
        ]
        rows = []
        if block.get("image"):
            img_qwidth = block.get("resize_image") or 1.0
            imgwidth = IMGWIDTH.replace("<QWIDTH>", str(img_qwidth))
            block["contents"] = IMG.replace("<IMGPATH>", block["image"]).replace(
                "<IMGWIDTH>", imgwidth
            )
        else:
            block["contents"] = block["text"]
        if block.get("no_center"):
            block["centering"] = ""
        else:
            block["centering"] = "\\centering"
        if block.get("font_size"):
            fs = block["font_size"]
            block["fontsize"] = "\\fontsize{FSpt}{LHpt}\\selectfont".replace(
                "FS", str(fs)
            ).replace("LH", str(fs + 2))
        else:
            block["fontsize"] = ""
        for _ in range(block.get("rows") or 1):
            row = (
                TIKZBOX_START.replace("<CENTERING>", block["centering"]).replace(
                    "<FONTSIZE>", block["fontsize"]
                )
                + "\n".join([self.make_tikzbox(block)] * block["columns"])
                + TIKZBOX_END
            )
            rows.append(row)
        return "\n".join(header) + "\n" + "\n\n\\vspace{1mm}\n\n".join(rows)

    def generate(self):
        for block in self.parse_input(self.args.filename):
            if self.args.debug:
                print(block)
            if block.get("for_question"):
                self.blocks.append(self.generate_for_question(block["for_question"]))
            elif block["columns"]:
                self.blocks.append(self.generate_regular_block(block))
        self.blocks.append("\\end{document}")
        return "\n\n".join(self.blocks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file with description")
    parser.add_argument("--lang", default="ru")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--compress", action="store_true")
    args = parser.parse_args()

    tex_contents = HandoutGenerator(args).generate()
    file_dir = os.path.dirname(os.path.abspath(args.filename))
    bn, _ = os.path.splitext(os.path.basename(args.filename))

    tex_path = os.path.join(file_dir, f"{bn}_{args.lang}.tex")
    write_file(tex_path, tex_contents)
    tectonic_path = get_tectonic_path()
    if not tectonic_path:
        print("tectonic is not present, installing it...")
        install_tectonic()
        tectonic_path = get_tectonic_path()
    if not tectonic_path:
        raise Exception("tectonic couldn't be installed successfully :(")
    if args.debug:
        print(f"tectonic found at `{tectonic_path}`")

    subprocess.run([tectonic_path, os.path.basename(tex_path)], check=True, cwd=file_dir)

    output_file = replace_ext(tex_path, "pdf")

    if args.compress:
        print(f"compressing {output_file}")
        size_before = round(os.stat(output_file).st_size / 1024)
        output_file_compressed = output_file[:-4] + ".compressed.pdf"
        subprocess.run(
            [
                "gs",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.5",
                "-dPDFSETTINGS=/default",
                "-dNOPAUSE",
                "-dQUIET",
                "-dBATCH",
                f"-sOutputFile={output_file_compressed}",
                output_file,
            ],
            check=True,
        )
        shutil.move(output_file_compressed, output_file)
        size_after = round(os.stat(output_file).st_size / 1024)
        q = round(size_after / size_before, 1)
        print(f"before: {size_before}kb, after: {size_after}kb, compression: {q}")

    print(f"Output file: {output_file}")

    if not args.debug:
        os.remove(tex_path)


if __name__ == "__main__":
    main()
