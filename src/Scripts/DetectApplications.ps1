Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*,
                 HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* |
    Where-Object { $_.DisplayName } |
    Select-Object DisplayName, DisplayVersion, Publisher,
        @{Name="Executable";Expression={
            $exe = $_.DisplayIcon
            if ($exe -and $exe -match "\.exe") {
                ($exe -split ",")[0]
            }
            elseif ($_.InstallLocation) {
                $primary = Get-ChildItem $_.InstallLocation -Filter *.exe -File -ErrorAction SilentlyContinue |
                           Sort-Object Length -Descending |
                           Select-Object -First 1
                if ($primary) { $primary.FullName }
            }
        }} |
    Where-Object { $_.Executable } |
    Sort-Object DisplayName |
    Format-List DisplayName, Executable
    Out-String -Width 4096