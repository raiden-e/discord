try {
    python.exe --version
    if ($LASTEXITCODE -ne 0) {
        throw "Exitcode $LASTEXITCODE"
    }
}
catch {
    throw "Python is not installed"
}
if (!(Test-Path -Path "$PSScriptRoot\venv" -PathType Container)) {
    python.exe -m virtualenv venv
}

& "$PSScriptRoot\venv\Scripts\Activate.ps1"

python.exe -m pip install -U pip
python.exe -m pip install -U -r "requirements.txt"
python.exe index.py