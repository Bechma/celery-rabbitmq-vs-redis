$brokers = @("redis", "rabbit")
$messages = @(100, 500, 1000, 5000, 10000, 50000)

For ($iter = 0; $iter -lt 5; $iter++) {
    foreach ($i in $brokers) {
        foreach ($j in $messages) {
            python .\app.py $i $j
        }
    }
}
