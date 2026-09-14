$root='D:\nexus-xau-engine-repo'
Write-Output '### DOCS'
Get-ChildItem "$root\docs" -File |
  Where-Object { $_.Name -match '0700|07_00|DAILY_FRAME|REMAINING_RUN|INHERITED_ORIGIN|MTF_ALIGNMENT|PATH_REMAINING|MAE_PLA' } |
  Sort-Object LastWriteTime,Name |
  Select-Object Name,LastWriteTime,Length |
  Format-Table -AutoSize
Write-Output '### RESULTS'
Get-ChildItem "$root\results" -Directory |
  Where-Object { $_.Name -match '0700|REMAINING|DAILY|INHERITED|MTF|PATH' } |
  Sort-Object Name |
  Select-Object Name,LastWriteTime |
  Format-Table -AutoSize
