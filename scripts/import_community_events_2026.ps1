param(
    [string]$OutputPath = (Join-Path $PSScriptRoot "..\content\events\agenda-comunitaria-2026.json")
)

$ErrorActionPreference = "Stop"
$sourceUrl = "https://jb-rider.com.br/eventos.php"
$today = [datetime]"2026-07-25"
$brazilianStates = @(
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
    "SP", "SE", "TO"
)

function Remove-Diacritics([string]$Value) {
    if (-not $Value) { return "" }
    $normalized = $Value.Normalize([Text.NormalizationForm]::FormD)
    $builder = [Text.StringBuilder]::new()
    foreach ($character in $normalized.ToCharArray()) {
        if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($character) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$builder.Append($character)
        }
    }
    return $builder.ToString().Normalize([Text.NormalizationForm]::FormC)
}

function ConvertTo-Slug([string]$Value) {
    $slug = (Remove-Diacritics $Value).ToLowerInvariant()
    $slug = [regex]::Replace($slug, "[^a-z0-9]+", "-").Trim("-")
    return $slug
}

function ConvertTo-IsoDate([string]$Value) {
    return [datetime]::ParseExact($Value, "dd/MM/yyyy", [Globalization.CultureInfo]::InvariantCulture).ToString("yyyy-MM-dd")
}

function Get-EventType([string]$Title) {
    $value = (Remove-Diacritics $Title).ToLowerInvariant()
    if ($value -match "passeio|motociata|romaria|missa|bencao") { return "Passeio e mobilização motociclística" }
    if ($value -match "benefic|solidari|acao social") { return "Ação beneficente sobre duas rodas" }
    if ($value -match "motocross|velocross|enduro|trilhao|trilha") { return "Motociclismo off-road" }
    if ($value -match "festival|motofest|moto fest|motorock|moto rock|bike fest|biker fest") { return "Festival de motociclismo" }
    if ($value -match "anivers|niver|anos|mc|moto clube|motoclube") { return "Encontro de moto clube" }
    return "Encontro de motociclistas"
}

function Get-Segment([string]$Title) {
    $value = (Remove-Diacritics $Title).ToLowerInvariant()
    if ($value -match "scooter|vespa") { return "Scooters" }
    if ($value -match "moto|motoc|motorock|\bmc\b") { return "Motos" }
    if ($value -match "bicic|ciclismo|mtb|pedal|bmx|e-bike|bike and run|bike fest|biker fest") { return "Bicicletas" }
    return "Motos"
}

function New-EventRecord {
    param(
        [string]$Title,
        [string]$StartDate,
        [string]$EndDate,
        [string]$City,
        [string]$State,
        [string]$EventType,
        [string]$Segment,
        [string]$Source,
        [string]$SourceLabel,
        [string]$Verification = "agenda_comunitaria"
    )
    $slug = ConvertTo-Slug "$Title-$City-$State-$StartDate"
    return [ordered]@{
        slug = $slug
        title = $Title
        short_name = $Title
        start_date = $StartDate
        end_date = $EndDate
        city = $City
        state = $State
        country = "Brasil"
        scope = "Nacional"
        region = ""
        venue = "Local informado pelo organizador"
        status = "agendada"
        event_type = $EventType
        segment = $Segment
        official_url = $Source
        source_url = $Source
        source_label = $SourceLabel
        verification_status = $Verification
        cover = "/assets/img/competicoes-eventos-default.svg"
        image_credit = "Arte: TVDUASRODAS"
        featured = $false
        free = $false
        summary = "$EventType em $City/$State, com data divulgada para 2026. Confirme local, horário, acesso e programação diretamente com a organização antes de viajar."
        attractions = @()
        body = "## Serviço`n`nEvento incluído na agenda nacional da TVDUASRODAS para ampliar a visibilidade de encontros locais e regionais. As informações vieram da agenda indicada como fonte e podem ser atualizadas pelo organizador.`n`n## Confirme antes de sair`n`nConsulte o canal do evento, o moto clube responsável ou a prefeitura local para confirmar endereço, horários, regras de acesso, camping, inscrições e eventuais alterações."
        last_updated = "2026-07-25T12:00:00-04:00"
    }
}

