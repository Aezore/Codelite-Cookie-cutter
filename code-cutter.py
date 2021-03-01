""" Creates a workable Codelite Workspace and project from folder name """
import argparse
import base64
import xml.etree.ElementTree as ET
from pathlib import Path

PR_SAMPLE = b"PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPENvZGVMaXRlX1Byb2plY3QgTmFtZT0iVU9DX1ByYWN0MCIgSW50ZXJuYWxUeXBlPSJDb25zb2xlIiBWZXJzaW9uPSIxMTAwMCI+CiAgPFBsdWdpbnM+CiAgICA8UGx1Z2luIE5hbWU9InFtYWtlIj4KICAgICAgPCFbQ0RBVEFbMDAwMTAwMDFOMDAwN1JlbGVhc2UwMDAwMDAwMDAwMDBdXT4KICAgIDwvUGx1Z2luPgogIDwvUGx1Z2lucz4KICA8RGVzY3JpcHRpb24vPgogIDxEZXBlbmRlbmNpZXMvPgogIDxWaXJ0dWFsRGlyZWN0b3J5IE5hbWU9ImluY2x1ZGUiPgogICAgPEZpbGUgTmFtZT0iaW5jbHVkZS9tYWluLmgiLz4KICA8L1ZpcnR1YWxEaXJlY3Rvcnk+CiAgPFZpcnR1YWxEaXJlY3RvcnkgTmFtZT0ic3JjIj4KICAgIDxGaWxlIE5hbWU9InNyYy9tYWluLmMiLz4KICA8L1ZpcnR1YWxEaXJlY3Rvcnk+CiAgPFNldHRpbmdzIFR5cGU9IkV4ZWN1dGFibGUiPgogICAgPEdsb2JhbFNldHRpbmdzPgogICAgICA8Q29tcGlsZXIgT3B0aW9ucz0iIiBDX09wdGlvbnM9IiIgQXNzZW1ibGVyPSIiPgogICAgICAgIDxJbmNsdWRlUGF0aCBWYWx1ZT0iLiIvPgogICAgICA8L0NvbXBpbGVyPgogICAgICA8TGlua2VyIE9wdGlvbnM9IiI+CiAgICAgICAgPExpYnJhcnlQYXRoIFZhbHVlPSIuIi8+CiAgICAgIDwvTGlua2VyPgogICAgICA8UmVzb3VyY2VDb21waWxlciBPcHRpb25zPSIiLz4KICAgIDwvR2xvYmFsU2V0dGluZ3M+CiAgICA8Q29uZmlndXJhdGlvbiBOYW1lPSJEZWJ1ZyIgQ29tcGlsZXJUeXBlPSJnbnUgZ2NjIiBEZWJ1Z2dlclR5cGU9IkdOVSBnZGIgZGVidWdnZXIiIFR5cGU9IkV4ZWN1dGFibGUiIEJ1aWxkQ21wV2l0aEdsb2JhbFNldHRpbmdzPSJhcHBlbmQiIEJ1aWxkTG5rV2l0aEdsb2JhbFNldHRpbmdzPSJhcHBlbmQiIEJ1aWxkUmVzV2l0aEdsb2JhbFNldHRpbmdzPSJhcHBlbmQiPgogICAgICA8Q29tcGlsZXIgT3B0aW9ucz0iLWc7LU8wOy1XYWxsOyAtV2Vycm9yIiBDX09wdGlvbnM9Ii1nOy1PMDstV2FsbDsgLVdlcnJvciIgQXNzZW1ibGVyPSIiIFJlcXVpcmVkPSJ5ZXMiIFByZUNvbXBpbGVkSGVhZGVyPSIiIFBDSEluQ29tbWFuZExpbmU9Im5vIiBQQ0hGbGFncz0iIiBQQ0hGbGFnc1BvbGljeT0iMCI+CiAgICAgICAgPEluY2x1ZGVQYXRoIFZhbHVlPSIuIi8+CiAgICAgICAgPEluY2x1ZGVQYXRoIFZhbHVlPSIuL2luY2x1ZGUiLz4KICAgICAgPC9Db21waWxlcj4KICAgICAgPExpbmtlciBPcHRpb25zPSIiIFJlcXVpcmVkPSJ5ZXMiPgogICAgICAgIDxMaWJyYXJ5UGF0aCBWYWx1ZT0iLi4vbGliIi8+CiAgICAgIDwvTGlua2VyPgogICAgICA8UmVzb3VyY2VDb21waWxlciBPcHRpb25zPSIiIFJlcXVpcmVkPSJubyIvPgogICAgICA8R2VuZXJhbCBPdXRwdXRGaWxlPSIuLi9iaW4vJChQcm9qZWN0TmFtZSkiIEludGVybWVkaWF0ZURpcmVjdG9yeT0iLi9EZWJ1ZyIgQ29tbWFuZD0iLi4vYmluLyQoUHJvamVjdE5hbWUpIiBDb21tYW5kQXJndW1lbnRzPSIiIFVzZVNlcGFyYXRlRGVidWdBcmdzPSJubyIgRGVidWdBcmd1bWVudHM9IiIgV29ya2luZ0RpcmVjdG9yeT0iLi4vYmluIiBQYXVzZUV4ZWNXaGVuUHJvY1Rlcm1pbmF0ZXM9InllcyIgSXNHVUlQcm9ncmFtPSJubyIgSXNFbmFibGVkPSJ5ZXMiLz4KICAgICAgPEJ1aWxkU3lzdGVtIE5hbWU9IkRlZmF1bHQiLz4KICAgICAgPEVudmlyb25tZW50IEVudlZhclNldE5hbWU9IiZsdDtVc2UgRGVmYXVsdHMmZ3Q7IiBEYmdTZXROYW1lPSImbHQ7VXNlIERlZmF1bHRzJmd0OyI+CiAgICAgICAgPCFbQ0RBVEFbXV0+CiAgICAgIDwvRW52aXJvbm1lbnQ+CiAgICAgIDxEZWJ1Z2dlciBJc1JlbW90ZT0ibm8iIFJlbW90ZUhvc3ROYW1lPSIiIFJlbW90ZUhvc3RQb3J0PSIiIERlYnVnZ2VyUGF0aD0iIiBJc0V4dGVuZGVkPSJubyI+CiAgICAgICAgPERlYnVnZ2VyU2VhcmNoUGF0aHMvPgogICAgICAgIDxQb3N0Q29ubmVjdENvbW1hbmRzLz4KICAgICAgICA8U3RhcnR1cENvbW1hbmRzLz4KICAgICAgPC9EZWJ1Z2dlcj4KICAgICAgPFByZUJ1aWxkLz4KICAgICAgPFBvc3RCdWlsZC8+CiAgICAgIDxDdXN0b21CdWlsZCBFbmFibGVkPSJubyI+CiAgICAgICAgPFJlYnVpbGRDb21tYW5kLz4KICAgICAgICA8Q2xlYW5Db21tYW5kLz4KICAgICAgICA8QnVpbGRDb21tYW5kLz4KICAgICAgICA8UHJlcHJvY2Vzc0ZpbGVDb21tYW5kLz4KICAgICAgICA8U2luZ2xlRmlsZUNvbW1hbmQvPgogICAgICAgIDxNYWtlZmlsZUdlbmVyYXRpb25Db21tYW5kLz4KICAgICAgICA8VGhpcmRQYXJ0eVRvb2xOYW1lPk5vbmU8L1RoaXJkUGFydHlUb29sTmFtZT4KICAgICAgICA8V29ya2luZ0RpcmVjdG9yeS8+CiAgICAgIDwvQ3VzdG9tQnVpbGQ+CiAgICAgIDxBZGRpdGlvbmFsUnVsZXM+CiAgICAgICAgPEN1c3RvbVBvc3RCdWlsZC8+CiAgICAgICAgPEN1c3RvbVByZUJ1aWxkLz4KICAgICAgPC9BZGRpdGlvbmFsUnVsZXM+CiAgICAgIDxDb21wbGV0aW9uIEVuYWJsZUNwcDExPSJubyIgRW5hYmxlQ3BwMTQ9Im5vIj4KICAgICAgICA8Q2xhbmdDbXBGbGFnc0MvPgogICAgICAgIDxDbGFuZ0NtcEZsYWdzLz4KICAgICAgICA8Q2xhbmdQUC8+CiAgICAgICAgPFNlYXJjaFBhdGhzLz4KICAgICAgPC9Db21wbGV0aW9uPgogICAgPC9Db25maWd1cmF0aW9uPgogICAgPENvbmZpZ3VyYXRpb24gTmFtZT0iUmVsZWFzZSIgQ29tcGlsZXJUeXBlPSJnbnUgZ2NjIiBEZWJ1Z2dlclR5cGU9IkdOVSBnZGIgZGVidWdnZXIiIFR5cGU9IkV4ZWN1dGFibGUiIEJ1aWxkQ21wV2l0aEdsb2JhbFNldHRpbmdzPSJhcHBlbmQiIEJ1aWxkTG5rV2l0aEdsb2JhbFNldHRpbmdzPSJhcHBlbmQiIEJ1aWxkUmVzV2l0aEdsb2JhbFNldHRpbmdzPSJhcHBlbmQiPgogICAgICA8Q29tcGlsZXIgT3B0aW9ucz0iLWc7LU8wOy1XYWxsOyAtV2Vycm9yIiBDX09wdGlvbnM9Ii1nOy1PMDstV2FsbDsgLVdlcnJvciIgQXNzZW1ibGVyPSIiIFJlcXVpcmVkPSJ5ZXMiIFByZUNvbXBpbGVkSGVhZGVyPSIiIFBDSEluQ29tbWFuZExpbmU9Im5vIiBQQ0hGbGFncz0iIiBQQ0hGbGFnc1BvbGljeT0iMCI+CiAgICAgICAgPEluY2x1ZGVQYXRoIFZhbHVlPSIuIi8+CiAgICAgICAgPEluY2x1ZGVQYXRoIFZhbHVlPSIuL2luY2x1ZGUiLz4KICAgICAgICA8SW5jbHVkZVBhdGggVmFsdWU9Ii4uL1Rlc3RMaWIvaW5jbHVkZSIvPgogICAgICAgIDxQcmVwcm9jZXNzb3IgVmFsdWU9Ik5ERUJVRyIvPgogICAgICA8L0NvbXBpbGVyPgogICAgICA8TGlua2VyIE9wdGlvbnM9IiIgUmVxdWlyZWQ9InllcyI+CiAgICAgICAgPExpYnJhcnlQYXRoIFZhbHVlPSIuLi9saWIiLz4KICAgICAgPC9MaW5rZXI+CiAgICAgIDxSZXNvdXJjZUNvbXBpbGVyIE9wdGlvbnM9IiIgUmVxdWlyZWQ9Im5vIi8+CiAgICAgIDxHZW5lcmFsIE91dHB1dEZpbGU9Ii4uL2Jpbi8kKFByb2plY3ROYW1lKSIgSW50ZXJtZWRpYXRlRGlyZWN0b3J5PSIuL1JlbGVhc2UiIENvbW1hbmQ9Ii4uL2Jpbi8kKFByb2plY3ROYW1lKSIgQ29tbWFuZEFyZ3VtZW50cz0iIiBVc2VTZXBhcmF0ZURlYnVnQXJncz0ibm8iIERlYnVnQXJndW1lbnRzPSIiIFdvcmtpbmdEaXJlY3Rvcnk9Ii4uL2JpbiIgUGF1c2VFeGVjV2hlblByb2NUZXJtaW5hdGVzPSJ5ZXMiIElzR1VJUHJvZ3JhbT0ibm8iIElzRW5hYmxlZD0ieWVzIi8+CiAgICAgIDxCdWlsZFN5c3RlbSBOYW1lPSJEZWZhdWx0Ii8+CiAgICAgIDxFbnZpcm9ubWVudCBFbnZWYXJTZXROYW1lPSImbHQ7VXNlIERlZmF1bHRzJmd0OyIgRGJnU2V0TmFtZT0iJmx0O1VzZSBEZWZhdWx0cyZndDsiPgogICAgICAgIDwhW0NEQVRBW11dPgogICAgICA8L0Vudmlyb25tZW50PgogICAgICA8RGVidWdnZXIgSXNSZW1vdGU9Im5vIiBSZW1vdGVIb3N0TmFtZT0iIiBSZW1vdGVIb3N0UG9ydD0iIiBEZWJ1Z2dlclBhdGg9IiIgSXNFeHRlbmRlZD0ibm8iPgogICAgICAgIDxEZWJ1Z2dlclNlYXJjaFBhdGhzLz4KICAgICAgICA8UG9zdENvbm5lY3RDb21tYW5kcy8+CiAgICAgICAgPFN0YXJ0dXBDb21tYW5kcy8+CiAgICAgIDwvRGVidWdnZXI+CiAgICAgIDxQcmVCdWlsZC8+CiAgICAgIDxQb3N0QnVpbGQvPgogICAgICA8Q3VzdG9tQnVpbGQgRW5hYmxlZD0ibm8iPgogICAgICAgIDxSZWJ1aWxkQ29tbWFuZC8+CiAgICAgICAgPENsZWFuQ29tbWFuZC8+CiAgICAgICAgPEJ1aWxkQ29tbWFuZC8+CiAgICAgICAgPFByZXByb2Nlc3NGaWxlQ29tbWFuZC8+CiAgICAgICAgPFNpbmdsZUZpbGVDb21tYW5kLz4KICAgICAgICA8TWFrZWZpbGVHZW5lcmF0aW9uQ29tbWFuZC8+CiAgICAgICAgPFRoaXJkUGFydHlUb29sTmFtZT5Ob25lPC9UaGlyZFBhcnR5VG9vbE5hbWU+CiAgICAgICAgPFdvcmtpbmdEaXJlY3RvcnkvPgogICAgICA8L0N1c3RvbUJ1aWxkPgogICAgICA8QWRkaXRpb25hbFJ1bGVzPgogICAgICAgIDxDdXN0b21Qb3N0QnVpbGQvPgogICAgICAgIDxDdXN0b21QcmVCdWlsZC8+CiAgICAgIDwvQWRkaXRpb25hbFJ1bGVzPgogICAgICA8Q29tcGxldGlvbiBFbmFibGVDcHAxMT0ibm8iIEVuYWJsZUNwcDE0PSJubyI+CiAgICAgICAgPENsYW5nQ21wRmxhZ3NDLz4KICAgICAgICA8Q2xhbmdDbXBGbGFncy8+CiAgICAgICAgPENsYW5nUFAvPgogICAgICAgIDxTZWFyY2hQYXRocy8+CiAgICAgIDwvQ29tcGxldGlvbj4KICAgIDwvQ29uZmlndXJhdGlvbj4KICA8L1NldHRpbmdzPgo8L0NvZGVMaXRlX1Byb2plY3Q+Cg=="
WS_SAMPLE = b"PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPENvZGVMaXRlX1dvcmtzcGFjZSBOYW1lPSJQcmFjdDAiIERhdGFiYXNlPSIiIFZlcnNpb249IjEwMDAwIj4KICA8UHJvamVjdCBOYW1lPSJVT0NfUHJhY3QwIiBQYXRoPSJVT0NfUHJhY3QwL1VPQ19QcmFjdDAucHJvamVjdCIgQWN0aXZlPSJZZXMiLz4KICA8QnVpbGRNYXRyaXg+CiAgICA8V29ya3NwYWNlQ29uZmlndXJhdGlvbiBOYW1lPSJEZWJ1ZyIgU2VsZWN0ZWQ9Im5vIj4KICAgICAgPEVudmlyb25tZW50Lz4KICAgICAgPFByb2plY3QgTmFtZT0iVU9DX1ByYWN0MCIgQ29uZmlnTmFtZT0iRGVidWciLz4KICAgIDwvV29ya3NwYWNlQ29uZmlndXJhdGlvbj4KICAgIDxXb3Jrc3BhY2VDb25maWd1cmF0aW9uIE5hbWU9IlJlbGVhc2UiIFNlbGVjdGVkPSJ5ZXMiPgogICAgICA8RW52aXJvbm1lbnQvPgogICAgICA8UHJvamVjdCBOYW1lPSJVT0NfUHJhY3QwIiBDb25maWdOYW1lPSJSZWxlYXNlIi8+CiAgICA8L1dvcmtzcGFjZUNvbmZpZ3VyYXRpb24+CiAgPC9CdWlsZE1hdHJpeD4KPC9Db2RlTGl0ZV9Xb3Jrc3BhY2U+Cg=="

