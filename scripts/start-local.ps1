[CmdletBinding()]
param(
    [switch]$NoBuild,
    [switch]$CheckOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$envPath = Join-Path $projectRoot ".env"
$examplePath = Join-Path $projectRoot ".env.example"

function New-SecureHexValue {
    param([int]$ByteCount = 32)

    $bytes = New-Object byte[] $ByteCount
    $generator = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try {
        $generator.GetBytes($bytes)
    }
    finally {
        $generator.Dispose()
    }

    return -join ($bytes | ForEach-Object { $_.ToString("x2") })
}

function Read-EnvironmentFile {
    param([string]$Path)

    $values = @{}
    foreach ($line in Get-Content -LiteralPath $Path) {
        $trimmed = $line.Trim()
        if (-not $trimmed -or $trimmed.StartsWith("#") -or -not $trimmed.Contains("=")) {
            continue
        }

        $parts = $trimmed.Split("=", 2)
        $values[$parts[0].Trim()] = $parts[1].Trim()
    }

    return $values
}

function Initialize-EnvironmentFile {
    if (Test-Path -LiteralPath $envPath) {
        Write-Host "Configuracion local encontrada. El archivo .env no fue modificado."
        return
    }

    if (-not (Test-Path -LiteralPath $examplePath)) {
        throw "No se encontro .env.example. No se creo ninguna configuracion."
    }

    $secretKey = New-SecureHexValue -ByteCount 32
    $databasePassword = New-SecureHexValue -ByteCount 24
    $lines = foreach ($line in Get-Content -LiteralPath $examplePath) {
        if ($line.StartsWith("DJANGO_SECRET_KEY=")) {
            "DJANGO_SECRET_KEY=$secretKey"
        }
        elseif ($line.StartsWith("POSTGRES_PASSWORD=")) {
            "POSTGRES_PASSWORD=$databasePassword"
        }
        else {
            $line
        }
    }

    $utf8WithoutBom = [System.Text.UTF8Encoding]::new($false)
    [System.IO.File]::WriteAllLines($envPath, $lines, $utf8WithoutBom)
    Write-Host "Configuracion local creada con secretos aleatorios."
}

function Assert-SafeEnvironment {
    $values = Read-EnvironmentFile -Path $envPath
    $problems = [System.Collections.Generic.List[string]]::new()

    $secretKey = if ($values.ContainsKey("DJANGO_SECRET_KEY")) {
        $values["DJANGO_SECRET_KEY"]
    }
    else {
        ""
    }
    $databasePassword = if ($values.ContainsKey("POSTGRES_PASSWORD")) {
        $values["POSTGRES_PASSWORD"]
    }
    else {
        ""
    }

    if ($secretKey.Length -lt 40 -or $secretKey -match "replace|unsafe|change-me") {
        $problems.Add("DJANGO_SECRET_KEY debe ser aleatoria y tener al menos 40 caracteres.")
    }
    if ($databasePassword.Length -lt 20 -or $databasePassword -match "replace|unsafe|change-me") {
        $problems.Add("POSTGRES_PASSWORD debe ser aleatoria y tener al menos 20 caracteres.")
    }
    if (-not $values.ContainsKey("DJANGO_ALLOWED_HOSTS")) {
        $problems.Add("Falta DJANGO_ALLOWED_HOSTS.")
    }

    if ($problems.Count -gt 0) {
        $details = $problems -join [Environment]::NewLine
        throw @"
La configuracion local no es segura y Docker no se iniciara:
$details

El archivo .env existente se conservo sin cambios.
No copies .env.example sobre una instalacion existente.
"@
    }
}

Push-Location $projectRoot
try {
    Initialize-EnvironmentFile
    Assert-SafeEnvironment
    Write-Host "Configuracion local validada."

    if ($CheckOnly) {
        Write-Host "Comprobacion terminada; Docker no fue iniciado."
        exit 0
    }

    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        throw "Docker no esta disponible. Abre Docker Desktop y vuelve a intentarlo."
    }

    docker compose config --quiet
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose rechazo la configuracion antes del arranque."
    }

    if ($NoBuild) {
        docker compose up -d
    }
    else {
        docker compose up -d --build
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Docker no pudo iniciar los servicios."
    }

    $deadline = (Get-Date).AddSeconds(60)
    $health = "starting"
    do {
        Start-Sleep -Seconds 2
        $containerId = docker compose ps -q web
        if ($containerId) {
            $health = docker inspect --format "{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}" $containerId
        }
    } while ($health -eq "starting" -and (Get-Date) -lt $deadline)

    if ($health -ne "healthy" -and $health -ne "running") {
        throw "El servicio web termino con estado '$health'. Ejecuta: docker compose logs --tail 40 web"
    }

    Write-Host "Nexo Norte esta listo en http://localhost:8000"
}
finally {
    Pop-Location
}