$html = (Invoke-WebRequest -UseBasicParsing $sourceUrl).Content
$matches = [regex]::Matches(
    $html,
    '<strong style="font-size:0\.95rem;">\s*([^<]+)<br>\s*([^<]+)</strong>',
    [Text.RegularExpressions.RegexOptions]::IgnoreCase
)

$records = [Collections.Generic.List[object]]::new()
foreach ($match in $matches) {
    $dateText = [Net.WebUtility]::HtmlDecode($match.Groups[1].Value).Trim()
    $label = [Net.WebUtility]::HtmlDecode($match.Groups[2].Value).Trim()
    if ($dateText -notmatch "^(\d{2}/\d{2}/2026)(?:\s+a\s+(\d{2}/\d{2}/2026))?$") { continue }

    $startDate = ConvertTo-IsoDate $Matches[1]
    $endDate = if ($Matches[2]) { ConvertTo-IsoDate $Matches[2] } else { $startDate }
    if ([datetime]$endDate -lt $today) { continue }

    if ($label -notmatch "^(.*?)\s+-\s+(.+)-([A-Z]{2})$") { continue }
    $title = $Matches[1].Trim(" ", "_", "-").Replace([char]0xFFFD, "i")
    $city = $Matches[2].Trim(" ", "_", "-").Replace([char]0xFFFD, "i")
    $state = $Matches[3].ToUpperInvariant()
    if (-not $title -or -not $city -or $state -notin $brazilianStates) { continue }
    if ($title -match "^(teste|prog|programa|flyer)$") { continue }

    $record = New-EventRecord `
        -Title $title `
        -StartDate $startDate `
        -EndDate $endDate `
        -City $city `
        -State $state `
        -EventType (Get-EventType $title) `
        -Segment (Get-Segment $title) `
        -Source $sourceUrl `
        -SourceLabel "Agenda comunitária JB-RIDER"
    [void]$records.Add($record)
}

$supplemental = @(
    @{ Title = "18º Encontro Internacional de Motos de Altas Cilindradas"; Start = "2026-08-14"; End = "2026-08-15"; City = "Boa Vista"; State = "RR"; Type = "Encontro de motociclistas"; Segment = "Motos"; Url = "https://www.folhabv.com.br/variedades/roraima-moto-clube-inicia-vendas-para-18o-encontro-de-motos-de-altas-cilindradas-neste-sabado-9/"; Label = "Roraima Moto Clube / Folha BV"; Verification = "fonte_local" },
    @{ Title = "Motoimp 2026"; Start = "2026-09-03"; End = "2026-09-06"; City = "Imperatriz"; State = "MA"; Type = "Festival de moto e rock"; Segment = "Motos"; Url = "https://motoimp.com.br/"; Label = "Site oficial Motoimp"; Verification = "fonte_oficial" },
    @{ Title = "Motoshow 2026"; Start = "2026-07-31"; End = "2026-08-02"; City = "Três Lagoas"; State = "MS"; Type = "Festival de motociclismo"; Segment = "Motos"; Url = "https://www.motoshowtl.com.br/"; Label = "Site oficial Motoshow"; Verification = "fonte_oficial" },
    @{ Title = "Diamantina Motofest 2026"; Start = "2026-09-04"; End = "2026-09-07"; City = "Diamantina"; State = "MG"; Type = "Festival de motociclismo"; Segment = "Motos"; Url = "https://dtnamotofest.com.br/"; Label = "Site oficial Diamantina Motofest"; Verification = "fonte_oficial" },
    @{ Title = "20º Encontro de Motociclistas MotoNave"; Start = "2026-10-30"; End = "2026-11-01"; City = "Navegantes"; State = "SC"; Type = "Encontro de motociclistas"; Segment = "Motos"; Url = "https://navegantes.sc.gov.br/wp-content/uploads/2026/04/EDITAL-4.pdf"; Label = "Prefeitura de Navegantes"; Verification = "fonte_oficial" },
    @{ Title = "Motoara 2026"; Start = "2026-10-10"; End = "2026-10-11"; City = "Araguaína"; State = "TO"; Type = "Encontro de motos e motociclismo"; Segment = "Motos"; Url = "https://www.al.to.leg.br/arquivos/diario-oficial_4275_80966.PDF"; Label = "Assembleia Legislativa do Tocantins"; Verification = "fonte_oficial" },
    @{ Title = "Campeonato Amapaense de Ciclismo 2026"; Start = "2026-08-01"; End = "2026-12-31"; City = "Macapá"; State = "AP"; Type = "Campeonato estadual de estrada, contrarrelógio e MTB"; Segment = "Bicicletas"; Url = "https://esportecorrida.com.br/upload_diversos/11_02_2026_15_44_50.pdf"; Label = "Federação Amapaense de Ciclismo"; Verification = "calendario_oficial_datas_parciais" },
    @{ Title = "Campeonato de Motocross de Rondônia 2026"; Start = "2026-08-01"; End = "2026-08-31"; City = "Cerejeiras e Corumbiara"; State = "RO"; Type = "Motocross estadual"; Segment = "Motos"; Url = "https://www.rondoniaovivo.com/noticia/esporte/2026/02/24/calendario-cheio-limero-divulga-programacao-das-competicoes-de-motocross-para-2026.html"; Label = "LIMERO / Rondônia ao Vivo"; Verification = "fonte_local_datas_parciais" }
)

foreach ($item in $supplemental) {
    [void]$records.Add((New-EventRecord `
        -Title $item.Title `
        -StartDate $item.Start `
        -EndDate $item.End `
        -City $item.City `
        -State $item.State `
        -EventType $item.Type `
        -Segment $item.Segment `
        -Source $item.Url `
        -SourceLabel $item.Label `
        -Verification $item.Verification))
}

$stateRegions = @{
    AC = "Norte"; AP = "Norte"; AM = "Norte"; PA = "Norte"; RO = "Norte"; RR = "Norte"; TO = "Norte"
    AL = "Nordeste"; BA = "Nordeste"; CE = "Nordeste"; MA = "Nordeste"; PB = "Nordeste"; PE = "Nordeste"; PI = "Nordeste"; RN = "Nordeste"; SE = "Nordeste"
    DF = "Centro-Oeste"; GO = "Centro-Oeste"; MT = "Centro-Oeste"; MS = "Centro-Oeste"
    ES = "Sudeste"; MG = "Sudeste"; RJ = "Sudeste"; SP = "Sudeste"
    PR = "Sul"; RS = "Sul"; SC = "Sul"
}

$seen = @{}
$deduplicated = foreach ($record in ($records | Sort-Object { $_["start_date"] }, { $_["state"] }, { $_["city"] }, { $_["title"] })) {
    $record.region = $stateRegions[$record.state]
    $key = ConvertTo-Slug "$($record.start_date)-$($record.end_date)-$($record.state)-$($record.city)-$($record.title)"
    if ($seen.ContainsKey($key)) { continue }
    $seen[$key] = $true
    $record
}

$payload = [ordered]@{
    title = "Agenda comunitária nacional de duas rodas 2026"
    source_url = $sourceUrl
    last_updated = "2026-07-25T12:00:00-04:00"
    methodology = "Fatos básicos de agenda (nome, data, cidade e UF), deduplicados e complementados por fontes oficiais e locais. Itens comunitários exigem confirmação com o organizador."
    entries = @($deduplicated)
}

$resolvedOutput = [IO.Path]::GetFullPath($OutputPath)
$json = $payload | ConvertTo-Json -Depth 8
[IO.File]::WriteAllText($resolvedOutput, $json, [Text.UTF8Encoding]::new($false))
Write-Output "Agenda gravada em $resolvedOutput com $($deduplicated.Count) eventos."
