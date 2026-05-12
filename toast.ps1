# Example
# `notify --text "Failed to connect to server" --title "Connection Error" --icon Error --baloon-icon Error`
param(
    [Parameter(Position=0)]
    [Alias('text')]
    [string]$TipText = 'm',

    [Alias('title')]
    [string]$TipTitle = $null,

    [Alias('icon')]
    [ValidateSet(
        'Application',
        'Asterisk',
        'Error',
        'Exclamation',
        'Hand',
        'Information',
        'Question',
        'Shield',
        'Warning',
        'WinLogo'
    )]
    [string]$TipIcon = 'Application',

    [Alias('baloon-icon')]
    [ValidateSet('None', 'Info', 'Warning', 'Error')]
    [string]$BaloonTipIcon = 'None',

    [int]$Timeout = 10,
    [bool]$Visible = $true
)

[reflection.assembly]::loadwithpartialname('System.Windows.Forms') > $NULL
[reflection.assembly]::loadwithpartialname('System.Drawing') > $NULL


#
#
$notifyicon = New-Object System.Windows.Forms.NotifyIcon

$notifyicon.icon              = [System.Drawing.SystemIcons]::($TipIcon)
$notifyicon.visible           = $Visible
$notifyicon.text              = 'z'
$notifyicon.balloonTipIcon    = [System.Windows.Forms.ToolTipIcon]::Parse([System.Windows.Forms.ToolTipIcon], $BaloonTipIcon)
$notifyicon.balloonTipTitle   = $TipTitle
$notifyicon.balloonTipText    = $TipText

$notifyicon.ShowBalloonTip($Timeout)
