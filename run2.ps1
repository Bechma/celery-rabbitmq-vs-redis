$brokers = @("redis", "rabbit")
$messages = @(100, 200)

For ($iter = 0; $iter -lt 3; $iter++) {
    foreach ($i in $brokers) {
        foreach ($j in $messages) {
            python .\app.py $i $j 1000000
        }
    }
}