PR_PATH = "NONE"
PR_NAME = "NONE"

INCLUDE_PATH = "./include"


def xml_b64_decoder(sample):
    """ Decodes sample data into usable xml object """
    _xml = base64.b64decode(sample)
    return ET.fromstring(_xml)


def project(argumentos):
    """ Creates a dict of arguments for the project """
    _dict_project = {}

    print("Nombre del Proyecto: {0}".format(argumentos.folder_path))
    print(
        argumentos.folder_path,
        type(argumentos.folder_path),
        argumentos.folder_path.exists(),
    )

    if argumentos.folder_path.exists():
        _dict_project["Name"] = argumentos.folder_path.name
        _dict_project["workspace_filename"] = "".join(
            [argumentos.folder_path.name, ".workspace"]
        )
        _dict_project["workspace_path"] = "".join(
            [argumentos.folder_path.name, "/", _dict_project["workspace_filename"]]
        )
        _dict_project["project_filename"] = "".join(
            [argumentos.folder_path.name, ".project"]
        )
        _dict_project["project_path"] = "".join(
            [argumentos.folder_path.name, "/", _dict_project["project_filename"]]
        )

    else:
        print("La carpeta no existe")
    return _dict_project


def crear():
    """ Creates Both XML Files for Codelite based on samples enconded in Base64 """
    with open("PR.projecto2", "wb") as pr_file, open("PR.workspace2", "wb") as ws_file:
        pr_file.write(base64.b64decode(PR_SAMPLE))
        ws_file.write(base64.b64decode(WS_SAMPLE))


