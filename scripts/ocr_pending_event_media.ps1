param(
    [string]$Manifest = "output/audit-flyers/manifest.json",
    [string]$Output = "output/audit-flyers/ocr-windows.json"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime]

function Await-WinRt($Operation, $ResultType) {
    $method = [System.WindowsRuntimeSystemExtensions].GetMethods() |
        Where-Object {
            $_.Name -eq "AsTask" -and $_.IsGenericMethod -and
            $_.GetParameters().Count -eq 1
        } |
        Select-Object -First 1
    $task = $method.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    $task.Wait()
    return $task.Result
}

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($null -eq $engine) {
    throw "O mecanismo OCR do Windows não está disponível."
}

$root = (Resolve-Path ".").Path
$payload = Get-Content -LiteralPath $Manifest -Raw -Encoding UTF8 | ConvertFrom-Json
$results = [System.Collections.Generic.List[object]]::new()
$failures = [System.Collections.Generic.List[object]]::new()

foreach ($item in $payload.items) {
    $relative = [string]$item.path
    $suffix = [IO.Path]::GetExtension($relative).ToLowerInvariant()
    if ($suffix -notin @(".jpg", ".jpeg", ".png", ".webp", ".gif")) {
        $failures.Add([pscustomobject]@{
            slug = [string]$item.slug
            path = $relative
            error = "formato_não_suportado_pelo_ocr"
        })
        continue
    }
    try {
        $absolute = [IO.Path]::GetFullPath((Join-Path $root $relative))
        $file = Await-WinRt ([Windows.Storage.StorageFile]::GetFileFromPathAsync($absolute)) ([Windows.Storage.StorageFile])
        $stream = Await-WinRt ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
        $decoder = Await-WinRt ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bitmap = Await-WinRt ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        $ocr = Await-WinRt ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
        $results.Add([pscustomobject]@{
            slug = [string]$item.slug
            url = [string]$item.url
            path = $relative
            text = [string]$ocr.Text
        })
        $stream.Dispose()
    }
    catch {
        $failures.Add([pscustomobject]@{
            slug = [string]$item.slug
            path = $relative
            error = $_.Exception.Message
        })
    }
}

$report = [ordered]@{
    processed = $results.Count
    failed = $failures.Count
    engine = "Windows.Media.Ocr"
    items = $results
    failures = $failures
}
$json = $report | ConvertTo-Json -Depth 6
[IO.File]::WriteAllText((Join-Path $root $Output), $json, [Text.UTF8Encoding]::new($false))
$report | Select-Object processed, failed, engine | ConvertTo-Json -Compress
