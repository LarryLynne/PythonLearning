import os
import sys
import shutil


folders = {"archives": [], "video": [], "audio": [], "documents": [], "images": []}
file_types = {
    'JPEG': "images", 'PNG': "images", 'JPG': "images", 'SVG': "images",
    'AVI': "video", 'MP4': "video", 'MOV': "video", 'MKV': "video",
    'DOC': "documents", 'DOCX': "documents", 'TXT': "documents", 'PDF': "documents", 'XLSX': "documents",
    'PPTX': "documents",
    'MP3': "audio", 'OGG': "audio", 'WAV': "audio", 'AMR': "audio", 'FLAC': "audio",
    'ZIP': "archives", 'GZ': "archives", 'TAR': "archives", 'RAR': "archives"
}


def translate(name: str) -> str:
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    res = ""
    res = name.translate(TRANS)
    return res


def get_file_ext(filename: str) -> str:
    parts = filename.split(".")
    return parts[len(parts) - 1]


def normalize(filename: str) -> str:
    ext = get_file_ext(filename)
    f_name = os.path.basename(filename)
    f_name = translate(f_name).replace("." + get_file_ext(filename), "")
    for fn in f_name:
        n = ord(fn)
        if n < 48 or 57 < n < 65 or 90 < n < 97 or n > 122:
            f_name = f_name.replace(fn, "_")
    return f_name + "." + ext


def create_folders(path: str):
    for folder in folders:
        p = os.path.join(path, folder)
        if not os.path.exists(p):
            os.mkdir(p)


def scan_dir(path: str) -> []:
    files = os.listdir(path)
    i = 0
    while i < len(files):
        files[i] = os.path.join(path, files[i])
        i += 1
    files1 = []
    for file in files:
        if os.path.isdir(file) and folders.get(os.path.basename(file)) is None:
            files1 += scan_dir(file)
    return files + files1


def print_files(files: []):
    known_exts = []
    unknown_exts = []
    for file in files:
        if os.path.isfile(file):
            ext = get_file_ext(file)
            filetype = file_types.get(ext.upper())
            files_by_type = folders.get(filetype)
            if files_by_type is not None:
                files_by_type.append(os.path.basename(file))
                if known_exts.count(ext) == 0:
                    known_exts.append(ext)
            else:
                if unknown_exts.count(ext) == 0:
                    unknown_exts.append(ext)
    files_by_cat = ""
    for k in folders.keys():
        if len(folders.get(k)) > 0:
            files_by_cat += k + ": \n"
            for v in folders.get(k):
                files_by_cat += "\t" + v + "\n"
    print(files_by_cat)
    kn_res = ""
    if len(known_exts) > 0:
        kn_res = "Known extentions:\n"
        for kn in known_exts:
            kn_res += "\t" + kn + "\n"
    print(kn_res)
    u_res = ""
    if len(unknown_exts) > 0:
        u_res = "Unknown extentions:\n"
        for u in unknown_exts:
            u_res += "\t" + u + "\n"
    print(u_res)


def sort_files(files: [str], path: str):
    create_folders(path)
    for file in files:
        if os.path.isdir(file):
            r = list(folders.keys())
            if not os.listdir(file) and r.count(os.path.basename(file)) == 0:
                os.remove(file)
        else:
            file_type = file_types.get(get_file_ext(file).upper())
            if file_type is not None:
                if file_type == "archives":
                    shutil.unpack_archive(file, os.path.join(path, file_type, normalize(os.path.basename(file)).replace(get_file_ext(file), "")))
                    os.remove(file)
                else:
                    os.replace(file, os.path.join(path, file_type, normalize(os.path.basename(file))))


def run():
    if sys.argv[0] == "":
        print("There is no args. Goodbye!")
    else:
        pt = sys.argv[1]
        files = scan_dir(pt)
        print_files(files)
        sort_files(files, pt)


if __name__ == "__main__":
    for param in sys.argv:
        print(param)
    run()
