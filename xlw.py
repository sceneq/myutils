from __future__ import annotations

# pywintypes.com_error: (-2147352567, '例外が発生しました。', (0, 'Microsoft Excel', "マクロ ''e5489931.xlsm'!Sheet1!go' を実行できません。このブックでマクロが使用できないか、またはすべてのマクロが無効になっている可能性があります。", 'xlmain11.chm', 0, -2146827284), None)
# The macro may not be available in this workbook or all macros may be disabled

import xlwings as xw
import sys
from pathlib import Path
import os
from datetime import datetime

# from xlwings import cli
# cli.main() のコピペ

def export_vba_modules(book: xw.Book, overwrite=False) -> dict[str, int]:
    # TODO: catch error when Trust Access to VBA Object model isn't enabled
    # TODO: raise error if editing while file hashes differ
    type_to_ext = {100: "cls", 1: "bas", 2: "cls", 3: "frm"}
    path_to_type = {}
    for vb_component in book.api.VBProject.VBComponents:
        file_path = (
            Path(".").resolve()
            / f"{vb_component.Name}.{type_to_ext[vb_component.Type]}"
        )
        path_to_type[str(file_path)] = vb_component.Type
        if (
            vb_component.Type == 100 and vb_component.CodeModule.CountOfLines > 0
        ) or vb_component.Type != 100:
            # Prevents cluttering everything with empty files if you have lots of sheets
            if overwrite or not file_path.exists():
                vb_component.Export(str(file_path))
                if vb_component.Type == 100:
                    # Remove the meta info so it can be distinguished from regular
                    # classes when running "xlwings vba import"
                    with open(file_path, "r", encoding="cp932") as f:
                        exported_code = f.readlines()
                    with open(file_path, "w", encoding="cp932") as f:
                        f.writelines(exported_code[9:])
    return path_to_type

def vba_get_book(args):
    if args and args.file:
        book = xw.Book(args.file)
    else:
        if not xw.apps:
            sys.exit(
                "Your workbook must be open or you have to supply the --file argument."
            )
        else:
            book = xw.books.active
    return book

def vba_edit(args):
    import pywintypes
    from watchgod import watch, RegExpWatcher, Change

    book = vba_get_book(args)

    path_to_type = export_vba_modules(book, overwrite=False)
    mode = "verbose" if args.verbose else "silent"

    print(f"NOTE: Deleting a VBA module here will also delete it in the VBA editor!")
    print(f"Watching for changes in {book.name} ({mode} mode)...(Hit Ctrl-C to stop)")

    for changes in watch(
        Path(".").resolve(),
        watcher_cls=RegExpWatcher,
        watcher_kwargs=dict(re_files=r"^.*(\.cls|\.frm|\.bas)$"),
        normal_sleep=400,
    ):
        for change_type, path in changes:
            module_name = os.path.splitext(os.path.basename(path))[0]
            module_type = path_to_type[path]
            vb_component = book.api.VBProject.VBComponents(module_name)
            if change_type == Change.modified:
                with open(path, "r") as f:
                    vba_code = f.readlines()
                line_count = vb_component.CodeModule.CountOfLines
                if line_count > 0:
                    vb_component.CodeModule.DeleteLines(1, line_count)
                # ThisWorkbook/Sheet, bas, cls, frm
                type_to_firstline = {100: 0, 1: 1, 2: 9, 3: 15}
                try:
                    vb_component.CodeModule.AddFromString(
                        "".join(vba_code[type_to_firstline[module_type] :])
                    )
                    print("applied", datetime.now().replace(microsecond=0))
                except pywintypes.com_error:
                    print(
                        f"ERROR: Couldn't update module {module_name}. "
                        f"Please update changes manually."
                    )
                if args.verbose:
                    print(f"INFO: Updated module {module_name}.")
            elif change_type == Change.deleted:
                try:
                    book.api.VBProject.VBComponents.Remove(vb_component)
                    print("deleted")
                except pywintypes.com_error:
                    print(
                        f"ERROR: Couldn't delete module {module_name}. "
                        f"Please delete it manually."
                    )
            elif change_type == Change.added:
                print(
                    f"ERROR: Couldn't add {module_name} as this isn't supported. "
                    "Please add new files via the VBA Editor."
                )
            book.save()

from dataclasses import dataclass
@dataclass
class VbaEditArgs:
    file: str
    verbose = False

if sys.argv[1] == "watch":
    vba_edit(VbaEditArgs(file=sys.argv[2]))
elif sys.argv[1] == "run":
    wb = xw.Book(sys.argv[2])
    name = sys.argv[3]
    wb.macro(name)()
else:
    print("fallback")
    from xlwings import cli
    cli.main()
