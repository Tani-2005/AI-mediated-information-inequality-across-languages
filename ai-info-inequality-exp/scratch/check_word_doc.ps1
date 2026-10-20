$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docPath = (Resolve-Path ".\paper\word_preprint\LINGUA_AUDIT_preprint.docx").Path
    $doc = $word.Documents.Open($docPath)
    $pageCount = $doc.ComputeStatistics(2) # 2 = wdStatisticPages
    $wordCount = $doc.ComputeStatistics(0) # 0 = wdStatisticWords
    $tableCount = $doc.Tables.Count
    Write-Host "Word COM successfully opened document: $docPath"
    Write-Host "Page count: $pageCount"
    Write-Host "Word count: $wordCount"
    Write-Host "Table count: $tableCount"
    
    $pdfPath = [System.IO.Path]::ChangeExtension($docPath, ".pdf")
    $doc.SaveAs([ref]$pdfPath, [ref]17) # 17 = wdFormatPDF
    Write-Host "Exported PDF to: $pdfPath"
}
finally {
    if ($doc) { $doc.Close([ref]$false) }
    $word.Quit()
}
