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
    python.exe -m venv venv
}

& "$PSScriptRoot\venv\Scripts\Activate.ps1"

python.exe -m pip install -U pip
python.exe -m pip install -U -r "requirements.txt"

try {
    $env:config | Out-File -FilePath "config.json"
}
catch {
    Write-Error "Could not export config to config.json"
}

python.exe index.py