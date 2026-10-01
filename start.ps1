param(
  [int]$Port = 8000
)

# Reads GEMINI_API_KEY / TAVILY_API_KEY from your Windows user environment.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not $env:GEMINI_API_KEY) { $env:GEMINI_API_KEY = [Environment]::GetEnvironmentVariable("GEMINI_API_KEY", "User") }
if (-not $env:TAVILY_API_KEY) { $env:TAVILY_API_KEY = [Environment]::GetEnvironmentVariable("TAVILY_API_KEY", "User") }

Write-Host "GEMINI_API_KEY : $(if ($env:GEMINI_API_KEY) { 'set' } else { 'missing' })"
Write-Host "TAVILY_API_KEY : $(if ($env:TAVILY_API_KEY) { 'set' } else { 'missing' })"

python -m uvicorn main:app --port $Port
