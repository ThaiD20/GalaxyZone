from cx_Freeze import setup, Executable
import os
import sys


diretorio_atual = os.path.abspath(os.path.dirname(__file__))
pasta_assets = os.path.join(diretorio_atual, "assets")
pasta_src = os.path.join(diretorio_atual, "src")


arquivos_incluidos = [
    (pasta_assets, "assets"),
    (pasta_src, "src")
]


base = None
if sys.platform == "win32":

    base = None

executables = [
    Executable(
        "main.py",
        base=base,
        target_name="GalaxyZone.exe" # Nome do seu arquivo final
    )
]

setup(
    name="GalaxyZone",
    version="1.0",
    description="Jogo GalaxyZone",
    options={
        "build_exe": {
            "packages": ["pygame", "os", "sys", "random"],
            "include_files": arquivos_incluidos,
        }
    },
    executables=executables
)

# python setup.py build - Gerador de executavel