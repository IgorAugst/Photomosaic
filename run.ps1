<#
.SYNOPSIS
    Programa que cria um mosaico fotografico
.DESCRIPTION
    .
.PARAMETER dir
    diretorio para o arquivo
.PARAMETER sai
    diretorio de saida da imagem
.PARAMETER res
    quantidade de imagens para compor o mosaico
.PARAMETER fac
    resolucao das imagens menores
.PARAMETER pretoBranco
    utilizado para gerar imagens em preto e branco
.PARAMETER update
    utilizado para atualizar os dados das imagens
.PARAMETER imagens
    Diretorio do conjunto de imagens
#>


param(
    [Parameter(Mandatory=$true)]        
    [string]$dir,
    [string]$sai = "./",
    [int]$res = 60,
    [int]$fac = 100,
    [switch]$pretoBranco = $false,
    [switch]$update = $false,
    [string]$imagens = "./images"
)

if($update){
    & "python.exe" "./src/Process.py" $imagens
    Write-Host("Atualizado")
}

& "python.exe" "./src/Mosaic.py" $dir $sai $res $fac $pretoBranco $imagens
Write-Host "Fim"