def main():
    """ Main Entry Point """

    argument_parser = argparse.ArgumentParser(description="CookieCutter para Codelite")
    argument_parser.add_argument(
        "folder_path", type=Path, help="Nombre de la carpeta o proyecto"
    )
    argumentos = argument_parser.parse_args()
    project_vars = project(argumentos)

    ws_root = xml_b64_decoder(WS_SAMPLE)
    pr_root = xml_b64_decoder(PR_SAMPLE)

    ws_root.attrib["Name"] = project_vars["Name"]

    for child in ws_root.iter("Project"):
        child.attrib["Name"] = project_vars["Name"]
        if "Path" in child.attrib:
            child.attrib["Path"] = project_vars["project_path"]

    pr_root.attrib["Name"] = project_vars["Name"]

    # TODO: Añadir o cambiar el IncludePath segun arbol de directorios
    # for child in pr_root.iter("IncludePath"):
    #    child.attrib["Value"] = ",".join([child.attrib["Value"], INCLUDE_PATH])

    ws_tree = ET.ElementTree(ws_root)
    pr_tree = ET.ElementTree(pr_root)

    ws_tree.write(
        project_vars["workspace_filename"],
        xml_declaration=True,
        method="xml",
        encoding="UTF-8",
    )

    pr_tree.write(
        project_vars["project_path"],
        xml_declaration=True,
        method="xml",
        encoding="UTF-8",
    )

"""TODO: Añadir CDATA keywords al XML

    with open(project_vars["project_path"], "r+") as project_xml:
        content_read = project_xml.read()
        print(f"{content_read}")
        project_xml.seek(0)

        content = project_xml.readlines()
        print("-----------")
        print(f"content")

        content[23] = "        <![CDATA[]]>\n"
        content[63] = "        <![CDATA[]]>\n"

        project_xml.seek(0)
        project_xml.writelines(content)"""


if __name__ == "__main__":
    main()
