param(
    [string]$Prompt = 'm',
    [string]$Title  = ''
)

[reflection.assembly]::loadwithpartialname('System.Windows.Forms') > $NULL
[reflection.assembly]::loadwithpartialname('System.Drawing') > $NULL
$notify = new-object system.windows.forms.notifyicon
$notify.icon = [System.Drawing.SystemIcons]::Information
$notify.visible = $true
$notify.showballoontip(10, $Title, $Prompt, [system.windows.forms.tooltipicon]::None)
